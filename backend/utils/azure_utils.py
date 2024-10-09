import os
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI
from dotenv import load_dotenv
import json
import numpy as np
load_dotenv()  # Load variables from .env file

def get_azure_blob_client():
    connection_string = str(os.getenv("BLOB_CONNECTION_STRING"))
    return BlobServiceClient.from_connection_string(connection_string)

def get_blob_container_client(container_name, blob_service_client):
    # get the container client
    return blob_service_client.get_container_client(container_name)

def list_blob_containers():
    blob_service_client = get_azure_blob_client()
    # List all containers in the storage account
    containers = blob_service_client.list_containers()
    for container in containers:
        print(container['name'])
def upload_to_blob(local_file_path,container_name):
    # get the blob client
    blob_service_client = get_azure_blob_client()
    # get the container client
    container_client = get_blob_container_client(container_name=container_name,blob_service_client=blob_service_client)
    # local_file_path = "docs/test_ima_1.pdf"
    #get the filename
    blob_name = os.path.basename(local_file_path)
    # uplaod
    with open(local_file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"Uploaded {blob_name} to {container_name}")

def get_embedding_model_client():
    # Azure OpenAI credentials
    ada_endpoint = str(os.getenv("ADA_ENDPOINT"))
    ada_key = str(os.getenv("ADA_KEY"))
    # Initialize Azure OpenAI client
    return AzureOpenAI(
        azure_endpoint=ada_endpoint,
        api_key=ada_key,
        api_version="2023-05-15"
    )
def create_embeddings(text, max_tokens=8191):
    ada_deployment = "text-embedding-ada-002"
    
    # Split the text into chunks if it exceeds the max token limit
    chunks = [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]
    openai_client = get_embedding_model_client()
    embeddings = []
    for chunk in chunks:
        response = openai_client.embeddings.create(
            input=chunk,
            model=ada_deployment
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)
    
    # If there are multiple chunks, average the embeddings
    if len(embeddings) > 1:
        return np.mean(embeddings, axis=0).tolist()
    else:
        return embeddings[0]
    
def get_ai_search_client():
    # Initialize Search client
    admin_key = str(os.getenv("AI_SEARCH_KEY"))
    endpoint = str(os.getenv("AI_SEARCH_ENDPOINT"))
    index_name = 'legal-docs'
    return SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(admin_key))

def search_vector_index(query,doc_id=2):
    embedding  = create_embeddings(query)
    vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=3, fields="titleVector")
    search_client = get_ai_search_client()
    # Create a filter to restrict search to a specific document ID
    # Corrected filter expression
    # filter_expression = f"id eq '{doc_id}' or id startswith '{doc_id}-chunk-'"
    #perform vector search
    return search_client.search(  
        search_text=query,  
        vector_queries= [vector_query],
        select=["title", "content", "category","link"],
        # filter=filter_expression
    )  

def get_gpt4o_client():
    # Azure OpenAI credentials
    gpt4o_endpoint = os.getenv("GPT4O_ENDPOINT")
    gpt4o_key = os.getenv("GPT4O_KEY")
    deployment_name = "gpt-4o"
    
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=gpt4o_key,
        api_version="2023-05-15",
        azure_endpoint=gpt4o_endpoint
    )
    
    return client, deployment_name
def get_relevant_context(query):
    # Perform vector search
    results = search_vector_index(query)
    # Extract and return relevant context as JSON objects
    context = [
        {
            "title": result['title'],
            "category": result['category'],
            "content": result['content'],
            "link": result['link']
        } for result in results
    ]
    return context
def generate_response(query, context, conversation_history):
    context_str = json.dumps(context, indent=2)
    
    # Prepare the conversation history
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    
    prompt = f"""Use the following information to answer the user's question. 
    If the information doesn't contain the answer, say you don't know.

    Context (JSON format):
    {context_str}

    Conversation History:
    {history_str}

    User's question: {query}

    Provide a concise answer based on the given context and conversation history. 
    If relevant, mention which document(s) (by title or category) the information comes from and cite the link as well.
    Cite the actual words from the document as well.
    """
    
    openai_client, deployment_name = get_gpt4o_client()
    response = openai_client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content