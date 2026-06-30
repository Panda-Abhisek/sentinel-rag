from app.evaluation.answer_evaluator import AnswerEvaluator
from app.evaluation.evaluation_service import EvaluationService
from app.evaluation.retrieval_evaluator import RetrievalEvaluator
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.vectorstore.qdrant_client import QdrantService


qdrant_service = QdrantService()

llm_service = LLMService()

retrieval_evaluator = RetrievalEvaluator()

answer_evaluator = AnswerEvaluator()

evaluation_service = EvaluationService(
    retrieval_evaluator=retrieval_evaluator,
    answer_evaluator=answer_evaluator,
)

retrieval_service = RetrievalService(
    qdrant_service=qdrant_service,
    llm_service=llm_service,
    evaluation_service=evaluation_service,
)


def get_retrieval_service() -> RetrievalService:
    return retrieval_service