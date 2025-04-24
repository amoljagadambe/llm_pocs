import requests
import streamlit as st

def get_open_ai_response(input_text):
    response = requests.post(url='http://localhost:8080/essay/invoke',
                              json={'input':{'topic':input_text}})
    
    return response.json()['output']['content']

def get_mistral_ai_response(input_text):
    response = requests.post(url='http://localhost:8080/poem/invoke',
                              json={'input':{'topic':input_text}})
    
    return response.json()['output']['content']

st.title('Langchain Deom with Langserve')
input_text_openai = st.text_input(' (Open AI)write esssay On')
if input_text_openai:
    st.write(get_open_ai_response(input_text_openai))

input_text_mistralai = st.text_input('(Mistral AI)write Poem On')
if input_text_mistralai:
    st.write(get_mistral_ai_response(input_text_mistralai))

