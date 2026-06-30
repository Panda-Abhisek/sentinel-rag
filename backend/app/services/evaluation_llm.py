import logging

from langchain_openai import ChatOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class EvaluationLLM:
    """
    Singleton service responsible for providing the evaluation LLM.

    This model is used exclusively for:
    - RAGAS
    - DeepEval
    - G-Eval
    - Future evaluation pipelines
    """

    _instance: ChatOpenAI | None = None

    @classmethod
    def get_llm(cls) -> ChatOpenAI:
        """
        Returns a singleton instance of the evaluation LLM.
        """

        if cls._instance is None:
            logger.info("Initializing NVIDIA Evaluation LLM.")

            cls._instance = ChatOpenAI(
                model=settings.EVALUATION_MODEL,
                api_key=settings.NVIDIA_API_KEY,
                base_url="https://integrate.api.nvidia.com/v1",
                temperature=0.0,
                max_tokens=2048,
            )

            logger.info("Evaluation LLM initialized successfully.")

        return cls._instance