# datastore.py
from langchain_community.graphs import Neo4jGraph

class DataStore:
    def __init__(self, graph: Neo4jGraph, llm_transformer):
        self.graph = graph
        self.llm_transformer = llm_transformer

    def store_data(self, title: str, content):
        graph_documents = self.llm_transformer.convert_to_graph_documents(content)
        self.graph.add_graph_documents(
            graph_documents,
            baseEntityLabel=True,
            include_source=True
        )
