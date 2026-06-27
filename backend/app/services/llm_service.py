import logging
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Handles all interactions with the Large Language Model.

    Responsibilities:
    - Initialize the LLM
    - Generate grounded responses
    - Hide provider-specific implementation details
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
        )

    def generate(self, prompt: str) -> str:
        """
        Generates an answer from the supplied prompt.

        Args:
            prompt: Fully formatted prompt.

        Returns:
            Generated answer.
        """

        logger.info("Sending prompt to Groq.")

        try:
            response = self.llm.invoke(
                [HumanMessage(content=prompt)]
            )

            logger.info("Received response from Groq.")

            answer = response.content

            answer = re.sub(
                r"<think>.*?</think>",
                "",
                answer,
                flags=re.DOTALL,
            ).strip()

            return answer

        except Exception:
            logger.exception("LLM generation failed.")
            raise