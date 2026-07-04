from dataclasses import dataclass

from app.services.retrieval_service import RetrievalService
from app.services.generation_service import GenerationService
from app.evaluation.evaluation_service import EvaluationService


@dataclass
class SentinelContext:
    retrieval: RetrievalService
    generation: GenerationService
    evaluation: EvaluationService