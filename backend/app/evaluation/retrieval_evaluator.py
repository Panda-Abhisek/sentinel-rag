import logging

from app.evaluation.confidence_scorer import ConfidenceScorer
from app.evaluation.metrics import MetricsCalculator, RetrievedResults
from app.evaluation.models import RetrievalEvaluation

logger = logging.getLogger(__name__)


class RetrievalEvaluator:

    def __init__(
        self,
        metrics_calculator: MetricsCalculator | None = None,
        confidence_scorer: ConfidenceScorer | None = None,
    ) -> None:
        self._metrics_calculator = metrics_calculator or MetricsCalculator()
        self._confidence_scorer = confidence_scorer or ConfidenceScorer()

    def evaluate(
        self,
        results: RetrievedResults,
    ) -> RetrievalEvaluation:

        logger.info("Evaluating retrieval quality for %d documents.", len(results))

        metrics = self._metrics_calculator.calculate(results)

        confidence = self._confidence_scorer.calculate(metrics)

        warnings = self._generate_warnings(metrics)

        logger.info(
            "Retrieval evaluation: confidence=%s (%.2f) | warnings=%d",
            confidence.level,
            confidence.score,
            len(warnings),
        )

        return RetrievalEvaluation(
            confidence=confidence,
            metrics=metrics,
            warnings=warnings,
        )

    def _generate_warnings(self, metrics) -> list[str]:

        warnings: list[str] = []

        if metrics.retrieved_documents == 0:
            warnings.append("No documents retrieved.")

        if metrics.average_similarity < 0.60:
            warnings.append("Low average similarity score.")

        if metrics.duplicate_ratio > 0.40:
            warnings.append("High duplicate chunk ratio.")

        if metrics.unique_sources <= 1:
            warnings.append("Low source diversity.")

        return warnings
