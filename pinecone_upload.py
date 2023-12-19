import os
import shutil

import pinecone
import streamlit as st
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

# load pinecone
pinecone.init(      
	api_key=st.secrets['PINECONE_API_KEY'],
	environment='us-west1-gcp-free'      
)      

# Load and Vectorise the data
embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])

index_name = st.secrets['PINECONE_INDEX']

src = "./to_upload"
dest = "./uploaded"

if index_name in pinecone.list_indexes():
    # load documents
    loader = DirectoryLoader(src, glob="*.*", use_multithreading=True)
    docs = loader.load()
    # create vector database
    Pinecone.from_documents(docs, embeddings, index_name=index_name)

     # Move loaded file from to_upload to uploaded
    for f in os.listdir(src):
        src_path = os.path.join(src, f)
        dest_path = os.path.join(dest, f)
        shutil.move(src_path, dest_path)
    print(f'🔥 data uploaded to {index_name} index')
else:
    print(f'❌ {index_name} index not found')