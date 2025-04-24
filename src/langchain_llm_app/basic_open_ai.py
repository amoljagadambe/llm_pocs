from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.agents import initialize_agent, load_tools, AgentType
from dotenv import load_dotenv

load_dotenv() # load the open ai key

def genrate_pet_name(animal_type):
    """
    we could have used the Chat Open AI and Chat Prompt Template but we just wanted to invoke the llm
    if we are dealing with tools then we have to work with Chat API.
    """
    prompt_template = PromptTemplate.from_template(
        "give me the five best name for my {animal_type}"
    )
    llm = OpenAI(temperature=0.5, model="gpt-4.1",)
    name_chain =  prompt_template | llm
    response = name_chain.invoke({'animal_type': animal_type})
    return response


if __name__ == "__main__":
    response  = genrate_pet_name('sheep')
    print(response)