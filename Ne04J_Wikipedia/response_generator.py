# response_generator.py
from typing import List
from langchain.text_splitter import TokenTextSplitter

class ResponseGenerator:
    # def generate_response(self, question: str, context: List[str]) -> str:
    #     combined_context = " ".join(context)
    #     response = f"Generated answer based on context: {combined_context}"
    #     documents = self.split_text_document(combined_context)
    #     return documents

    # def split_text_document(self, combined_context: str) -> List[str]:
    #     text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
    #     documents = text_splitter.split_documents([combined_context])
    #     return documents


    def split_text_document(self, question: str, context: List[str]) -> List[str]:
        text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
        documents = text_splitter.split_documents([question])
        return documents