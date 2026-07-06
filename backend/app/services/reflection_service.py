import logging

from app.langgraph.models import ReflectionReport

logger = logging.getLogger(__name__)


class ReflectionService:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def reflect(
        self,
        answers: list[str],
        evaluations,
        selected_index: int,
    ) -> ReflectionReport:

        prompt = f"""
            You are the Reflection Agent of an enterprise Retrieval-Augmented Generation system.

            The system generated multiple candidate answers.

            Candidate Answers:

            {answers}

            Evaluation Reports:

            {[evaluation.model_dump() for evaluation in evaluations]}

            Selected Answer Index:
            {selected_index}

            Explain why this answer was selected.

            Return ONLY valid JSON.

            {{
                "attempts": {len(answers)},
                "selected_attempt": {selected_index + 1},
                "confidence": 0.95,
                "reasoning": "..."
            }}
            """

        logger.info("Running reflection agent.")

        response = await self.llm.generate(prompt)

        logger.info(
            "Reflection response:\n%s",
            response,
        )

        try:
            return ReflectionReport.model_validate_json(
                response
            )

        except Exception:

            logger.exception(
                "Reflection parsing failed."
            )

            evaluation = evaluations[selected_index]

            confidence = (
                evaluation.answer.faithfulness
                + evaluation.answer.answer_relevancy
                + evaluation.answer.context_utilization
                + evaluation.answer.completeness
            ) / 4

            return ReflectionReport(
                attempts=len(answers),
                selected_attempt=selected_index + 1,
                confidence=confidence,
                reasoning="Reflection fallback.",
            )