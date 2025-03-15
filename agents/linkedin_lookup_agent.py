import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add the parent directory to sys.path to enable imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
from tools.tools import get_profile_url_tavily

def extract_first_profile_url(search_results, name):
    """
    Extract the first specific LinkedIn profile URL from search results.
    Skip directory pages and look for direct profile URLs.
    """
    if not search_results:
        return None
        
    # First, try to find a direct profile URL (not a directory)
    for result in search_results:
        url = result.get('url', '')
        if 'linkedin.com/in/' in url and '/pub/dir/' not in url:
            print(f"Found specific LinkedIn profile: {url}")
            return url
    
    # If no direct profile is found, return the first LinkedIn URL (even if it's a directory)
    for result in search_results:
        url = result.get('url', '')
        if 'linkedin.com' in url:
            return url
            
    return None

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0, 
        model_name="gpt-4o-mini-2024-07-18"
        )
    template = """
        given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
        Try to find a direct profile URL that contains '/in/' in the URL rather than a directory page.
        Your answer should contain only a URL.
        """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], 
        template=template
        )
    
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profle page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Linkedin Page URL"
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name).to_string()}
        )
    
    # Get raw search results to potentially extract a better URL
    raw_search_results = []
    try:
        for action in result.get('intermediate_steps', []):
            if isinstance(action[1], list):
                raw_search_results = action[1]
                break
    except Exception as e:
        print(f"Error extracting raw search results: {e}")
    
    # Process the search results to get the best profile URL
    if raw_search_results and '/pub/dir/' in result["output"]:
        print("Directory URL detected in results. Attempting to find specific profile...")
        specific_url = extract_first_profile_url(raw_search_results, name)
        if specific_url and '/in/' in specific_url:
            print(f"Found better URL: {specific_url}")
            return specific_url
    
    print(result)
    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name = "Rachel Underbakke")
    print(linkedin_url)