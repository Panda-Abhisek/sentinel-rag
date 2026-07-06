from dataclasses import dataclass

from app.services.retrieval_service import RetrievalService
from app.services.generation_service import GenerationService
from app.evaluation.evaluation_service import EvaluationService
from app.services.critic_service import CriticService
from app.services.query_rewriter_service import QueryRewriterService


@dataclass
class SentinelContext:
    retrieval: RetrievalService
    generation: GenerationService
    evaluation: EvaluationService
    critic: CriticService
    rewriter: QueryRewriterService