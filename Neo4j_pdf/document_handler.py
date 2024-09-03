from langchain_community.document_loaders import PyPDFLoader
from neo4j_handler import Neo4jHandler

def process_uploaded_pdfs(uploaded_files, neo4j_handler):
    documents = []
    for uploaded_file in uploaded_files:
        temppdf = f"./temp.pdf"
        with open(temppdf, "wb") as file:
            file.write(uploaded_file.getvalue())
        
        loader = PyPDFLoader(temppdf)
        docs = loader.load()
        documents.extend(docs)
        
        # Store document content in Neo4j
        for doc in docs:
            neo4j_handler.add_document(file_name=uploaded_file.name, content=doc.page_content)
    
    return documents
