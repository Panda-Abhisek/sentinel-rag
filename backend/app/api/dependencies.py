"""
Dependency providers for SentinelRAG.

This module centralizes construction of application services using
FastAPI's dependency injection system.

Each provider is responsible for creating and returning a single
application component. Higher-level services compose lower-level
dependencies through provider functions rather than relying on module-
level singletons.

This design improves:

- Testability
- Dependency overriding
- Separation of concerns
- Future migration to external DI containers
"""

from functools import lru_cache

from app.evaluation.answer_evaluator import AnswerEvaluator
from app.evaluation.evaluation_service import EvaluationService
from app.evaluation.hallucination_detector import HallucinationDetector
from app.evaluation.retrieval_evaluator import RetrievalEvaluator

from app.healing.answer_selector import AnswerSelector
from app.healing.healing_policy import HealingPolicy
from app.healing.healing_service import HealingService
from app.healing.query_rewriter import QueryRewriter
from app.healing.retry_strategy import RetryStrategy

from app.rag.rewrite_prompt_builder import RewritePromptBuilder

from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService

from app.vectorstore.qdrant_client import QdrantService

from app.langgraph.dependencies import SentinelContext
from app.services.graph_service import GraphService
from app.services.generation_service import GenerationService
from app.services.critic_service import CriticService
from app.services.query_rewriter_service import QueryRewriterService
from app.services.answer_selector_service import AnswerSelectorService
from app.services.planner_service import PlannerService


# ==========================================================
# Infrastructure
# ==========================================================

@lru_cache
def get_qdrant_service() -> QdrantService:
    return QdrantService()


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService()


# ==========================================================
# Evaluation
# ==========================================================

@lru_cache
def get_retrieval_evaluator() -> RetrievalEvaluator:
    return RetrievalEvaluator()


@lru_cache
def get_answer_evaluator() -> AnswerEvaluator:
    return AnswerEvaluator()


@lru_cache
def get_hallucination_detector() -> HallucinationDetector:
    return HallucinationDetector()


@lru_cache
def get_evaluation_service() -> EvaluationService:
    return EvaluationService(
        retrieval_evaluator=get_retrieval_evaluator(),
        answer_evaluator=get_answer_evaluator(),
        hallucination_detector=get_hallucination_detector(),
    )


# ==========================================================
# Retrieval
# ==========================================================

@lru_cache
def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        qdrant_service=get_qdrant_service()
    )


# ==========================================================
# Healing
# ==========================================================

@lru_cache
def get_healing_policy() -> HealingPolicy:
    return HealingPolicy()


@lru_cache
def get_rewrite_prompt_builder() -> RewritePromptBuilder:
    return RewritePromptBuilder()


@lru_cache
def get_query_rewriter() -> QueryRewriter:
    return QueryRewriter(
        llm_service=get_llm_service(),
        prompt_builder=get_rewrite_prompt_builder(),
    )


@lru_cache
def get_retry_strategy() -> RetryStrategy:
    return RetryStrategy(
        query_rewriter=get_query_rewriter(),
    )


@lru_cache
def get_answer_selector() -> AnswerSelector:
    return AnswerSelector()


@lru_cache
def get_healing_service() -> HealingService:
    return HealingService(
        retrieval_service=get_retrieval_service(),
        healing_policy=get_healing_policy(),
        retry_strategy=get_retry_strategy(),
        answer_selector=get_answer_selector(),
    )
    
def get_generation_service() -> GenerationService:
    return GenerationService(
        llm_service=get_llm_service(),
    )


def get_graph_dependencies() -> SentinelContext:
    return SentinelContext(
        planner=get_planner_service(),
        retrieval=get_retrieval_service(),
        generation=get_generation_service(),
        evaluation=get_evaluation_service(),
        critic=get_critic_service(),
        rewriter=get_rewriter_query(),
        selector=get_answer_selector_service()
    )


def get_graph_service() -> GraphService:
    return GraphService(
        dependencies=get_graph_dependencies(),
    )
    
def get_critic_service() -> CriticService:
    return CriticService(
        llm_service=get_llm_service()
    )
    
def get_rewriter_query() -> QueryRewriterService:
    return QueryRewriterService(
        llm_service=get_llm_service()
    )
    
def get_answer_selector_service() -> AnswerSelectorService:
    return AnswerSelectorService()

def get_planner_service() -> PlannerService:
    return PlannerService(
        llm_service=get_llm_service()
    )