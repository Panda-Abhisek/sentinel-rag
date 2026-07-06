from app.evaluation.confidence_scorer import ConfidenceScorer
from app.evaluation.metrics import MetricsCalculator, RetrievedResults
from app.evaluation.models import RetrievalEvaluation


class RetrievalEvaluator:
    """
    Evaluates the quality of retrieved documents.
    """

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
        """
        Evaluate retrieval results.
        """

        metrics = self._metrics_calculator.calculate(results)

        confidence = self._confidence_scorer.calculate(metrics)

        warnings = self._generate_warnings(metrics)

        return RetrievalEvaluation(
            confidence=confidence,
            metrics=metrics,
            warnings=warnings,
        )

    def _generate_warnings(self, metrics) -> list[str]:
        """
        Generate retrieval warnings.
        """

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