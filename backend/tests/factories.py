"""
Reusable test factories for SentinelRAG.

These helpers construct valid domain models with sensible defaults.
Individual tests should override only the fields relevant to the
scenario being tested.
"""

from app.evaluation.models import (
    AnswerEvaluation,
    ConfidenceScore,
    EvaluationReport,
    HallucinationEvaluation,
    LatencyMetrics,
    RetrievalEvaluation,
    RetrievalMetrics,
)
from app.schemas.retrieval import (
    QueryResponse,
    SourceDocument,
)


def retrieval_metrics_factory(
    *,
    average_similarity: float = 0.80,
    max_similarity: float = 0.90,
    min_similarity: float = 0.70,
    similarity_std: float = 0.05,
    retrieved_documents: int = 5,
    unique_sources: int = 5,
    average_chunk_length: float = 500.0,
    duplicate_ratio: float = 0.0,
) -> RetrievalMetrics:
    return RetrievalMetrics(
        average_similarity=average_similarity,
        max_similarity=max_similarity,
        min_similarity=min_similarity,
        similarity_std=similarity_std,
        retrieved_documents=retrieved_documents,
        unique_sources=unique_sources,
        average_chunk_length=average_chunk_length,
        duplicate_ratio=duplicate_ratio,
    )


def confidence_factory(
    *,
    score: float = 0.80,
    level: str = "HIGH",
) -> ConfidenceScore:
    return ConfidenceScore(
        score=score,
        level=level,
    )


def retrieval_evaluation_factory(
    *,
    confidence_score: float = 0.80,
    confidence_level: str = "HIGH",
    duplicate_ratio: float = 0.0,
    warnings: list[str] | None = None,
) -> RetrievalEvaluation:
    return RetrievalEvaluation(
        confidence=confidence_factory(
            score=confidence_score,
            level=confidence_level,
        ),
        metrics=retrieval_metrics_factory(
            duplicate_ratio=duplicate_ratio,
        ),
        warnings=warnings or [],
    )


def answer_evaluation_factory(
    *,
    faithfulness: float = 0.90,
    answer_relevancy: float = 0.90,
    context_utilization: float = 0.90,
    completeness: float = 0.90,
) -> AnswerEvaluation:
    return AnswerEvaluation(
        faithfulness=faithfulness,
        answer_relevancy=answer_relevancy,
        context_utilization=context_utilization,
        completeness=completeness,
    )


def hallucination_factory(
    *,
    hallucination_score: float = 0.10,
) -> HallucinationEvaluation:
    return HallucinationEvaluation(
        hallucination_score=hallucination_score,
    )


def evaluation_report_factory(
    *,
    retrieval_confidence: float = 0.80,
    answer_score: float = 0.90,
    hallucination_score: float = 0.10,
    duplicate_ratio: float = 0.0,
) -> EvaluationReport:
    return EvaluationReport(
        retrieval=retrieval_evaluation_factory(
            confidence_score=retrieval_confidence,
            duplicate_ratio=duplicate_ratio,
        ),
        answer=answer_evaluation_factory(
            faithfulness=answer_score,
            answer_relevancy=answer_score,
            context_utilization=answer_score,
            completeness=answer_score,
        ),
        hallucination=hallucination_factory(
            hallucination_score=hallucination_score,
        ),
    )


def latency_factory(
    *,
    retrieval_ms: float = 100.0,
    generation_ms: float = 500.0,
    evaluation_ms: float = 300.0,
    total_ms: float = 900.0,
) -> LatencyMetrics:
    return LatencyMetrics(
        retrieval_ms=retrieval_ms,
        generation_ms=generation_ms,
        evaluation_ms=evaluation_ms,
        total_ms=total_ms,
    )


def source_factory(
    *,
    page: int = 1,
    source: str = "test.pdf",
    score: float = 0.90,
    content: str = "Test content",
) -> SourceDocument:
    return SourceDocument(
        page=page,
        source=source,
        score=score,
        content=content,
    )


def query_response_factory(
    *,
    answer: str = "Test answer",
    answer_score: float = 0.90,
    hallucination_score: float = 0.10,
    retrieval_confidence: float = 0.80,
    duplicate_ratio: float = 0.0,
) -> QueryResponse:
    return QueryResponse(
        answer=answer,
        sources=[
            source_factory(),
        ],
        evaluation=evaluation_report_factory(
            retrieval_confidence=retrieval_confidence,
            answer_score=answer_score,
            hallucination_score=hallucination_score,
            duplicate_ratio=duplicate_ratio,
        ),
        latency=latency_factory(),
    )