import logging

from app.evaluation.models import EvaluationReport
from app.evaluation.score_level import ScoreLevel

logger = logging.getLogger(__name__)


class EvaluationLogger:
    """
    Logs retrieval and answer evaluation metrics.
    """

    @staticmethod
    def log(evaluation: EvaluationReport) -> None:
        logger.info("=" * 60)
        logger.info("Evaluation Summary")
        logger.info("=" * 60)

        # ---------------------------------------------------------
        # Retrieval Evaluation
        # ---------------------------------------------------------
        logger.info("Retrieval Evaluation")

        logger.info(
            "  Confidence          : %.2f (%s)",
            evaluation.retrieval.confidence.score,
            evaluation.retrieval.confidence.level,
        )

        logger.info(
            "  Avg Similarity      : %.3f",
            evaluation.retrieval.metrics.average_similarity,
        )

        logger.info(
            "  Max Similarity      : %.3f",
            evaluation.retrieval.metrics.max_similarity,
        )

        logger.info(
            "  Retrieved Docs      : %d",
            evaluation.retrieval.metrics.retrieved_documents,
        )

        logger.info(
            "  Unique Sources      : %d",
            evaluation.retrieval.metrics.unique_sources,
        )

        logger.info(
            "  Duplicate Ratio     : %.2f",
            evaluation.retrieval.metrics.duplicate_ratio,
        )

        if evaluation.retrieval.warnings:
            logger.warning(
                "  Warnings            : %s",
                ", ".join(evaluation.retrieval.warnings),
            )
        else:
            logger.info("  Warnings            : None")

        # ---------------------------------------------------------
        # Answer Evaluation
        # ---------------------------------------------------------
        logger.info("-" * 60)
        logger.info("Answer Evaluation")

        logger.info(
            "  Faithfulness        : %.2f (%s)",
            evaluation.answer.faithfulness,
            ScoreLevel.level(evaluation.answer.faithfulness),
        )

        logger.info(
            "  Answer Relevancy    : %.2f (%s)",
            evaluation.answer.answer_relevancy,
            ScoreLevel.level(evaluation.answer.answer_relevancy),
        )

        logger.info(
            "  Context Utilization : %.2f (%s)",
            evaluation.answer.context_utilization,
            ScoreLevel.level(evaluation.answer.context_utilization),
        )

        logger.info(
            "  Completeness        : %.2f (%s)",
            evaluation.answer.completeness,
            ScoreLevel.level(evaluation.answer.completeness),
        )

        logger.info(
            "  Overall Score       : %.2f (%s)",
            evaluation.answer.overall_score,
            ScoreLevel.level(evaluation.answer.overall_score),
        )

        logger.info("=" * 60)
        logger.info("Hallucination Detection")

        logger.info(
            "  Hallucination Score : %.2f",
            evaluation.hallucination.hallucination_score,
        )

        logger.info(
            "  Risk Level          : %s",
            evaluation.hallucination.risk_level,
        )

        logger.info(
            "  Grounded            : %s",
            "YES" if evaluation.hallucination.grounded else "NO",
        )