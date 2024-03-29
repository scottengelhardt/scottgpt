import webbrowser

import pinecone
import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from streamlit.components.v1 import html


# Do similarity search and send response
def generate_response(message):
    similar_response = st.session_state.db.similarity_search(
        message
    )  # do a similarity search in our database for a matching vector
    data = [
        doc.page_content for doc in similar_response
    ]  # get the contents of the vector
    response = st.session_state.chain.run(
        message=message, data=data, history=st.session_state.history
    )  # send the message and relevant data to our llm
    return response.replace("$", "\$")  # annoying streamlit formatting


def main():
    # load pinecone
    pinecone.init(
        api_key=st.secrets["PINECONE_API_KEY"], environment="us-west1-gcp-free"
    )

    # Create memory store
    # https://discuss.streamlit.io/t/how-can-i-store-data-into-variables/38350/4
    if "history" not in st.session_state:
        st.session_state.history = []
        st.session_state.history.append(
            {
                "role": "bot",
                "content": "Hello! I am an AI chatbot trained on Scott's professional life. You can ask me anything about his work, background, or education. Enjoy!",
            }
        )

    if "embeddings" not in st.session_state:
        # Load the data from Pinecone
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.db = Pinecone.from_existing_index(
            "scott", st.session_state.embeddings
        )

        # Setup LLMChain and prompt template
        st.session_state.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k", openai_api_key=st.secrets["OPENAI_API_KEY"])

        st.session_state.template = """
        You, referred to in history as 'bot', are a world class conversational chat bot whose goal is to answer questions about Scott and help him get hired. 
        I will share a users's message with you and you will give me a clear answer that should follow these rules:
            1. The response should pertain only to the data provided below.
            2. If the question appears to be missing context or subject matter, use the the provided history to infer context. Start searching from back to front. 
            3. If there is relevant information in the history, you should provide it in the context of the most recent historic message.
            4. If the message from the user says "You" or "Your" it should be intepretted as referring to Scott.
            5. If a response is not found in the information or history provided below, respond "I don't know the answer to that. You can email Scott at scott_engelhardt@outlook.com to ask him directly." 

        Here is the chat history:
        {history}

        Below is a message I received from the user:
        {message}

        Here is the relevant information:
        {data}

        Provide me with a response to their prompt.
        """

        st.session_state.prompt = PromptTemplate(
            input_variables=["history", "message", "data"],
            template=st.session_state.template,
        )
        st.session_state.chain = LLMChain(
            llm=st.session_state.llm, prompt=st.session_state.prompt
        )

    # Build an app with streamlit
    st.set_page_config(page_title="ScottBot", page_icon=":zap:")

    st.header("ScottBot :zap:")

    col1, col2, col3, *_ = st.columns(3)
    with col1:
         if st.button("Open My Resume"):
            open_page("https://github.com/scottengelhardt/scottgpt/blob/dc87c1b12f559e12dfe6029e009eb4f7f9fb5ed8/resume.pdf")
    with col2:
        if st.button("My Interactive Intro"):
            open_page("https://share.mindstamp.com/w/RgoLuuzfyGFi?from=streamlit")
    with col3:
        if st.button("Send Me an Email"):
            open_page("mailto:scott_engelhardt@outlook.com")

    # show previous messages
    for message in st.session_state.history:
        avatar = "👨" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # get new input and response from llm
    user_input = st.chat_input(placeholder="What can I answer for you?")
    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        st.chat_message("user", avatar="👨").markdown(user_input)
        response = generate_response(user_input)
        st.session_state.history.append({"role": "bot", "content": response})
        st.chat_message("assistant", avatar="🤖").markdown(response)


def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script, height=0,width=0)


if __name__ == "__main__":
    main()
