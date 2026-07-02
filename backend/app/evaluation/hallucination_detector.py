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
    """
    Detects hallucinations by comparing the generated answer
    against the retrieved context.
    """

    def __init__(self) -> None:
        self._llm = EvaluationLLM.get_llm()

    async def evaluate(
        self,
        retrieval_results: RetrievedResults,
        answer: str,
    ) -> HallucinationEvaluation:
        """
        Detect hallucinations in the generated answer.
        """

        start = time.perf_counter()
        
        contexts = self._extract_contexts(
            retrieval_results
        )

        prompt = (
            EvaluationPromptBuilder.build_hallucination_prompt(
                contexts=contexts,
                answer=answer,
            )
        )

        logger.info("Running hallucination detection.")

        response = await self._llm.ainvoke(prompt)
        
        logger.info(
            "Raw LLM response:\n%s",
            response.content,
        )

        evaluation = parse_json_response(
            HallucinationEvaluation,
            response.content,
        )

        logger.info(
            "Hallucination detection completed in %.2f ms.",
            (time.perf_counter() - start) * 1000,
        )

        return evaluation

    @staticmethod
    def _extract_contexts(
        retrieval_results: RetrievedResults,
    ) -> list[str]:
        """
        Extract retrieved contexts.
        """

        return [
            document.page_content[:settings.MAX_CONTEXT_DOCUMENTS]
            for document, _ in retrieval_results
        ]