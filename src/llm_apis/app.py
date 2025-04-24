from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI

load_dotenv() # load dot env file

os.environ['LANGSMITH_PROJECT'] = f'{os.getenv("LANGSMITH_PROJECT")}-apis' # overwrite the langsmith project name


app = FastAPI(
    title='Langchain Server',
    version='1.0',
    description='A simple API Server'
)


opena_ai = ChatOpenAI()
mistral_ai = ChatMistralAI(model_name='mistral-large-latest')

prompt_one = ChatPromptTemplate.from_template('write me an essay about {topic} with 100 words')
prompt_two = ChatPromptTemplate.from_template('write me an poem about {topic} with 100 words')

add_routes(
    app,
    prompt_one | opena_ai,
    path = '/essay'
)

add_routes(
    app,
    prompt_two | mistral_ai,
    path= '/poem'
)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080)
