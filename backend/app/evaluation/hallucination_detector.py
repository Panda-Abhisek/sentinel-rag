import logging
import time

from app.evaluation.metrics import RetrievedResults
from app.evaluation.models import HallucinationEvaluation
from app.rag.evaluation_prompt_builder import EvaluationPromptBuilder
from app.services.evaluation_llm import EvaluationLLM
from app.core.config import settings
from app.evaluation.json_parser import parse_json_response

logger = logging.getLogger(__name__)


class HallucinationDetector:

    def __init__(self) -> None:
        self._llm = EvaluationLLM.get_llm()

    async def evaluate(
        self,
        retrieval_results: RetrievedResults,
        answer: str,
    ) -> HallucinationEvaluation:

        start = time.perf_counter()
        logger.info("Entering HallucinationDetector.evaluate")

        contexts = self._extract_contexts(retrieval_results)

        prompt = EvaluationPromptBuilder.build_hallucination_prompt(
            contexts=contexts,
            answer=answer,
        )

        response = await self._llm.ainvoke(prompt)

        logger.info("Raw LLM response:\n%s", response.content)

        evaluation = parse_json_response(
            HallucinationEvaluation,
            response.content,
        )

        logger.info("Exiting HallucinationDetector.evaluate | duration_ms=%.2f", (time.perf_counter() - start) * 1000)

        return evaluation

    @staticmethod
    def _extract_contexts(retrieval_results: RetrievedResults) -> list[str]:
        return [
            document.page_content[:settings.MAX_CONTEXT_DOCUMENTS]
            for document, _ in retrieval_results
        ]
