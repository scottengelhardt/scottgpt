import os

import pinecone
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

load_dotenv() # load .env file

# load pinecone
pinecone.init(      
	api_key=os.getenv('PINECONE_API_KEY'),      
	environment='us-west1-gcp-free'      
)      

# 1. Load and Vectorise the data
embeddings = OpenAIEmbeddings()

index_name = os.getenv('PINECONE_INDEX')
src = "./docs"

if index_name in pinecone.list_indexes():
    # load documents
    loader = DirectoryLoader(src, glob="*.*", use_multithreading=True)
    docs = loader.load()
    # create vector database
    Pinecone.from_documents(docs, embeddings, index_name=index_name)

    # Move loaded file from to_upload to uploaded
    for f in os.listdir(src):
        src_path = os.path.join(src, f)
    print(f'🔥 data uploaded to {index_name} index')
else:
    print(f'❌ {index_name} index not found')