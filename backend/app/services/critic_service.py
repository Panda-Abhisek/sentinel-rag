import logging
import time

from app.langgraph.models import CriticDecision
from app.core.logging_config import LogUtils
from app.services.models import CriticResult

logger = logging.getLogger(__name__)


class CriticService:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def review(
        self,
        question: str,
        answer: str,
        evaluation,
    ) -> CriticResult:

        start = time.perf_counter()
        LogUtils.entry(logger, "CriticService.review")

        prompt = f"""
            You are the quality reviewer for an enterprise Retrieval-Augmented Generation (RAG) system.

            Your task is to decide whether the current answer should be accepted or whether the system should perform another retrieval using a rewritten query.

            Question:
            {question}

            Generated Answer:
            {answer}

            Evaluation Metrics:
            {evaluation.model_dump_json(indent=2)}

            Rules:

            - Return "finish" if the answer is correct, grounded and complete.
            - Return "rewrite" only if another retrieval is likely to improve the answer.
            - Do NOT rewrite simply because the answer could be longer.
            - Keep the rewritten query concise.
            - Return ONLY valid JSON.

            Example:

            {{
                "critic_route": "finish",
                "reason": "The answer is complete and grounded.",
                "confidence": 0.95,
                "rewritten_query": null
            }}

            or

            {{
                "critic_route": "rewrite",
                "reason": "The retrieved context appears incomplete.",
                "confidence": 0.42,
                "rewritten_query": "Explain FastAPI dependency injection"
            }}
            """

        response = await self.llm.generate(prompt)

        # logger.info("Critic response:\n%s", response)

        try:
            ans = response.content
            if "<think>" in ans:
                ans = ans.split("</think>")[-1].strip()
            decision = CriticDecision.model_validate_json(ans)
            LogUtils.exit(logger, "CriticService.review", start, route=decision.critic_route)
            return CriticResult(
                decision=decision,
                token_usage=response.usage
            )

        except Exception:
            logger.exception("Failed to parse critic output.")
            LogUtils.exit(logger, "CriticService.review", start, route="fallback")
            return CriticResult(
                decision= CriticDecision(
                        critic_route="finish",
                        reason="Critic output could not be parsed.",
                        confidence=0.0,
                        rewritten_query=None,
                    ),
                token_usage=response.usage
            )
