import logging
import time

from app.evaluation.models import AnswerEvaluation
from app.evaluation.metrics import RetrievedResults
from app.services.evaluation_llm import EvaluationLLM
from app.rag.evaluation_prompt_builder import EvaluationPromptBuilder
from app.core.config import settings
from app.evaluation.json_parser import parse_json_response
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


class AnswerEvaluator:

    def __init__(self) -> None:
        self._llm = EvaluationLLM.get_llm()

    async def evaluate(
        self,
        question: str,
        retrieval_results: RetrievedResults,
        answer: str,
    ) -> AnswerEvaluation:

        start = time.perf_counter()
        LogUtils.entry(logger, "AnswerEvaluator.evaluate")

        contexts = [
            document.page_content[:settings.EVALUATION_MAX_CONTEXT_LENGTH]
            for document, _ in retrieval_results[:settings.EVALUATION_MAX_RETRIEVAL_RESULTS]
        ]

        prompt = EvaluationPromptBuilder.build_answer_evaluation_prompt(
            question=question,
            contexts=contexts,
            answer=answer,
        )

        response = await self._llm.ainvoke(prompt)

        logger.info(
            "Raw LLM response:\n%s",
            response.content,
        )

        evaluation = parse_json_response(
            AnswerEvaluation,
            response.content,
        )

        LogUtils.exit(logger, "AnswerEvaluator.evaluate", start)

        return evaluation
