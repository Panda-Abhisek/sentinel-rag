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
            temperature=settings.GENERATION_TEMPERATURE,
            max_tokens=settings.GENERATION_MAX_TOKENS,
        )

    async def generate(
        self,
        prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """
        Generate a response from the configured language model.

        Optional generation parameters override the default model
        configuration for a single request.
        """

        logger.info("Sending prompt to Groq.")

        llm = self.llm

        if (
            temperature is not None
            or max_tokens is not None
        ):
            llm = ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model=settings.LLM_MODEL,
                temperature=(
                    temperature
                    if temperature is not None
                    else settings.GENERATION_TEMPERATURE
                ),
                max_tokens=(
                    max_tokens
                    if max_tokens is not None
                    else settings.GENERATION_MAX_TOKENS
                ),
            )

        try:
            response = await llm.ainvoke(
                [HumanMessage(content=prompt)]
            )

            logger.info("Received response from Groq.")

            answer = re.sub(
                r"<think>.*?</think>",
                "",
                response.content,
                flags=re.DOTALL,
            ).strip()

            return answer

        except Exception:
            logger.exception("LLM generation failed.")
            raise