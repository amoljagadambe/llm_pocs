import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_weaviate.vectorstores import WeaviateVectorStore
from weaviate.auth import Auth
import time
import weaviate


load_dotenv() # load all the env variable

groq_api_key = os.getenv('GROQ_API_KEY')


if 'vector' not in st.session_state:
    st.session_state.embeddings = OpenAIEmbeddings()
    """
    We will use the langsmith collection created on vector store.
    """
    client = weaviate.connect_to_weaviate_cloud(
            cluster_url=f'https://{os.getenv("WEAVIATE_URL")}',
            auth_credentials=Auth.api_key(os.getenv('WEAVIATE_API_KEY')),
            headers={
                    'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY') # openai api key for vectorizer & generative
                }
        )
    st.session_state.vectors = WeaviateVectorStore(client=client, index_name="Langsmith", text_key="content", embedding=st.session_state.embeddings)
    
st.title('Chat GROQ Demo.!')
llm= ChatGroq(model='deepseek-r1-distill-llama-70b')
prompt = ChatPromptTemplate.from_template(
    """
    Your a Chatbot assitant. which help with the queries regarding langsmith.
    Answer the questions based on the provided context only.
    Please provide the most accurate respone based on question.
    if you don't know the answer please say 'I don't know.'
    <context>
    {context}
    </context>
    Question: {input}

"""
)

document_chain = create_stuff_documents_chain(llm, prompt)
retriver = st.session_state.vectors.as_retriever( search_type="mmr",search_kwargs={"k": 3, "lambda_mult": 0.7})
retrival_chain = create_retrieval_chain(retriver, document_chain)

user_input = st.text_input('Input your prompt here')

if user_input:
    start_time = time.process_time()
    response = retrival_chain.invoke({'input': user_input})
    print(f'time taken for response: {time.process_time()-start_time}')
    st.write(response['answer'])

    # with streamlit expander
    with st.expander('Document similarity search'):
        print(response.keys())
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write('------------')



