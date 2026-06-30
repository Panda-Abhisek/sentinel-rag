import logging

from app.evaluation.metrics import RetrievedResults
from app.evaluation.models import HallucinationEvaluation
from app.rag.evaluation_prompt_builder import EvaluationPromptBuilder
from app.services.evaluation_llm import EvaluationLLM

logger = logging.getLogger(__name__)


class HallucinationDetector:
    """
    Detects hallucinations by comparing the generated answer
    against the retrieved context.
    """

    def __init__(self) -> None:
        self._llm = EvaluationLLM.get_llm().with_structured_output(
            HallucinationEvaluation
        )

    async def evaluate(
        self,
        retrieval_results: RetrievedResults,
        answer: str,
    ) -> HallucinationEvaluation:
        """
        Detect hallucinations in the generated answer.
        """

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

        evaluation = await self._llm.ainvoke(prompt)

        logger.info("Hallucination detection completed.")

        return evaluation

    @staticmethod
    def _extract_contexts(
        retrieval_results: RetrievedResults,
    ) -> list[str]:
        """
        Extract retrieved contexts.
        """

        return [
            document.page_content
            for document, _ in retrieval_results
        ]