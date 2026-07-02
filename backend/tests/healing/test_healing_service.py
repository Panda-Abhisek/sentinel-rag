"""
Unit tests for HealingService.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.healing.answer_selector import AnswerSelector
from app.healing.healing_policy import HealingPolicy
from app.healing.healing_service import HealingService
from app.healing.models import (
    HealingDecision,
    RetryReason,
    SelectedAnswer,
    SelectionResult,
    WinnerReason,
)
from app.healing.retry_strategy import RetryStrategy
from app.services.retrieval_service import RetrievalService

from tests.factories import query_response_factory


@pytest.fixture
def retrieval_service() -> AsyncMock:
    return AsyncMock(spec=RetrievalService)


@pytest.fixture
def healing_policy() -> MagicMock:
    return MagicMock(spec=HealingPolicy)


@pytest.fixture
def retry_strategy() -> AsyncMock:
    return AsyncMock(spec=RetryStrategy)


@pytest.fixture
def answer_selector() -> MagicMock:
    return MagicMock(spec=AnswerSelector)


@pytest.fixture
def healing_service(
    retrieval_service,
    healing_policy,
    retry_strategy,
    answer_selector,
):
    return HealingService(
        retrieval_service=retrieval_service,
        healing_policy=healing_policy,
        retry_strategy=retry_strategy,
        answer_selector=answer_selector,
    )
    
@pytest.mark.asyncio
async def test_returns_original_when_retry_not_required(
    healing_service,
    retrieval_service,
    healing_policy,
):
    """
    Original answer should be returned when healing is unnecessary.
    """

    original = query_response_factory()

    retrieval_service.retrieve_answer.return_value = original

    healing_policy.decide.return_value = HealingDecision(
        should_retry=False,
    )

    response = await healing_service.answer(
        "What is FastAPI?"
    )

    assert response.response is original

    assert response.healing.healing_attempted is False

    assert (
        response.healing.selected_answer
        == SelectedAnswer.ORIGINAL
    )

    retrieval_service.retrieve_answer.assert_awaited_once()
    
@pytest.mark.asyncio
async def test_retry_returns_healed_answer(
    healing_service,
    retrieval_service,
    healing_policy,
    retry_strategy,
    answer_selector,
):
    """
    Healed answer should be returned when selected.
    """

    original = query_response_factory(
        answer_score=0.60,
    )

    healed = query_response_factory(
        answer_score=0.95,
    )

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    healing_policy.decide.return_value = HealingDecision(
        should_retry=True,
        retry_reason=RetryReason.LOW_ANSWER_QUALITY,
    )

    retry_strategy.retry.return_value = (
        "Improved query"
    )

    answer_selector.select.return_value = (
        SelectionResult(
            response=healed,
            selected_answer=SelectedAnswer.HEALED,
            winner_reason=WinnerReason.HIGHER_ANSWER_QUALITY,
        )
    )

    response = await healing_service.answer(
        "dependency injection"
    )

    assert response.response is healed

    assert response.healing.healing_attempted

    assert response.healing.healing_success

    assert (
        response.healing.selected_answer
        == SelectedAnswer.HEALED
    )
    
@pytest.mark.asyncio
async def test_retry_keeps_original_answer(
    healing_service,
    retrieval_service,
    healing_policy,
    retry_strategy,
    answer_selector,
):
    """
    Original answer should be retained after retry if it is still
    considered better.
    """

    original = query_response_factory()

    healed = query_response_factory(
        hallucination_score=0.80,
    )

    retrieval_service.retrieve_answer.side_effect = [
        original,
        healed,
    ]

    healing_policy.decide.return_value = HealingDecision(
        should_retry=True,
        retry_reason=RetryReason.HIGH_HALLUCINATION_RISK,
    )

    retry_strategy.retry.return_value = (
        "Improved query"
    )

    answer_selector.select.return_value = (
        SelectionResult(
            response=original,
            selected_answer=SelectedAnswer.ORIGINAL,
            winner_reason=WinnerReason.LOWER_HALLUCINATION,
        )
    )

    response = await healing_service.answer(
        "query"
    )

    assert response.response is original

    assert response.healing.healing_attempted

    assert response.healing.healing_success

    assert (
        response.healing.selected_answer
        == SelectedAnswer.ORIGINAL
    )
    
@pytest.mark.asyncio
async def test_retry_failure_returns_original(
    healing_service,
    retrieval_service,
    healing_policy,
    retry_strategy,
):
    """
    Failures during retry should gracefully fall back to the original
    response.
    """

    original = query_response_factory()

    retrieval_service.retrieve_answer.return_value = (
        original
    )

    healing_policy.decide.return_value = HealingDecision(
        should_retry=True,
        retry_reason=RetryReason.UNKNOWN,
    )

    retry_strategy.retry.side_effect = RuntimeError(
        "rewrite failed"
    )

    response = await healing_service.answer(
        "query"
    )

    assert response.response is original

    assert (
        response.healing.selected_answer
        == SelectedAnswer.ORIGINAL
    )

    assert response.healing.healing_attempted

    assert response.healing.selected_answer.value == "original"

    assert response.healing.healing_success
    
@pytest.mark.asyncio
async def test_invalid_query_raises_value_error(
    healing_service,
):
    """
    Empty queries should be rejected.
    """

    with pytest.raises(ValueError):
        await healing_service.answer("")
        
@pytest.mark.asyncio
async def test_whitespace_query_raises_value_error(
    healing_service,
):
    """
    Whitespace-only queries should be rejected.
    """

    with pytest.raises(ValueError):
        await healing_service.answer("      ")
        
def test_validate_query_accepts_valid_query(
    healing_service,
):
    """
    Validation should accept a normal query.
    """

    healing_service._validate_query(
        "What is FastAPI?"
    )
    
    
def test_validate_query_rejects_empty_query(
    healing_service,
):
    """
    Validation should reject an empty query.
    """

    with pytest.raises(ValueError):
        healing_service._validate_query("")