# app/vectorstore/qdrant_client.py

from typing import Optional

import logging

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore

from app.core.config import settings
from app.embeddings.embedding_model import get_bge_embeddings

logger = logging.getLogger(__name__)


class QdrantService:
    """
    Handles all interactions with the Qdrant vector database.

    Responsibilities:
    - Store document embeddings
    - Retrieve documents
    - Delete collections (later)
    - Manage collections (later)
    """

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
        """
        Stores document embeddings inside a Qdrant collection.

        Args:
            documents: List of LangChain Document objects.
            embeddings: Embedding model instance.
            collection_name: Target Qdrant collection.
            recreate_collection: Recreate collection if it already exists.
        """

        logger.info(
            f"Storing {len(documents)} chunks into collection '{collection_name}'..."
        )

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
                f"Successfully stored {len(documents)} chunks in '{collection_name}'."
            )

        except Exception:
            logger.exception("Failed to store documents in Qdrant.")
            raise
        
        
    def search(self, query: str, top_k: int = 5) -> list[tuple[Document, float]]:
        """
        Retrieves the most relevant documents from Qdrant.
        """

        try:
            documents = self._get_vector_store().similarity_search_with_score(
                query=query,
                k=top_k,
            )
            logger.info(
                "Searching collection '%s'.",
                settings.QDRANT_COLLECTION,
            )
            
            logger.info(
                "Retrieved %d documents.",
                len(documents),
            )

            return documents

        except Exception:
            logger.exception("Failed to search Qdrant.")
            raise   
