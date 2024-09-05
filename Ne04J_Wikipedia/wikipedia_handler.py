# wikipedia_handler.py
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document

class WikipediaHandler:
    def fetch_page(self, title: str) -> list[Document]:
        raw_documents = WikipediaLoader(query=title).load()
        return raw_documents

    def preprocess_text(self, documents: list[Document]) -> list[Document]:
        text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
        return text_splitter.split_documents(documents[:1])
