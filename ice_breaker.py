from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    print("Hello, LangChain!")

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts
    """

    summary_prompt_template = PromptTemplate(input_variables="information", template=summary_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini-2024-07-18")
    
    chain = summary_prompt_template | llm
   
    res = chain.invoke(input={"information": "John is a software engineer from San Francisco."})
    print(res)


    