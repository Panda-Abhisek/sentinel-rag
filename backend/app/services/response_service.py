from app.schemas.retrieval import QueryResponse
from app.evaluation.models import LatencyMetrics
from app.healing.models import HealingResponse
from app.healing.models import HealingReport
from app.rag.source_mapper import SourceMapper

from langchain_core.documents import Document


class ResponseBuilder:
    """
    Builds the final API responses from graph state.

    This class contains no retrieval, generation or evaluation logic.
    Its only responsibility is assembling response DTOs.
    """

    @staticmethod
    def build_query_response(
        *,
        answer: str,
        documents: list[tuple[Document, float]],
        evaluation,
        retrieval_ms: float,
        generation_ms: float,
        evaluation_ms: float,
        total_ms: float,
    ) -> QueryResponse:

        return QueryResponse(
            answer=answer,
            sources=SourceMapper.source_mapper(documents),
            evaluation=evaluation,
            latency=LatencyMetrics(
                retrieval_ms=retrieval_ms,
                generation_ms=generation_ms,
                evaluation_ms=evaluation_ms,
                total_ms=total_ms,
            ),
        )

    @staticmethod
    def build_healing_response(
        *,
        original_response: QueryResponse,
        final_response: QueryResponse,
        healing_report: HealingReport | None,
    ) -> HealingResponse:

        return HealingResponse(
            original_response=original_response,
            final_response=final_response,
            healing_report=healing_report,
        )