"""
Utilities for generating JSON output contracts from Pydantic models.
"""

from enum import Enum
from typing import Any, get_args, get_origin

from pydantic import BaseModel


def build_json_contract(
    model: type[BaseModel],
) -> str:
    """
    Build a human-readable JSON contract from a Pydantic model.

    The generated contract is intended for prompt engineering rather
    than machine validation. It describes the expected JSON fields and
    their value types without providing example values.

    Parameters
    ----------
    model:
        Pydantic model describing the expected JSON response.

    Returns
    -------
    str
        JSON contract suitable for inclusion in LLM prompts.
    """

    lines = [
        "Return ONLY one valid JSON object.",
        "",
        "The JSON must contain exactly these fields:",
        "",
        "{",
    ]

    fields = list(model.model_fields.items())

    for index, (name, field) in enumerate(fields):
        field_type = _describe_type(field.annotation)
        comma = "," if index < len(fields) - 1 else ""
        lines.append(f'  "{name}": {field_type}{comma}')

    lines.extend(
        [
            "}",
            "",
            "Rules:",
            "- Compute every value from the supplied context.",
            "- Do NOT copy this template.",
            "- Do NOT include markdown.",
            "- Do NOT include explanations.",
            "- Do NOT include code fences.",
            "- Do NOT include additional keys.",
        ]
    )

    return "\n".join(lines)


def _describe_type(annotation: Any) -> str:
    """
    Convert a Python type annotation into an LLM-friendly description.
    """

    origin = get_origin(annotation)

    if origin is not None:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]

        if args:
            return _describe_type(args[0])

    if annotation is float:
        return "<float between 0.0 and 1.0>"

    if annotation is int:
        return "<integer>"

    if annotation is bool:
        return "<true | false>"

    if annotation is str:
        return "<string>"

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        values = " | ".join(member.value for member in annotation)
        return f"<{values}>"

    return "<value>"