import os

import pinecone
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

load_dotenv() # load .env file

# load pinecone
pinecone.init(      
	api_key=os.getenv('PINECONE_API_KEY'),      
	environment='us-west1-gcp-free'      
)      

index_name = os.getenv('PINECONE_INDEX')

if index_name in pinecone.list_indexes():
    pinecone.delete_index(index_name)
    print(f'🔥 deleted {index_name} index')
else:
    print(f'❌ {index_name} index not found')