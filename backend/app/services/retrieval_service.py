import logging
import time

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

        start = time.perf_counter()
        logger.info("Entering RetrievalService.retrieve_documents | top_k=%d | query=%s", top_k, question)

        docs = self.qdrant_service.search(
            query=question,
            top_k=top_k,
        )

        logger.info("Exiting RetrievalService.retrieve_documents | duration_ms=%.2f | docs=%d", (time.perf_counter() - start) * 1000, len(docs))
        return docs
