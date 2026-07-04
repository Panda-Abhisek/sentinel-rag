import logging
from langchain_core.documents import Document
from app.vectorstore.qdrant_client import QdrantService

logger = logging.getLogger(__name__)

class RetrievalService:

    def __init__(self, qdrant_service: QdrantService):
        self.qdrant_service = qdrant_service

    def retrieve_documents(
        self,
        question: str,
        top_k: int,
    ) -> list[tuple[Document, float]]:

        return self.qdrant_service.search(
            query=question,
            top_k=top_k,
        )