import os
import requests
import re
from dotenv import load_dotenv
import time

load_dotenv()

def extract_profile_from_directory(directory_url, name):
    """
    When encountering a LinkedIn directory URL, attempt to extract a specific profile.
    This is a simplified approach that needs the scrapin.io API or web scraping for a production solution.
    For now, we'll attempt to find a specific profile by querying with more specific information.
    """
    print(f"Directory URL detected: {directory_url}")
    print(f"Attempting to find specific profile for {name}...")
    
    # Try using the directory enrichment endpoint if available
    try:
        api_endpoint = "https://api.scrapin.io/enrichment/directory"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": directory_url,
        }
        
        response = requests.get(api_endpoint, params=params, timeout=10)
        data = response.json()
        
        # Check if the API returned profile options
        if data and "profiles" in data and data["profiles"]:
            profiles = data["profiles"]
            # Return the first profile URL, which is likely the most relevant
            print(f"Found specific profile: {profiles[0]['url']}")
            return profiles[0]['url']
    except Exception as e:
        print(f"Directory API approach failed: {e}")
    
    # Fallback: Try an alternative search approach by constructing a more specific URL
    # This is a simple approach - a production system would implement more advanced logic
    try:
        # Try to construct a likely profile URL based on the name
        name_parts = name.lower().split()
        first_name = name_parts[0]
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        # Try a direct search for this person using the scrapin.io API
        api_endpoint = "https://api.scrapin.io/search"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "query": f"{name} linkedin",
        }
        
        response = requests.get(api_endpoint, params=params, timeout=10)
        results = response.json().get("results", [])
        
        # Look for specific profile URLs (containing '/in/')
        for result in results:
            url = result.get("url", "")
            if "linkedin.com/in/" in url:
                print(f"Found specific profile through search: {url}")
                return url
    except Exception as e:
        print(f"Search approach failed: {e}")
    
    # If we couldn't extract a specific profile, return None
    return None

def scrape_linkedin_profile(linkedin_url: str, mock: bool = False, name: str = None) -> dict:
    """scrape information from linkedin profiles,
    Manually scrape information from a LinkedIn profile. 
    Args:
        linkedin_url (str): The URL of the LinkedIn profile.
        mock (bool, optional): Whether to use mock data. Defaults to False.
        name (str, optional): The person's name. Used for directory lookup.
    """
    # Check if the URL is a directory page
    if "pub/dir/" in linkedin_url:
        print(f"Warning: The URL {linkedin_url} is a directory page, not a specific profile.")
        
        # Try to extract a specific profile URL from the directory
        specific_profile_url = extract_profile_from_directory(linkedin_url, name)
        
        if specific_profile_url:
            print(f"Found specific profile: {specific_profile_url}")
            # Call this function again with the specific URL
            # Add a small delay to prevent API rate limits
            time.sleep(1)
            return scrape_linkedin_profile(specific_profile_url, mock)
        else:
            # Fallback to a more aggressive search using the full name
            # This would ideally use a more sophisticated search mechanism in a production system
            if name:
                print(f"Attempting direct profile construction for {name}...")
                name_parts = name.lower().split()
                if len(name_parts) >= 2:
                    # Try the first common LinkedIn URL pattern
                    first_name = name_parts[0]
                    last_name = name_parts[-1]
                    constructed_url = f"https://www.linkedin.com/in/{first_name}-{last_name}"
                    
                    print(f"Trying constructed URL: {constructed_url}")
                    # Try to scrape this URL
                    try:
                        api_endpoint = "https://api.scrapin.io/enrichment/profile"
                        params = {
                            "apikey": os.getenv("SCRAPIN_API_KEY"),
                            "linkedInUrl": constructed_url,
                        }
                        response = requests.get(api_endpoint, params=params, timeout=10)
                        if response.status_code == 200 and response.json().get("person"):
                            print(f"Successfully found profile at constructed URL: {constructed_url}")
                            return scrape_linkedin_profile(constructed_url, mock)
                    except Exception as e:
                        print(f"Error with constructed URL: {e}")
            
            # If all attempts fail, return a placeholder
            return {
                "error": "Directory URL provided - not a specific profile",
                "url": linkedin_url,
                "name": name,
                "note": "Multiple profiles exist for this name. The system attempted to find a specific profile but was unsuccessful."
            }
        
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/kcrommelin15/aef7ab6765f7e59e9d986f91c79ad74d/raw/466b38fe2b5333f41088a6e0218297e1788f3b57/kevin-li-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)
    
    data = response.json().get("person")
    
    # Check if we received valid person data
    if data is None:
        print(f"Warning: No profile data found for {linkedin_url}")
        return {
            "error": "No profile data found",
            "url": linkedin_url,
            "note": "The API could not retrieve profile information for this URL."
        }
        
    data = {
        k: v
        for k, v in data.items()
        if v not in ([],"", "", None)
        and k not in ["certifications"]
    }
    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://www.linkedin.com/in/kcrommelin/",
            mock=True
        )
    )