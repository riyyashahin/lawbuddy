import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
#faiss runs locally. we can store in our own machine instead of cloud

def get_pdf_text(pdf_docs) :
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def load_law_book_data():
    with open("ipc.pdf", "rb") as ipc_file, open("constitution_of_india.pdf", "rb") as const_file:
        text = get_pdf_text([ipc_file, const_file])
    
    text_chunks = get_text_chunks(text)
    vectorstore = get_vectorstore(text_chunks)
    return get_conversation_chain(vectorstore)


def get_text_chunks(text) :
    text_splitter = CharacterTextSplitter(
        separator="\n",chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks) :
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore) :
    llm = ChatOpenAI()
    # chatbot that has memory - so initialise a instance of memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    # initialise the session
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain

def handle_userinput(user_question) :
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response['chat_history']

    # for i, message in enumerate(st.session_state.chat_history):
    #     if i % 2 == 0:
    #         st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    #     else:
    #         st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    

    


def main() :

    import os
    from dotenv import load_dotenv
    load_dotenv()
    print("DEBUG - API Key:", os.getenv("OPENAI_API_KEY"))
    st.set_page_config(page_title="Chat with Indian Law", page_icon="⚖️")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state :
        with st.spinner("Loading Indian Law Book..."):
            st.session_state.conversation = load_law_book_data()
    if "chat_history" not in st.session_state :
        st.session_state.chat_history = []

    st.header("Chat with Indian Law ⚖️ ")

    with st.form(key="qa form", clear_on_submit=True):
        user_question = st.text_input("Ask a question about Indian Law:", key="user_input")
        submitted = st.form_submit_button("Ask")

    if submitted and user_question:
        handle_userinput(user_question)

    if st.session_state.chat_history:
        for message in reversed(st.session_state.chat_history):
            if message.type == "human":
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    
    # user_question = st.text_input("Ask a question about Indian Law:", key="user_input")
    # if user_question:
    #     handle_userinput(user_question)
    #     user_question = ""

    

    
if __name__ == '__main__':
    main()