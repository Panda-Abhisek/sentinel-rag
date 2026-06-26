# app/vectorstore/qdrant_client.py

from typing import Optional

import logging

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore

from app.core.config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """
    Handles all interactions with the Qdrant vector database.

    Responsibilities:
    - Store document embeddings
    - Retrieve documents (later)
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