from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
_embeddings = None

def get_bge_embeddings() -> HuggingFaceEmbeddings:
    """
    Initializes and returns the BAAI/bge-small-en-v1.5 embedding model.
    Optimized with embedding normalization for optimal retrieval accuracy.
    """
    global _embeddings
    if _embeddings is None:
        logger.info("Initializing embedding model...")
        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': settings.EMBEDDING_DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )
    else:
        logger.info("Using cached embedding model.")
    return _embeddings
