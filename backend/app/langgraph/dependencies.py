from dataclasses import dataclass

from app.services.retrieval_service import RetrievalService
from app.services.generation_service import GenerationService
from app.evaluation.evaluation_service import EvaluationService
from app.services.critic_service import CriticService
from app.services.query_rewriter_service import QueryRewriterService
from app.services.answer_selector_service import AnswerSelectorService
from app.services.planner_service import PlannerService
from app.services.reflection_service import ReflectionService
from app.observability.tracing import TracingContext


@dataclass
class SentinelContext:
    planner: PlannerService
    retrieval: RetrievalService
    generation: GenerationService
    evaluation: EvaluationService
    critic: CriticService
    rewriter: QueryRewriterService
    selector: AnswerSelectorService
    reflection: ReflectionService
    
    tracing: TracingContext