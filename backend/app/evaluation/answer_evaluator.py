import logging

from langchain_core.documents import Document

from app.evaluation.models import AnswerEvaluation
from app.evaluation.metrics import RetrievedResults
from app.services.evaluation_llm import EvaluationLLM
from app.rag.evaluation_prompt_builder import EvaluationPromptBuilder
from app.core.config import settings

logger = logging.getLogger(__name__)


class AnswerEvaluator:
    """
    Evaluates the quality of a generated answer using an LLM-as-a-Judge.
    """

    def __init__(self) -> None:
        self._llm = EvaluationLLM.get_llm().with_structured_output(
            AnswerEvaluation
        )

    async def evaluate(
        self,
        question: str,
        retrieval_results: RetrievedResults,
        answer: str,
    ) -> AnswerEvaluation:
        """
        Evaluate the generated answer.
        """

        contexts = [
            document.page_content[:settings.EVALUATION_MAX_CONTEXT_LENGTH]
            for document, _ in retrieval_results[:settings.EVALUATION_MAX_RETRIEVAL_RESULTS]
        ]

        prompt = EvaluationPromptBuilder.build_answer_evaluation_prompt(
            question=question,
            contexts=contexts,
            answer=answer,
        )

        logger.info("Running answer evaluation.")

        evaluation = await self._llm.ainvoke(prompt)
        # print(evaluation)

        logger.info("Answer evaluation completed.")

        return evaluation
