from typing import Tuple
from dotenv import load_dotenv
from output_parsers import summary_parser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name:str)-> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    # Pass the name parameter to help when dealing with directory URLs
    linkedin_data = scrape_linkedin_profile(linkedin_url=linkedin_url, mock=False, name=name)
    
    # Check if we got an error from the LinkedIn scraper
    if "error" in linkedin_data:
        print(f"Error scraping LinkedIn profile: {linkedin_data['error']}")
        print(f"Note: {linkedin_data['note']}")
        
        if "Directory URL" in linkedin_data.get("error", ""):
            print("Try searching for a more specific name or provide a direct LinkedIn profile URL.")
            return "LinkedIn profile could not be found or processed."
    
    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts
        /n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
        )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini-2024-07-18")

    # chain = summary_prompt_template | llm | StrOutputParser()

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information":linkedin_data})

    return res, linkedin_data.get("photoUrl") 

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker")
    result = ice_break_with(name="Douglas Heinzel")
    print("\nResult:")
    print(result)

