import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from app.core.logging_config import LogUtils
from app.services.document_loader import get_document_loader
from app.services.text_splitter import get_character_text_splitter
from app.embeddings.embedding_model import get_bge_embeddings
from app.vectorstore.qdrant_client import QdrantService
from app.schemas.index import IndexResult
from app.core.config import settings

logger = logging.getLogger(__name__)

class IndexService:

    @staticmethod
    def process_and_index_pdf(
        file_path: str,
        original_filename: str,
        collection_name: str = settings.QDRANT_COLLECTION,
        qdrant_url: str = settings.QDRANT_URL,
        qdrant_api_key: Optional[str] = None
    ) -> IndexResult:

        start = time.perf_counter()
        LogUtils.entry(logger, "IndexService.process_and_index_pdf", file=original_filename)

        logger.info("Step 1/4: Loading document: %s", file_path)
        loader = get_document_loader(file_path)

        try:
            raw_documents = loader.load()
        except Exception:
            logger.exception("Failed to load PDF")
            raise

        logger.info("Step 2/4: Chunking document content...")
        splitter = get_character_text_splitter()
        chunked_documents = splitter.split_documents(raw_documents)

        path = Path(file_path)
        for index, chunk in enumerate(chunked_documents):
            chunk.metadata["filename"] = original_filename
            chunk.metadata["document_name"] = path.stem
            chunk.metadata["indexed_at"] = datetime.now(timezone.utc).isoformat()
            chunk.metadata["project"] = settings.PROJECT_NAME
            chunk.metadata["chunk_id"] = index

        logger.info("Step 3/4: Preparing embedding service...")
        embeddings_model = get_bge_embeddings()

        logger.info("Step 4/4: Generating vectors and uploading to Qdrant collection '%s'...", collection_name)
        qdrant_service = QdrantService(
            url=qdrant_url,
            api_key=qdrant_api_key
        )

        qdrant_service.store_documents(
            documents=chunked_documents,
            embeddings=embeddings_model,
            collection_name=collection_name,
        )

        LogUtils.exit(logger, "IndexService.process_and_index_pdf", start, chunks=len(chunked_documents))

        return IndexResult(
            status="success",
            filename=original_filename,
            collection=collection_name,
            chunks=len(chunked_documents),
        )
