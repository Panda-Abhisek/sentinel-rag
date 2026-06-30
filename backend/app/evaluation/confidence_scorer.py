from app.evaluation.models import ConfidenceScore, RetrievalMetrics


class ConfidenceScorer:
    """
    Computes an overall confidence score based on retrieval metrics.
    """

    def calculate(self, metrics: RetrievalMetrics) -> ConfidenceScore:
        """
        Calculate confidence score from retrieval metrics.
        """

        score = self._calculate_score(metrics)
        level = self._determine_level(score)

        return ConfidenceScore(
            score=round(score, 2),
            level=level,
        )

    def _calculate_score(self, metrics: RetrievalMetrics) -> float:
        """
        Weighted confidence calculation.

        Final score is clamped to the range [0.0, 1.0].
        """

        score = (
            metrics.average_similarity * 0.50
            + metrics.max_similarity * 0.20
            + self._document_score(metrics.retrieved_documents) * 0.15
            + self._source_diversity_score(metrics.unique_sources) * 0.10
            + (1 - metrics.duplicate_ratio) * 0.05
        )

        return max(0.0, min(score, 1.0))

    @staticmethod
    def _document_score(document_count: int) -> float:
        """
        Normalize document count to [0, 1].
        """

        return min(document_count / 5, 1.0)

    @staticmethod
    def _source_diversity_score(source_count: int) -> float:
        """
        Normalize unique source count to [0, 1].
        """

        return min(source_count / 3, 1.0)

    @staticmethod
    def _determine_level(score: float) -> str:
        """
        Convert numeric confidence into a human-readable level.
        """

        if score >= 0.80:
            return "HIGH"

        if score >= 0.60:
            return "MEDIUM"

        return "LOW"