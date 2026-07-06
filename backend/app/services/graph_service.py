import time

from app.langgraph.graph import graph
from app.langgraph.dependencies import SentinelContext
from app.langgraph.state import SentinelState
from app.services.response_service import ResponseBuilder


class GraphService:

    def __init__(self, dependencies: SentinelContext):
        self.dependencies = dependencies

    async def execute(
        self,
        question: str,
        top_k: int,
    ):
        request_start = time.perf_counter()

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
        }

        final_state = await graph.ainvoke(
            initial_state,
            context=self.dependencies
        )

        total_time = (
            time.perf_counter() - request_start
        ) * 1000

        final_state["total_ms"] = total_time

        return ResponseBuilder.build_query_response(
            answer=final_state["answer"],
            documents=final_state["retrieved_documents"],
            evaluation=final_state["evaluation"],
            retrieval_ms=final_state["retrieval_ms"],
            generation_ms=final_state["generation_ms"],
            evaluation_ms=final_state["evaluation_ms"],
            total_ms=final_state["total_ms"],
        )