import asyncio
import logging
import time
from app.evaluation.models import EvaluationReport
from app.evaluation.answer_evaluator import AnswerEvaluator
from app.evaluation.retrieval_evaluator import RetrievalEvaluator
from app.evaluation.metrics import RetrievedResults
from app.evaluation.hallucination_detector import HallucinationDetector

logger = logging.getLogger(__name__)


class EvaluationService:
    """
    Orchestrates all evaluation components.
    """

    def __init__(
        self,
        retrieval_evaluator: RetrievalEvaluator | None = None,
        answer_evaluator: AnswerEvaluator | None = None,
        hallucination_detector: HallucinationDetector | None = None,
    ) -> None:
        self._retrieval_evaluator = (
            retrieval_evaluator or RetrievalEvaluator()
        )
        self._answer_evaluator = (
            answer_evaluator or AnswerEvaluator()
        )
        self._hallucination_detector = (
            hallucination_detector or HallucinationDetector()
        )

    async def evaluate_pipeline(
        self,
        question: str,
        retrieval_results: RetrievedResults,
        answer: str,
    ) -> EvaluationReport:
        """
        Execute all evaluation pipelines and return a unified report.
        """

        logger.info("Starting evaluation pipeline.")
        start = time.perf_counter()
        retrieval_evaluation = self._retrieval_evaluator.evaluate(
            retrieval_results
        )

        # answer_evaluation = await self._answer_evaluator.evaluate(
        #     question=question,
        #     retrieval_results=retrieval_results,
        #     answer=answer,
        # )
        
        # hallucination_evaluation = (
        #     await self._hallucination_detector.evaluate(
        #         retrieval_results=retrieval_results,
        #         answer=answer,
        #     )
        # )
        
        answer_evaluation, hallucination_evaluation = await asyncio.gather(
            self._answer_evaluator.evaluate(
                question=question,
                retrieval_results=retrieval_results,
                answer=answer,
            ),
            self._hallucination_detector.evaluate(
                retrieval_results=retrieval_results,
                answer=answer,
            ),
        )

        logger.info("Evaluation pipeline completed in %.2f ms.",
            (time.perf_counter() - start) * 1000,
        )

        return EvaluationReport(
            retrieval=retrieval_evaluation,
            answer=answer_evaluation,
            hallucination=hallucination_evaluation,
        )