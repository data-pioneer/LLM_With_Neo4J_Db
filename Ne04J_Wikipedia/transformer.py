# transformer.py
from langchain_groq import ChatGroq
from langchain_experimental.graph_transformers import LLMGraphTransformer

class LLMTransformer:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(groq_api_key=groq_api_key, model="Llama3-8b-8192")
        self.llm_transformer = LLMGraphTransformer(llm=self.llm)

    def convert_to_graph_documents(self, content):
        return self.llm_transformer.convert_to_graph_documents(content)
