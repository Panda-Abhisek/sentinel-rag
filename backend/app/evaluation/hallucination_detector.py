import logging
import time

from app.evaluation.metrics import RetrievedResults
from app.evaluation.models import HallucinationEvaluation
from app.rag.evaluation_prompt_builder import EvaluationPromptBuilder
from app.services.evaluation_llm import EvaluationLLM
from app.core.config import settings
from app.evaluation.json_parser import parse_json_response
from app.core.logging_config import LogUtils

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
        LogUtils.entry(logger, "HallucinationDetector.evaluate")

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

        LogUtils.exit(logger, "HallucinationDetector.evaluate", start)

        return evaluation

    @staticmethod
    def _extract_contexts(retrieval_results: RetrievedResults) -> list[str]:
        return [
            document.page_content[:settings.MAX_CONTEXT_DOCUMENTS]
            for document, _ in retrieval_results
        ]
