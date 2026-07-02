"""
Unit tests for HealingPolicy.
"""

import pytest

from app.healing.healing_policy import HealingPolicy
from app.healing.models import RetryReason
from tests.factories import evaluation_report_factory


@pytest.fixture
def policy() -> HealingPolicy:
    return HealingPolicy()


def test_retry_on_low_retrieval_confidence(
    policy: HealingPolicy,
) -> None:
    """
    Retry should be triggered when retrieval confidence is below the
    configured threshold.
    """

    report = evaluation_report_factory(
        retrieval_confidence=0.40,
    )

    decision = policy.decide(report)

    assert decision.should_retry is True
    assert (
        decision.retry_reason
        == RetryReason.LOW_RETRIEVAL_CONFIDENCE
    )


def test_retry_on_high_hallucination_risk(
    policy: HealingPolicy,
) -> None:
    """
    Retry should be triggered when hallucination risk is high.
    """

    report = evaluation_report_factory(
        hallucination_score=0.90,
    )

    decision = policy.decide(report)

    assert decision.should_retry is True
    assert (
        decision.retry_reason
        == RetryReason.HIGH_HALLUCINATION_RISK
    )


def test_retry_on_low_answer_quality(
    policy: HealingPolicy,
) -> None:
    """
    Retry should be triggered when answer quality is below the
    configured threshold.
    """

    report = evaluation_report_factory(
        answer_score=0.40,
    )

    decision = policy.decide(report)

    assert decision.should_retry is True
    assert (
        decision.retry_reason
        == RetryReason.LOW_ANSWER_QUALITY
    )


def test_retry_on_duplicate_context(
    policy: HealingPolicy,
) -> None:
    """
    Retry should be triggered when duplicate context exceeds the
    configured threshold.
    """

    report = evaluation_report_factory(
        duplicate_ratio=0.80,
    )

    decision = policy.decide(report)

    assert decision.should_retry is True
    assert (
        decision.retry_reason
        == RetryReason.DUPLICATE_CONTEXT
    )


def test_no_retry_for_high_quality_response(
    policy: HealingPolicy,
) -> None:
    """
    High-quality responses should not trigger self-healing.
    """

    report = evaluation_report_factory(
        retrieval_confidence=0.90,
        answer_score=0.90,
        hallucination_score=0.05,
        duplicate_ratio=0.0,
    )

    decision = policy.decide(report)

    assert decision.should_retry is False
    assert decision.retry_reason is None
    
    
def test_first_matching_rule_wins(
    policy: HealingPolicy,
) -> None:
    """
    The first matching rule should determine the retry reason.
    """

    report = evaluation_report_factory(
        retrieval_confidence=0.40,
        hallucination_score=0.95,
        answer_score=0.20,
        duplicate_ratio=0.90,
    )

    decision = policy.decide(report)

    assert decision.should_retry is True

    assert (
        decision.retry_reason
        == RetryReason.LOW_RETRIEVAL_CONFIDENCE
    )