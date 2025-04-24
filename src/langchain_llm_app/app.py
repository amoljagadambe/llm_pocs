from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv() # load all the Keys


# prompt template

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template('You are helpful assistant. Please resonse to the user queries'),
    HumanMessagePromptTemplate.from_template('Question: {question}')
])

# streamlit framework
st.title('Langchain Demo with OpenAi API')
input_text = st.text_input('Search the topic you want')


# call open AI API
llm = ChatOpenAI(model='gpt-3.5-turbo')
mistral_llm = ChatMistralAI(model_name='mistral-large-latest')
output = StrOutputParser()

# create the cahin
chain = prompt | mistral_llm | output

if input_text:
    st.write(chain.invoke({'question': input_text}))




    