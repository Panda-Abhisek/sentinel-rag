from typing import Literal, TypedDict
from langchain_core.documents import Document

from app.evaluation.models import EvaluationReport
from app.langgraph.models import ReflectionReport


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
    
    retry_count: int
    max_retries: int
    
    critic_reason: str
    
    planner_route: Literal["retrieve", "rewrite"]
    critic_route: Literal["rewrite", "finish"]
    
    rewritten_query: str | None
    planner_reason: str
    
    candidate_answers: list[str]
    candidate_evaluations: list[EvaluationReport]
    selected_answer_index: int
    
    reflection: ReflectionReport | None