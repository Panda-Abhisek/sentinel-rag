from typing import Optional

import logging

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore

from app.core.config import settings
from app.embeddings.embedding_model import get_bge_embeddings
from app.core.logging_config import LogUtils

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

        LogUtils.entry(logger, "QdrantService.store_documents", chunks=len(documents), collection=collection_name)

        try:
            QdrantVectorStore.from_documents(
                documents=documents,
                embedding=embeddings,
                url=self.url,
                api_key=self.api_key,
                collection_name=collection_name,
                force_recreate=recreate_collection,
            )

            logger.info(
                "Successfully stored %d chunks in '%s'.",
                len(documents),
                collection_name,
            )

        except Exception:
            logger.exception("Failed to store documents in Qdrant.")
            raise


    def search(self, query: str, top_k: int = 5) -> list[tuple[Document, float]]:

        try:
            documents = self._get_vector_store().similarity_search_with_score(
                query=query,
                k=top_k,
            )

            logger.info(
                "Retrieved %d documents from collection '%s'.",
                len(documents),
                settings.QDRANT_COLLECTION,
            )

            return documents

        except Exception:
            logger.exception("Failed to search Qdrant.")
            raise
