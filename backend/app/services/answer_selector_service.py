import logging
import time

from app.evaluation.models import EvaluationReport

logger = logging.getLogger(__name__)


class AnswerSelectorService:

    def select(
        self,
        answers: list[str],
        evaluations: list[EvaluationReport],
    ) -> int:

        start = time.perf_counter()
        logger.info("Entering AnswerSelectorService.select | candidates=%d", len(answers))

        best_index = 0
        best_score = float("-inf")

        for i, evaluation in enumerate(evaluations):

            score = (
                evaluation.answer.faithfulness
                + evaluation.answer.answer_relevancy
                + evaluation.answer.context_utilization
                + evaluation.answer.completeness
            ) - evaluation.hallucination.hallucination_score

            logger.debug("Candidate %d composite_score=%.2f", i, score)

            if score > best_score:
                best_score = score
                best_index = i

        logger.info("Exiting AnswerSelectorService.select | duration_ms=%.2f | selected=%d | score=%.2f", (time.perf_counter() - start) * 1000, best_index, best_score)
        return best_index
