from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

_embeddings = None

def get_bge_embeddings(device: str = "cpu") -> HuggingFaceEmbeddings:
    """
    Initializes and returns the BAAI/bge-small-en-v1.5 embedding model.
    Optimized with embedding normalization for optimal retrieval accuracy.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True}
        )
    return _embeddings
