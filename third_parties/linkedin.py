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
    # if mock:
    #     return {
    #         "name": "John Doe",
    #         "title": "Software Engineer",
    #         "location": "San Francisco, CA",
    #         "summary": "I am a software engineer with 5 years of experience.",
    #     }

    # headers = {
    #     "Authorization": f"Bearer {os.getenv('LINKEDIN_TOKEN')}",
    #     "Accept": "application/json",
    # }
    # response = requests.get(linkedin_url, headers=headers)
    # response.raise_for_status()
    # data = response.json()

    # return {
    #     "name": data["localizedFirstName"] + " " + data["localizedLastName"],
    #     "title": data["localizedHeadline"],
    #     "location": data["location"]["name"],
    #     "summary": data["summary"],
    # }