from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.vectorstore.qdrant_client import QdrantService

qdrant_service: QdrantService = QdrantService()

llm_service: LLMService = LLMService()

retrieval_service: RetrievalService = RetrievalService(
    qdrant_service=qdrant_service,
    llm_service=llm_service,
)

def get_retrieval_service() -> RetrievalService:
    return retrieval_service