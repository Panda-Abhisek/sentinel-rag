from app.evaluation.confidence_scorer import ConfidenceScorer
from app.evaluation.models import RetrievalMetrics


def build_metrics(avg_similarity: float):
    return RetrievalMetrics(
        average_similarity=avg_similarity,
        max_similarity=avg_similarity,
        min_similarity=avg_similarity,
        similarity_std=0.01,
        retrieved_documents=5,
        unique_sources=3,
        average_chunk_length=400,
        duplicate_ratio=0.0,
    )


def test_high_confidence():
    scorer = ConfidenceScorer()

    confidence = scorer.calculate(build_metrics(0.90))

    assert confidence.level == "HIGH"


def test_medium_confidence():
    scorer = ConfidenceScorer()

    confidence = scorer.calculate(build_metrics(0.62))

    assert confidence.level == "MEDIUM"


def test_low_confidence():
    scorer = ConfidenceScorer()

    confidence = scorer.calculate(build_metrics(0.40))

    assert confidence.level == "LOW"