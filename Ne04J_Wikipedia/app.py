# app.py
import streamlit as st
from configuration import load_environment_variables
from database import Neo4jDatabase
from transformer import LLMTransformer
from datastore import DataStore
from retrieval import DataRetriever
from wikipedia_handler import WikipediaHandler
from response_generator import ResponseGenerator
from utility import generate_full_text_query

from langchain_community.graphs import Neo4jGraph
# Load environment variables
env = load_environment_variables()

# Initialize modules
db = Neo4jDatabase(uri=env["NEO4J_URI"], user=env["NEO4J_USERNAME"], password=env["NEO4J_PASSWORD"])
llm_transformer = LLMTransformer(groq_api_key=env["GROQ_API_KEY"])
graph = Neo4jGraph()
data_store = DataStore(graph, llm_transformer)
data_retriever = DataRetriever(graph, llm_transformer)
wiki_handler = WikipediaHandler()

response_generator = ResponseGenerator()

# Streamlit UI
st.title("Knowledge Graph with Neo4j and LLM")

# Fetch and process Wikipedia page
wiki_title = st.text_input("Enter Wikipedia Page Title:")
if st.button("Fetch and Store"):
    if wiki_title:
        raw_documents = wiki_handler.fetch_page(wiki_title)
        processed_documents = wiki_handler.preprocess_text(raw_documents)
        data_store.store_data(wiki_title, processed_documents)
        st.success("Data stored successfully!")


# Query the knowledge graph
query = st.text_input("Enter Query:")
if st.button("Retrieve Data"):
    if query:
        entities = data_retriever.retrieve_data(query)
        st.write("Entities Found:", entities)
