import logging
import time

from app.langgraph.models import ReflectionReport
from app.services.models import ReflectionResult

logger = logging.getLogger(__name__)


class ReflectionService:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def reflect(
        self,
        answers: list[str],
        evaluations,
        selected_index: int,
    ) -> ReflectionResult:

        start = time.perf_counter()
        logger.info("Entering ReflectionService.reflect | selected=%d", selected_index)

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

        response = await self.llm.generate(prompt)

        logger.info("Reflection response:\n%s", response)

        try:
            content = response.content
            if "<think>" in content:
                content = content.split("</think>")[-1].strip()
            logger.info("Reflection Content: \n%s", content)
            report = ReflectionReport.model_validate_json(content)
            logger.info("Exiting ReflectionService.reflect | duration_ms=%.2f | confidence=%s", (time.perf_counter() - start) * 1000, report.confidence)
            return ReflectionResult(
                result=report,
                token_usage=response.usage
            )

        except Exception:

            logger.exception("Reflection parsing failed.")

            evaluation = evaluations[selected_index]

            confidence = (
                evaluation.answer.faithfulness
                + evaluation.answer.answer_relevancy
                + evaluation.answer.context_utilization
                + evaluation.answer.completeness
            ) / 4

            logger.info("Exiting ReflectionService.reflect | duration_ms=%.2f | confidence=%s | fallback=%s", (time.perf_counter() - start) * 1000, confidence, True)

            return ReflectionResult(
                result = ReflectionReport(
                        attempts=len(answers),
                        selected_attempt=selected_index + 1,
                        confidence=confidence,
                        reasoning="Reflection fallback.",
                    ),
                token_usage=response.usage
            )
