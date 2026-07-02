"""
Integration tests for the self-healing pipeline.
"""

from unittest.mock import AsyncMock

import pytest

from app.healing.answer_selector import AnswerSelector
from app.healing.healing_policy import HealingPolicy
from app.healing.healing_service import HealingService
from app.healing.retry_strategy import RetryStrategy
from app.healing.query_rewriter import QueryRewriter
from app.services.retrieval_service import RetrievalService

from tests.factories import query_response_factory

@pytest.fixture
def retrieval_service():
    return AsyncMock(spec=RetrievalService)


@pytest.fixture
def llm_service():
    return AsyncMock()


@pytest.fixture
def prompt_builder():
    class FakePromptBuilder:

        def build(self, query: str) -> str:
            return f"Rewrite: {query}"

    return FakePromptBuilder()


@pytest.fixture
def query_rewriter(
    llm_service,
    prompt_builder,
):
    return QueryRewriter(
        llm_service=llm_service,
        prompt_builder=prompt_builder,
    )


@pytest.fixture
def retry_strategy(
    query_rewriter,
):
    return RetryStrategy(
        query_rewriter=query_rewriter,
    )


@pytest.fixture
def healing_service(
    retrieval_service,
    retry_strategy,
):
    return HealingService(
        retrieval_service=retrieval_service,
        healing_policy=HealingPolicy(),
        retry_strategy=retry_strategy,
        answer_selector=AnswerSelector(),
    )
    
    
@pytest.mark.asyncio
async def test_pipeline_without_retry(
    healing_service,
    retrieval_service,
):
    """
    High-quality answers should bypass healing.
    """

    response = query_response_factory(
        retrieval_confidence=0.95,
        answer_score=0.95,
        hallucination_score=0.05,
    )

    retrieval_service.retrieve_answer.return_value = response

    result = await healing_service.answer(
        "What is FastAPI?"
    )

    assert result.response is response

    assert result.healing.healing_attempted is False

    assert result.healing.retry_count == 0
    
    
    
@pytest.mark.asyncio
async def test_retry_due_to_low_retrieval_confidence(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    Low retrieval confidence should trigger healing.
    """

    original = query_response_factory(
        retrieval_confidence=0.30,
        answer_score=0.80,
    )

    healed = query_response_factory(
        retrieval_confidence=0.90,
        answer_score=0.90,
    )

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    llm_service.generate.return_value = (
        "Improved query"
    )

    response = await healing_service.answer(
        "FastAPI"
    )

    assert response.healing.healing_attempted

    assert response.healing.healing_success

    assert response.healing.retry_count == 1
    
    
    
@pytest.mark.asyncio
async def test_retry_due_to_hallucination(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    High hallucination risk should trigger healing.
    """

    original = query_response_factory(
        hallucination_score=0.90,
    )

    healed = query_response_factory(
        hallucination_score=0.05,
    )

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    llm_service.generate.return_value = (
        "Improved query"
    )

    result = await healing_service.answer(
        "dependency injection"
    )

    assert result.healing.healing_attempted

    assert result.healing.healing_success
    
    
    
@pytest.mark.asyncio
async def test_healed_answer_selected(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    The healed answer should be selected when it is objectively better.
    """

    original = query_response_factory(
        answer_score=0.50,
    )

    healed = query_response_factory(
        answer_score=0.95,
    )

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    llm_service.generate.return_value = (
        "Better query"
    )

    response = await healing_service.answer(
        "DI"
    )

    assert (
        response.healing.selected_answer.value
        == "healed"
    )
    
    
    
@pytest.mark.asyncio
async def test_original_answer_retained(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    The original answer should remain selected if healing makes the
    result worse.
    """

    original = query_response_factory(
        hallucination_score=0.05,
    )

    healed = query_response_factory(
        hallucination_score=0.80,
    )

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    llm_service.generate.return_value = (
        "Improved query"
    )

    response = await healing_service.answer(
        "DI"
    )

    assert (
        response.healing.selected_answer.value
        == "original"
    )
    
    
    
@pytest.mark.asyncio
async def test_retry_failure(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    Failures during query rewriting should return the original answer.
    """

    original = query_response_factory(
        retrieval_confidence=0.30,
    )

    retrieval_service.retrieve_answer.return_value = (
        original
    )

    llm_service.generate.side_effect = RuntimeError(
        "LLM unavailable"
    )

    response = await healing_service.answer(
        "FastAPI"
    )

    assert (
        response.healing.selected_answer.value
        == "original"
    )

    assert response.healing.healing_success is False
    
    
    
@pytest.mark.asyncio
async def test_retrieval_called_twice(
    healing_service,
    retrieval_service,
    llm_service,
):
    """
    Healing should execute two retrievals.
    """

    original = query_response_factory(
        retrieval_confidence=0.30,
    )

    healed = query_response_factory()

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    llm_service.generate.return_value = (
        "Improved query"
    )

    await healing_service.answer(
        "FastAPI"
    )

    assert (
        retrieval_service.retrieve_answer.await_count
        == 2
    )
    
    
    
    
