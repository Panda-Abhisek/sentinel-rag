from app.evaluation.models import EvaluationReport


class AnswerSelectorService:

    def select(
        self,
        answers: list[str],
        evaluations: list[EvaluationReport],
    ) -> int:

        best_index = 0
        best_score = float("-inf")

        for i, evaluation in enumerate(evaluations):

            score = (
                evaluation.answer.faithfulness
                + evaluation.answer.answer_relevancy
                + evaluation.answer.context_utilization
                + evaluation.answer.completeness
            ) - evaluation.hallucination.hallucination_score

            if score > best_score:
                best_score = score
                best_index = i

        return best_index