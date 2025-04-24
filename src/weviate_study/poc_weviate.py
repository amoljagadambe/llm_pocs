import weaviate
from weaviate.classes.init import Auth
import weaviate.classes as wvc
import json
from openai import OpenAI
import dotenv
import requests
import os

dotenv.load_dotenv()
model="text-embedding-ada-002"

def create_connection():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=f'https://{os.getenv("WEAVIATE_URL")}',
        auth_credentials=Auth.api_key(os.getenv('WEAVIATE_API_KEY')),
        headers={
                'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY') # openai api key for vectorizer & generative
            }
    )
    return client


def create_collection(name: str, description: str, db_connection: weaviate.Client):
    
    if db_connection.collections.exists(name):
        # print collection alreday exsists
        print(f"Collection {name} already exists")
        return False
    
    # create collection
    db_connection.collections.create(
        name=name,
        description=description,
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.config.Configure.Generative.openai(),
        properties=[
            wvc.config.Property(name="question", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="answer", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="category", data_type=wvc.config.DataType.TEXT),
        ],
        
        # # Configure the vector index
        # vector_index_config=wvc.config.Configure.VectorIndex.hnsw(  # Or `flat` or `dynamic`
        #     distance_metric=wvc.config.VectorDistances.COSINE,
        #     quantizer=wvc.config.Configure.VectorIndex.Quantizer.bq(),
        # ),
        # # Configure the inverted index
        # inverted_index_config=wvc.config.Configure.inverted_index(
        #     index_null_state=True,
        #     index_property_length=True,
        #     index_timestamps=True,
        # ),
    )
    print(f"Collection {name} created")
    return True


# add data to collection
def fetch_data(url: str):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data

def add_data_to_collection(data: list, collection_name: str, db_connection: weaviate.Client):
    collection_fetch = db_connection.collections.get(collection_name)

    with collection_fetch.batch.dynamic() as batch:
        for item in data:
            batch.add_object({
                'question': item['Question'],
                'answer': item['Answer'],
                'category': item['Category']
            })

            if batch.number_errors > 10:
                print(f'Number of errors: {len(batch.errors)}')
                print(f'Errors: {batch.errors}')

    print(f'Added {len(data)} objects to collection {collection_name}') 


def query_collection(query: str, collection_name: str, db_connection: weaviate.Client):
    collection_name = db_connection.collections.get(collection_name)
    response = collection_name.generate.near_text(query, limit=2, grouped_task="Write a tweet with emojis about these facts.")
    return response

def create_query_embedding(query: str, collection_name: str, db_connection: weaviate.Client):
    '''
    Create a vector embedding for the user query
    Use OpenAI's API to create the embedding, costly operation
    use if you want to use vector search
    '''
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        model=model,
        input=query
    )
    vector = response.data[0].embedding
    collection_name = db_connection.collections.get(collection_name)
    response = collection_name.generate.near_vector(vector, limit=2, grouped_task="Write a tweet with emojis about these facts.")
    return response

def genrate_resonse_using_hybrid_search(query: str, collection_name: str, db_connection: weaviate.Client):  
    collection_name = db_connection.collections.get(collection_name)
    response = collection_name.query.hybrid(query, limit=2)
    return response

with create_connection() as connection:
    '''
    # one time setup
    create_collection('Question', 'Jeopardy Question and Answer', connection)
    data = fetch_data('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    add_data_to_collection(data, 'Question', connection)
    '''

    # query collection
    resoponse = genrate_resonse_using_hybrid_search('carnivorous', 'Question', connection)
    # print(resoponse.generated)
    for obj in resoponse.objects:
        print(json.dumps(obj.properties, indent=2))

