import streamlit as st
from langchain_groq import ChatGroq
from rag_chain import setup_rag_chain
from document_handler import process_uploaded_pdfs
from embedding_store import get_embeddings, create_vectorstore
from chat_manager import get_session_history, store_chat_message
from config import load_config
from neo4j_handler import Neo4jHandler
import os
# Load environment variables
load_config()

# Initialize Neo4j connection
neo4j_handler = Neo4jHandler(uri=os.environ['NEO4J_URI'], user=os.environ['NEO4J_USERNAME'], password=os.environ['NEO4J_PASSWORD'])

# Streamlit interface
st.title("Conversational RAG With PDF uploads and chat history")
st.write("Upload PDFs and chat with their content")

#api_key = st.text_input("Enter your Groq API key:", type="password")
session_id = "default_session" # st.text_input("Session ID", value="default_session")


llm = ChatGroq(groq_api_key=os.environ['GROQ_API_KEY'], model_name="Gemma2-9b-It")
    
if 'store' not in st.session_state:
    st.session_state.store = {}

uploaded_files = st.file_uploader("Choose A PDF file", type="pdf", accept_multiple_files=True)
    
if uploaded_files:
    documents = process_uploaded_pdfs(uploaded_files, neo4j_handler)
    embeddings = get_embeddings()
    retriever = create_vectorstore(documents, embeddings)
        
    rag_chain = setup_rag_chain(llm, retriever)
        
    from langchain_core.runnables.history import RunnableWithMessageHistory
        
    conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            lambda: get_session_history(session_id, st.session_state.store, neo4j_handler),
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

    user_input = st.text_input("Your question:")
        
    if user_input:
        session_history = get_session_history(session_id, st.session_state.store, neo4j_handler)
        response = conversational_rag_chain.invoke({"input": user_input}, config={"configurable": {"session_id": session_id}})
            
        # Store user input and assistant response in Neo4j
        store_chat_message(neo4j_handler, session_id, "human", user_input)
        store_chat_message(neo4j_handler, session_id, "assistant", response['answer'])
            
        st.write("Assistant:", response['answer'])
        st.write("Chat History:", session_history.messages)


# Close Neo4j connection when the app stops
st.session_state['neo4j_handler'] = neo4j_handler
