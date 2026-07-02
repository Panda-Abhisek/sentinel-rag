"""
Unit tests for AnswerSelector.
"""

import pytest

from app.healing.answer_selector import AnswerSelector
from app.healing.models import (
    SelectedAnswer,
    WinnerReason,
)
from tests.factories import query_response_factory


@pytest.fixture
def selector() -> AnswerSelector:
    return AnswerSelector()


def test_select_healed_by_lower_hallucination(
    selector: AnswerSelector,
) -> None:
    """
    The healed answer should win when it has a lower hallucination risk.
    """

    original = query_response_factory(
        hallucination_score=0.90,
    )

    healed = query_response_factory(
        hallucination_score=0.10,
    )

    result = selector.select(
        original,
        healed,
    )

    assert result.response is healed
    assert result.selected_answer is SelectedAnswer.HEALED
    assert (
        result.winner_reason
        is WinnerReason.LOWER_HALLUCINATION
    )


def test_select_original_by_lower_hallucination(
    selector: AnswerSelector,
) -> None:
    """
    The original answer should win when it has a lower hallucination risk.
    """

    original = query_response_factory(
        hallucination_score=0.05,
    )

    healed = query_response_factory(
        hallucination_score=0.80,
    )

    result = selector.select(
        original,
        healed,
    )

    assert result.response is original
    assert result.selected_answer is SelectedAnswer.ORIGINAL
    assert (
        result.winner_reason
        is WinnerReason.LOWER_HALLUCINATION
    )


def test_select_healed_by_answer_quality(
    selector: AnswerSelector,
) -> None:
    """
    If hallucination risk is equal, answer quality should decide.
    """

    original = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.60,
    )

    healed = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.95,
    )

    result = selector.select(
        original,
        healed,
    )

    assert result.response is healed
    assert result.selected_answer is SelectedAnswer.HEALED
    assert (
        result.winner_reason
        is WinnerReason.HIGHER_ANSWER_QUALITY
    )


def test_select_original_by_answer_quality(
    selector: AnswerSelector,
) -> None:
    """
    The original answer should win when it has the higher quality score.
    """

    original = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.95,
    )

    healed = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.60,
    )

    result = selector.select(
        original,
        healed,
    )

    assert result.response is original
    assert result.selected_answer is SelectedAnswer.ORIGINAL
    assert (
        result.winner_reason
        is WinnerReason.HIGHER_ANSWER_QUALITY
    )


def test_select_healed_by_retrieval_confidence(
    selector: AnswerSelector,
) -> None:
    """
    Retrieval confidence should be used after hallucination and answer
    quality are tied.
    """

    original = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.90,
        retrieval_confidence=0.60,
    )

    healed = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.90,
        retrieval_confidence=0.95,
    )

    result = selector.select(
        original,
        healed,
    )

    assert result.response is healed
    assert result.selected_answer is SelectedAnswer.HEALED
    assert (
        result.winner_reason
        is WinnerReason.HIGHER_RETRIEVAL_CONFIDENCE
    )


def test_keep_original_when_all_metrics_equal(
    selector: AnswerSelector,
) -> None:
    """
    The original answer should be retained when every comparison metric
    is identical.
    """

    original = query_response_factory()

    healed = query_response_factory()

    result = selector.select(
        original,
        healed,
    )

    assert result.response is original
    assert result.selected_answer is SelectedAnswer.ORIGINAL
    assert (
        result.winner_reason
        is WinnerReason.ORIGINAL_RETAINED
    )


def test_raise_error_when_evaluation_missing(
    selector: AnswerSelector,
) -> None:
    """
    Responses without evaluation data should be rejected.
    """

    original = query_response_factory()
    healed = query_response_factory()

    healed.evaluation = None

    with pytest.raises(ValueError):
        selector.select(
            original,
            healed,
        )
        
        
def test_hallucination_has_higher_priority_than_answer_quality(
    selector: AnswerSelector,
) -> None:
    """
    Hallucination risk must always take precedence over answer quality.
    """

    original = query_response_factory(
        hallucination_score=0.10,
        answer_score=0.60,
    )

    healed = query_response_factory(
        hallucination_score=0.90,
        answer_score=1.00,
    )

    result = selector.select(
        original,
        healed,
    )

    assert result.response is original
    assert (
        result.winner_reason
        is WinnerReason.LOWER_HALLUCINATION
    )