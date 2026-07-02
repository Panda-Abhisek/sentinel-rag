"""
Answer selection service for SentinelRAG.

This module contains the AnswerSelector responsible for comparing the
original retrieval result with the healed retrieval result and
selecting the better answer.

Selection is deterministic and follows a fixed priority:

1. Lower hallucination risk
2. Higher answer quality
3. Higher retrieval confidence
4. Original answer (tie breaker)
"""

import logging

from app.schemas.retrieval import QueryResponse
from app.healing.models import SelectedAnswer, SelectionResult, WinnerReason

logger = logging.getLogger(__name__)


class AnswerSelector:
    """
    Select the better answer between an original response and a healed
    response using evaluation metrics.
    """

    def select(
        self,
        original: QueryResponse,
        healed: QueryResponse,
    ) -> SelectionResult:
        """
        Select the better response.

        Parameters
        ----------
        original:
            Response from the initial retrieval.

        healed:
            Response from the healing retry.

        Returns
        -------
        QueryResponse
            The selected response.
        """

        self._validate_response(original)
        self._validate_response(healed)

        logger.info("Selecting best answer.")

        winner = self._compare_hallucination_risk(original, healed)

        if winner is not None:
            logger.info(
                "Answer selected based on hallucination risk."
            )
            return SelectionResult(
                    response=healed,
                    selected_answer=SelectedAnswer.HEALED,
                    winner_reason=WinnerReason.LOWER_HALLUCINATION,
                ) if winner else SelectionResult(
                    response=original,
                    selected_answer=SelectedAnswer.ORIGINAL,
                    winner_reason=WinnerReason.LOWER_HALLUCINATION,
                )

        winner = self._compare_answer_quality(original, healed)

        if winner is not None:
            logger.info(
                "Answer selected based on answer quality."
            )
            return SelectionResult(
                    response=healed,
                    selected_answer=SelectedAnswer.HEALED,
                    winner_reason=WinnerReason.HIGHER_ANSWER_QUALITY,
                ) if winner else SelectionResult(
                    response=original,
                    selected_answer=SelectedAnswer.ORIGINAL,
                    winner_reason=WinnerReason.HIGHER_ANSWER_QUALITY,
                )

        winner = self._compare_retrieval_confidence(
            original,
            healed,
        )

        if winner is not None:
            logger.info(
                "Answer selected based on retrieval confidence."
            )
            return SelectionResult(
                    response=healed,
                    selected_answer=SelectedAnswer.HEALED,
                    winner_reason=WinnerReason.HIGHER_RETRIEVAL_CONFIDENCE,
                ) if winner else SelectionResult(
                    response=original,
                    selected_answer=SelectedAnswer.ORIGINAL,
                    winner_reason=WinnerReason.HIGHER_RETRIEVAL_CONFIDENCE,
                )

        logger.info(
            "Answers are equivalent. Selecting original answer."
        )

        return SelectionResult(
            response=original,
            selected_answer=SelectedAnswer.ORIGINAL,
            winner_reason=WinnerReason.ORIGINAL_RETAINED,
        )

    def _compare_hallucination_risk(
        self,
        original: QueryResponse,
        healed: QueryResponse,
    ) -> bool | None:
        """
        Compare hallucination risk.

        Returns
        -------
        bool | None
            True if healed wins, False if original wins,
            None if equal.
        """

        original_risk = original.evaluation.hallucination.risk_level.priority
        healed_risk = healed.evaluation.hallucination.risk_level.priority

        if healed_risk < original_risk:
            return True

        if healed_risk > original_risk:
            return False

        return None

    def _compare_answer_quality(
        self,
        original: QueryResponse,
        healed: QueryResponse,
    ) -> bool | None:

        original_score = original.evaluation.answer.overall_score
        healed_score = healed.evaluation.answer.overall_score

        if healed_score > original_score:
            return True

        if healed_score < original_score:
            return False

        return None

    def _compare_retrieval_confidence(
        self,
        original: QueryResponse,
        healed: QueryResponse,
    ) -> bool | None:

        original_score = (
            original.evaluation.retrieval.confidence.score
        )

        healed_score = (
            healed.evaluation.retrieval.confidence.score
        )

        if healed_score > original_score:
            return True

        if healed_score < original_score:
            return False

        return None

    def _validate_response(
        self,
        response: QueryResponse,
    ) -> None:
        """
        Validate a retrieval response.
        """

        if response.evaluation is None:
            raise ValueError(
                "QueryResponse must contain an evaluation."
            )