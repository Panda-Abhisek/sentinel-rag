"""
Healing policy for SentinelRAG.

This module contains the decision engine responsible for determining
whether the retrieval pipeline should perform a self-healing retry
based on the evaluation report.

The policy is intentionally heuristic-based and stateless. It does not
perform retrieval, query rewriting, or answer generation. Its sole
responsibility is to inspect evaluation results and produce a
HealingDecision.
"""

import logging

from app.evaluation.models import EvaluationReport, RiskLevel
from app.healing.models import HealingDecision, RetryReason

logger = logging.getLogger(__name__)


class HealingPolicy:
    """
    Determines whether the retrieval pipeline should perform a
    self-healing retry based on evaluation results.

    Rules are evaluated in priority order. The first matching rule
    determines the retry reason.
    """

    def __init__(
        self,
        retrieval_threshold: float = 0.60,
        answer_threshold: float = 0.70,
        duplicate_threshold: float = 0.50,
    ) -> None:
        self.retrieval_threshold = retrieval_threshold
        self.answer_threshold = answer_threshold
        self.duplicate_threshold = duplicate_threshold

        logger.info(
            "HealingPolicy initialized "
            "(retrieval_threshold=%.2f, "
            "answer_threshold=%.2f, "
            "duplicate_threshold=%.2f)",
            self.retrieval_threshold,
            self.answer_threshold,
            self.duplicate_threshold,
        )

    def decide(
        self,
        evaluation: EvaluationReport,
    ) -> HealingDecision:
        """
        Determine whether the pipeline should perform a retry.

        Parameters
        ----------
        evaluation:
            Unified evaluation report generated after retrieval and
            answer evaluation.

        Returns
        -------
        HealingDecision
            Decision describing whether a retry should occur and the
            reason for the retry.
        """

        logger.info("Evaluating healing policy.")

        if self._low_retrieval_confidence(evaluation):
            logger.info(
                "Healing triggered: low retrieval confidence "
                "(score=%.3f, threshold=%.3f).",
                evaluation.retrieval.confidence.score,
                self.retrieval_threshold,
            )

            return HealingDecision(
                should_retry=True,
                retry_reason=RetryReason.LOW_RETRIEVAL_CONFIDENCE,
            )

        if self._high_hallucination_risk(evaluation):
            logger.info(
                "Healing triggered: high hallucination risk."
            )

            return HealingDecision(
                should_retry=True,
                retry_reason=RetryReason.HIGH_HALLUCINATION_RISK,
            )

        if self._low_answer_quality(evaluation):
            logger.info(
                "Healing triggered: low answer quality "
                "(score=%.3f, threshold=%.3f).",
                evaluation.answer.overall_score,
                self.answer_threshold,
            )

            return HealingDecision(
                should_retry=True,
                retry_reason=RetryReason.LOW_ANSWER_QUALITY,
            )

        if self._duplicate_context(evaluation):
            logger.info(
                "Healing triggered: duplicate retrieval context "
                "(duplicate_ratio=%.3f, threshold=%.3f).",
                evaluation.retrieval.metrics.duplicate_ratio,
                self.duplicate_threshold,
            )

            return HealingDecision(
                should_retry=True,
                retry_reason=RetryReason.DUPLICATE_CONTEXT,
            )

        logger.info(
            "Healing decision: retry=%s reason=%s",
            False,
            None,
        )

        return HealingDecision(
            should_retry=False,
            rewrite_query=False,
        )

    def _low_retrieval_confidence(
        self,
        evaluation: EvaluationReport,
    ) -> bool:
        """
        Check whether retrieval confidence is below the configured
        threshold.
        """
        return (
            evaluation.retrieval.confidence.score
            < self.retrieval_threshold
        )

    def _high_hallucination_risk(
        self,
        evaluation: EvaluationReport,
    ) -> bool:
        """
        Check whether the generated answer has a high hallucination
        risk.
        """
        return (
            evaluation.hallucination.risk_level
            == RiskLevel.HIGH
        )

    def _low_answer_quality(
        self,
        evaluation: EvaluationReport,
    ) -> bool:
        """
        Check whether the generated answer quality is below the
        configured threshold.
        """
        return (
            evaluation.answer.overall_score
            < self.answer_threshold
        )

    def _duplicate_context(
        self,
        evaluation: EvaluationReport,
    ) -> bool:
        """
        Check whether the retrieved context contains excessive
        duplicate chunks.
        """
        return (
            evaluation.retrieval.metrics.duplicate_ratio
            > self.duplicate_threshold
        )