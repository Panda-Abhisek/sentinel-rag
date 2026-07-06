import logging
import time
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.core.logging_config import LogUtils

logger = logging.getLogger(__name__)


class LLMService:

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

        start = time.perf_counter()
        LogUtils.entry(logger, "LLMService.generate", model=settings.LLM_MODEL)

        llm = self.llm

        if temperature is not None or max_tokens is not None:
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

            answer = re.sub(
                r"<think>.*?</think>",
                "",
                response.content,
                flags=re.DOTALL,
            ).strip()

            LogUtils.exit(logger, "LLMService.generate", start, answer_len=len(answer))

            return answer

        except Exception:
            logger.exception("LLM generation failed.")
            raise
