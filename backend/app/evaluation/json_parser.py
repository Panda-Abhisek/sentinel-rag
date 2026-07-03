"""
Utilities for parsing structured JSON responses returned by LLMs.
"""

from __future__ import annotations

import json
import logging
import re

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


def parse_json_response(
    model: type[BaseModel],
    text: str,
) -> BaseModel:
    """
    Parse an LLM response into a validated Pydantic model.

    The parser automatically removes Markdown code fences and extracts
    the first JSON object before performing validation.

    Parameters
    ----------
    model:
        Target Pydantic model.

    text:
        Raw response returned by the language model.

    Returns
    -------
    BaseModel
        Validated Pydantic model instance.

    Raises
    ------
    ValueError
        If the response cannot be parsed into the requested model.
    """

    cleaned = _extract_json(text)

    try:
        return model.model_validate_json(cleaned)

    except ValidationError as exc:
        logger.error(
            "Invalid JSON returned for %s:\n%s",
            model.__name__,
            text,
        )
        raise ValueError(
            f"Invalid JSON response for {model.__name__}."
        ) from exc

    except json.JSONDecodeError as exc:
        logger.error(
            "Malformed JSON returned by LLM:\n%s",
            text,
        )
        raise ValueError(
            "Malformed JSON returned by LLM."
        ) from exc


def _extract_json(
    text: str,
) -> str:
    """
    Extract the first JSON object from an LLM response.

    Handles responses wrapped in Markdown code fences or surrounded by
    additional explanatory text.

    Parameters
    ----------
    text:
        Raw LLM response.

    Returns
    -------
    str
        Extracted JSON string.

    Raises
    ------
    ValueError
        If no JSON object is found.
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    raise ValueError("No JSON object found in LLM response.")