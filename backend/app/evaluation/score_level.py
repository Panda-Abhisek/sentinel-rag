from app.core.config import settings

class ScoreLevel:
    """
    Converts numeric evaluation scores into qualitative levels.
    """

    @staticmethod
    def level(score: float) -> str:
        if score >= settings.EVALUATION_SCORE_HIGH:
            return "HIGH"

        if score >= settings.EVALUATION_SCORE_MEDIUM:
            return "MEDIUM"

        return "LOW"