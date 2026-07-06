import logging
from dataclasses import dataclass
from statistics import mean, stdev
from typing import TypeAlias

from langchain_core.documents import Document

from app.evaluation.models import RetrievalMetrics

logger = logging.getLogger(__name__)

RetrievedResults: TypeAlias = list[tuple[Document, float]]


@dataclass(slots=True)
class SimilarityMetrics:
    average: float
    maximum: float
    minimum: float
    std: float


class MetricsCalculator:

    def calculate(self, results: RetrievedResults) -> RetrievalMetrics:
        if not results:
            logger.info("No results to compute metrics for.")
            return self._empty_metrics()

        similarity_metrics = self._calculate_similarity_metrics(results)
        unique_sources = self._calculate_source_metrics(results)
        average_chunk_length = self._calculate_chunk_metrics(results)
        duplicate_ratio = self._calculate_duplicate_ratio(results)

        metrics = RetrievalMetrics(
            average_similarity=similarity_metrics.average,
            max_similarity=similarity_metrics.maximum,
            min_similarity=similarity_metrics.minimum,
            similarity_std=similarity_metrics.std,
            retrieved_documents=len(results),
            unique_sources=unique_sources,
            average_chunk_length=average_chunk_length,
            duplicate_ratio=duplicate_ratio,
        )

        logger.info(
            "Metrics: docs=%d | avg_sim=%.3f | max_sim=%.3f | sources=%d | dup_ratio=%.2f",
            metrics.retrieved_documents,
            metrics.average_similarity,
            metrics.max_similarity,
            metrics.unique_sources,
            metrics.duplicate_ratio,
        )

        return metrics

    @staticmethod
    def _empty_metrics() -> RetrievalMetrics:
        return RetrievalMetrics(
            average_similarity=0.0,
            max_similarity=0.0,
            min_similarity=0.0,
            similarity_std=0.0,
            retrieved_documents=0,
            unique_sources=0,
            average_chunk_length=0.0,
            duplicate_ratio=0.0,
        )

    def _calculate_similarity_metrics(
        self,
        results: RetrievedResults,
    ) -> SimilarityMetrics:
        scores = [score for _, score in results]

        return SimilarityMetrics(
            average=mean(scores),
            maximum=max(scores),
            minimum=min(scores),
            std=stdev(scores) if len(scores) > 1 else 0.0,
        )

    def _calculate_source_metrics(
        self,
        results: RetrievedResults,
    ) -> int:
        sources = {
            document.metadata.get("source", "unknown")
            for document, _ in results
        }

        return len(sources)

    def _calculate_chunk_metrics(
        self,
        results: RetrievedResults,
    ) -> float:
        chunk_lengths = [
            len(document.page_content)
            for document, _ in results
        ]

        return mean(chunk_lengths)

    def _calculate_duplicate_ratio(
        self,
        results: RetrievedResults,
    ) -> float:
        contents = [
            self._normalize_content(document.page_content)
            for document, _ in results
        ]

        unique_chunks = len(set(contents))
        total_chunks = len(contents)

        duplicate_chunks = total_chunks - unique_chunks

        return duplicate_chunks / total_chunks

    @staticmethod
    def _normalize_content(content: str) -> str:
        return " ".join(content.split())
