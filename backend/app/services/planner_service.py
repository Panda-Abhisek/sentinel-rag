import logging
import time

from pydantic import BaseModel
from typing import Literal

from app.services.models import PlannerResult
from app.langgraph.models import PlannerDecision

logger = logging.getLogger(__name__)

class PlannerService:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def plan(
        self,
        question: str,
    ) -> PlannerResult:

        start = time.perf_counter()
        logger.info("Entering PlannerService.plan")

        prompt = f"""
            You are the Planner Agent for an enterprise Retrieval-Augmented Generation (RAG) system.

            Your responsibility is to decide whether the user's query should be retrieved directly
            or rewritten before retrieval.

            Choose "retrieve" if:
            - The question is clear.
            - The intent is specific.
            - Direct semantic retrieval is likely to work well.

            Choose "rewrite" if:
            - The question is broad.
            - The question compares multiple topics.
            - The question contains multiple sub-questions.
            - The wording is ambiguous.
            - A rewritten search query would likely improve retrieval quality.

            User Question:
            {question}

            Return ONLY valid JSON.

            Example 1:
            {{
                "planner_route": "retrieve",
                "reason": "The question is clear and suitable for direct retrieval."
            }}

            Example 2:
            {{
                "planner_route": "rewrite",
                "reason": "The query contains multiple concepts that should be clarified before retrieval."
            }}
            """

        response = await self.llm.generate(prompt)

        logger.info("Planner response:\n%s", response)
        
        logger.info("Planner response content:\n%s", response.content)

        try:
            ans = response.content
            if "<think>" in ans:
                ans = ans.split("</think>")[-1].strip()
            decision = PlannerDecision.model_validate_json(ans)
            logger.info("Planner Decision: \n%s", decision)
            logger.info("Exiting PlannerService.plan | duration_ms=%.2f | route=%s", (time.perf_counter() - start) * 1000, decision.planner_route)
            return PlannerResult(
                decision=decision,
                token_usage=response.usage,
            )

        except Exception:
            logger.exception("Failed to parse planner output.")
            logger.info("Exiting PlannerService.plan | duration_ms=%.2f | route=%s", (time.perf_counter() - start) * 1000, "fallback")
            return PlannerResult(
                decision=PlannerDecision(
                    planner_route="retrieve",
                    reason="Planner output could not be parsed. Falling back to direct retrieval.",
                ),
                token_usage=response.usage,
            )
