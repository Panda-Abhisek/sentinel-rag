from typing import Optional

import logging
import time

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore

from app.core.config import settings
from app.embeddings.embedding_model import get_bge_embeddings


logger = logging.getLogger(__name__)


class QdrantService:

    def __init__(
        self,
        url: str = settings.QDRANT_URL,
        api_key: Optional[str] = None,
    ):
        self.url = url
        self.api_key = api_key
        self.vector_store = None
        self.vector_store: Optional[QdrantVectorStore] = None

    def _get_vector_store(self) -> QdrantVectorStore:
        if self.vector_store is None:
            self.vector_store = QdrantVectorStore.from_existing_collection(
                url=self.url,
                api_key=self.api_key,
                collection_name=settings.QDRANT_COLLECTION,
                embedding=get_bge_embeddings(),
            )
        return self.vector_store

    def store_documents(
        self,
        documents: list[Document],
        embeddings: Embeddings,
        collection_name: str = settings.QDRANT_COLLECTION,
        recreate_collection: bool = False,
    ) -> None:

        start = time.perf_counter()
        logger.info("Entering QdrantService.store_documents | chunks=%d | collection=%s", len(documents), collection_name)

        try:
            QdrantVectorStore.from_documents(
                documents=documents,
                embedding=embeddings,
                url=self.url,
                api_key=self.api_key,
                collection_name=collection_name,
                force_recreate=recreate_collection,
            )

            logger.info("Exiting QdrantService.store_documents | duration_ms=%.2f | chunks=%d", (time.perf_counter() - start) * 1000, len(documents))

        except Exception:
            logger.exception("Failed to store documents in Qdrant.")
            raise


    def search(self, query: str, top_k: int = 5) -> list[tuple[Document, float]]:

        start = time.perf_counter()
        logger.info("Entering QdrantService.search | collection=%s | top_k=%d", settings.QDRANT_COLLECTION, top_k)

        try:
            documents = self._get_vector_store().similarity_search_with_score(
                query=query,
                k=top_k,
            )

            logger.info("Exiting QdrantService.search | duration_ms=%.2f | docs=%d", (time.perf_counter() - start) * 1000, len(documents))

            return documents

        except Exception:
            logger.exception("Failed to search Qdrant.")
            raise
