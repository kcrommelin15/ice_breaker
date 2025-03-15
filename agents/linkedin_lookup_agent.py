import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
# Fix the import statement - use relative import
from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0, 
        model_name="gpt-4o-mini-2024-07-18"
        )
    template = """
        given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page. Your answer should contain only a URL.
        """

    prompt_template = PromptTemplate(
        input_variables="name_of_person", 
        template=template
        )
    
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profle page",
            function=get_profile_url_tavily,
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
        input={"input": prompt_template.format_prompt(name_of_person=name)}
        )
    print(result)
    linkedin_proile_url = result["output"]

    return linkedin_proile_url

if __name__ == "__main__":
    linkedin_url = lookup(name = "Kevin Crommelin")
    print(linkedin_url)