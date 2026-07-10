import logging
import time

from app.langgraph.graph import graph
from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.evaluation.models import LatencyMetrics
from app.rag.source_mapper import SourceMapper
from app.schemas.retrieval import QueryResponse
from app.observability.events import ObservabilityEvent
from app.observability.langsmith import trace_graph

logger = logging.getLogger(__name__)


class GraphService:

    def __init__(self, dependencies: SentinelContext):
        self.dependencies = dependencies

    @trace_graph(
        "SentinelRAG",
        get_metadata=lambda self, *a, **kw: {
            "request_id": self.dependencies.tracing.request_id,
            "project": "SentinelRAG",
        },
    )
    async def execute(
        self,
        question: str,
        top_k: int,
    ):

        start = time.perf_counter()

        initial_state: SentinelState = {
            "query": question,
            "top_k": top_k,

            "retrieved_documents": [],

            "answer": None,

            "evaluation": None,

            "planner_route": "retrieve",
            "critic_route": "finish",

            "planner_reason": "",
            "critic_reason": "",

            "retry_count": 0,
            "max_retries": 2,

            "retrieval_ms": 0.0,
            "generation_ms": 0.0,
            "evaluation_ms": 0.0,
            "total_ms": 0.0,

            "candidate_answers": [],
            "candidate_evaluations": [],
            "selected_answer_index": 0,

            "reflection": None
        }

        runtime_logger = self.dependencies.tracing.logger

        runtime_logger.emit(
            ObservabilityEvent(
                event="graph_started",
                request_id=self.dependencies.tracing.request_id,
                data={
                    "query": question,
                    "top_k": top_k,
                },
            )
        )

        final_state = await graph.ainvoke(
            initial_state,
            context=self.dependencies
        )
        
        summary = self.dependencies.tracing.manager.complete(
            confidence=final_state["evaluation"].answer.overall_score,
            selected_attempt=final_state["selected_answer_index"],
        )

        runtime_logger.emit(
            ObservabilityEvent(
                event="graph_finished",
                request_id=self.dependencies.tracing.request_id,
                data={
                    "summary": summary.to_dict()
                },
            )
        )

        total_time = (
            time.perf_counter() - start
        ) * 1000

        logger.info("Exiting GraphService.execute | duration_ms=%.2f | confidence=%.2f", total_time, final_state["evaluation"].answer.overall_score)

        final_state["total_ms"] = total_time

        return QueryResponse(
            answer=final_state["answer"],
            sources=SourceMapper.source_mapper(
                final_state["retrieved_documents"]
            ),
            evaluation=final_state["evaluation"],
            latency=LatencyMetrics(
                retrieval_ms=final_state["retrieval_ms"],
                generation_ms=final_state["generation_ms"],
                evaluation_ms=final_state["evaluation_ms"],
                total_ms=final_state["total_ms"],
            ),
            reflection=final_state["reflection"],
        )
