from typing import Literal, TypedDict
from langchain_core.documents import Document

from app.evaluation.models import EvaluationReport


class SentinelState(TypedDict):
    # Input
    query: str
    top_k: int

    # Retrieval
    retrieved_documents: list[tuple[Document, float]]

    # Generation
    answer: str | None

    # Evaluation
    evaluation: EvaluationReport | None

    # Timing
    retrieval_ms: float
    generation_ms: float
    evaluation_ms: float
    total_ms: float
    
    route: Literal["retrieve", "rewrite"]
    planner_reason: str