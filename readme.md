# Scott's Bot 🤖
### Custom LLM on Trained Data

## Requirements
  - Python 3.9+
  - OpenAI Account
  - Pinecone Account

## Dependencies
  - Python Packages
     - `pip3 install langchain openai tiktoken pinecone-client streamlit`
  - OpenAI ChatGPT-3.5 
     - ChatGPT-4 can be used but there are limits to the number of queries that can be run per hour
     - It is recommended to us the 16k token version for longer queries and data loads
  - Pinecone
     - Pinecone is a vector storage database that will store the information loaded to the OpenAI model.
     - They do a better job of explaing than me. https://docs.pinecone.io/docs/overview
  
## Setup Data in Pinecone
  1. After you have an OpenAI and Pinecone account, both API keeps need to be stored in `./.streamlit/secrets.toml` along with the name of your Pinecone Index.
  2. Gather data from website, internal sources, etc. and place them in `./to_upload` as .txt files
  3. Run `pinecone_create.py` to create your pinecone index
     - `python3 pinecone_create.py`
     - This will create a simple index on the free plan. If you have a paid plan and want a more customized index, do so on Pinecone
  4. Once the index has been created and is fully setup (green status in Pinecone), upload your data to Pinecone by running  `pinecone_upload.py`
  5. Once your data is loaded to Pinecone, you should see the number of vectors in Pinecone is no longer 0 and your files moved from `./to_upload` to `./uploaded`.
  6. If you need to add data to your Pinecone index, add additional files to `./to_upload` and run `pinecone_upload.py` 
  7. If you need to delete any of your pinecone data (i.e. if you want to reupload an updated file), you can go into Pinecone and delete the vector(s) that have the relevant information, then follow step 6 to read your data. 
  8. If you need to delete all your pinecone data run `pinecone_delete.py` and then start back at step 2.
     - `python3 pinecone_delete.py`

## Run the Streamlit Web App
  ### This will run a basic Q&A bot via a local web page
  1. Setup your data in Pinecone
  2. Run `app.py` to run the web version of this application
     - `python3 -m streamlit run app.py`

## Fine Tuning
  The model is only as good as the data it receives. The more comprehensive and informative the data you upload to Pinecone, the better responses you will receive. It is recommended to format your data in a way that is concise and includes relevant information close to other information in proximity. Data can be uploaded to pinecone as an entire document or in smaller chunks. There are pros and cons to each. With the entire document loaded into one vector, you can send more info to ChatGPT and get more detailed (and potentially accurate) responses but your prompt will be longer making it more expensive. With chunked data, you can send smaller amounts of data from pinecone, however, this data may be incomplete and result in an answer that doesn't capture all available information. This will be cheaper however since not all data is included in the prompt and will use less tokens. My recommendation is format your data into concise files where all relevant information is contained and upload entire documents to Pincone. Pricing is very cheap and by limiting the size of your files, you can reduce costs.
  
  Another aspect that can be fine tuned is the prompt that is sent to the LLM. The prompt can be found in `app.py`. Here you want to be a structured as possible. You want to include rules on how to respond (format, tone, length, etc). The prompt will use tokens, so you want to limit it to an extent, but think of it as detailed instructions on how the model should respond. In my prompt, I include sections for: 
     - Instructions/Rules: telling the model how you want it to respond and handle different scenarios
     - History: a history of previous questions and responses. This is used to make the LLM conversational by being able to reference previous questions and responses.
     - Message: the Message from the user
     - Data: the data (vector) from pinecone that is relevant to the question at hand.


## Resources
  - Overview of vectors, embedding, and using them with ChatGPT
     - https://youtu.be/c_nCjlSB1Zk?si=3hbPQiuT5MPIsa-c
  - Pinecone Docs
     - https://docs.pinecone.io/docs/overview