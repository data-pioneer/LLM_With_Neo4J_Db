# retrieval.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars


class DataRetriever:
    def __init__(self, graph, llm_transformer):
        self.graph = graph
        self.llm_transformer = llm_transformer

    def retrieve_data(self, query: str):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_index = Neo4jVector.from_existing_graph(
            embeddings,
            search_type="hybrid",
            node_label="Document",
            text_node_properties=["text"],
            embedding_node_property="embedding"
        )
        
        print(f"Search query: {query}")
        structured_data = self.structured_retriever(query)
        unstructured_data = [el.page_content for el in vector_index.similarity_search(query)]
        final_data = f"""Structured data:
        {structured_data}
        Unstructured data:
        {"#Document ". join(unstructured_data)}
        """
        return final_data

    # Full-text index query
    def structured_retriever(self, question: str) -> str:
        # Ensure the full-text index exists before running queries
        self.ensure_fulltext_index()

        # Extract entities from text
        class Entities(BaseModel):
            """Identifying information about entities."""
            names: List[str] = Field(
                ...,
                description="All the required entities that appear in the text",
            )

        result = ""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are extracting organization and person entities from the text.",
                ),
                (
                    "human",
                    "Use the given format to extract information from the following input: {question}",
                ),
            ]
        )
        entity_chain = prompt | self.llm_transformer.llm.with_structured_output(Entities)
        entities = entity_chain.invoke({"question": question})

        for entity in entities.names:
            try:
                response = self.graph.query(
                    """
                    CALL db.index.fulltext.queryNodes('entity', $query, {limit: 2})
                    YIELD node, score
                    CALL {
                      WITH node
                      MATCH (node)-[r]->(neighbor)
                      RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
                      UNION ALL
                      WITH node
                      MATCH (node)<-[r]-(neighbor)
                      RETURN neighbor.id + ' - ' + type(r) + ' -> ' + node.id AS output
                    }
                    RETURN output LIMIT 50
                    """,
                    {"query": generate_full_text_query(entity)},
                )
                result += "\n".join([el['output'] for el in response])
            except:
                print(f"Query error:")

        return result

    def ensure_fulltext_index(self):
        # Check and create the full-text index if it does not exist
        try:
            indexes = self.graph.query("CALL db.indexes YIELD name RETURN name").values()
            index_names = [index[0] for index in indexes]

            if 'entity' not in index_names:
                self.graph.query(
                    """
                    CALL db.index.fulltext.createNodeIndex(
                        'entity',
                        ['Page', 'Section'],
                        ['title', 'text']
                    )
                    """
                )
                print("Full-text index 'entity' created successfully.")
            else:
                print("Full-text index 'entity' already exists.")
        except:
            print(f"Error ensuring index")

# Helper function to generate a full-text query
def generate_full_text_query(input: str) -> str:
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    return full_text_query.strip()
