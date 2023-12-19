import pinecone
import streamlit as st

# load pinecone
pinecone.init(      
	api_key=st.secrets['PINECONE_API_KEY'],      
	environment='us-west1-gcp-free'      
)      

index_name = st.secrets['PINECONE_INDEX']

if index_name in pinecone.list_indexes():
    pinecone.delete_index(index_name)
    print(f'🔥 deleted {index_name} index')
else:
    print(f'❌ {index_name} index not found')