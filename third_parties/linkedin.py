import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_url: str, mock: bool = False) -> dict:
    """scrape information from linkedin profiles,
    Manually scrape information from a LinkedIn profile. 
    Args:
        linkedin_url (str): The URL of the LinkedIn profile.
        mock (bool, optional): Whether to use mock data. Defaults to False.
    """
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