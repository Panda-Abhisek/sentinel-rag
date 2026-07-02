"""
Unit tests for QueryRewriter.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.healing.query_rewriter import QueryRewriter


@pytest.fixture
def llm_service() -> AsyncMock:
    """
    Mock LLM service.
    """
    mock = AsyncMock()
    return mock


@pytest.fixture
def prompt_builder() -> MagicMock:
    """
    Mock rewrite prompt builder.
    """
    return MagicMock()


@pytest.fixture
def query_rewriter(
    llm_service: AsyncMock,
    prompt_builder: MagicMock,
) -> QueryRewriter:
    """
    QueryRewriter under test.
    """
    return QueryRewriter(
        llm_service=llm_service,
        prompt_builder=prompt_builder,
    )


@pytest.mark.asyncio
async def test_successful_query_rewrite(
    query_rewriter: QueryRewriter,
    llm_service: AsyncMock,
    prompt_builder: MagicMock,
) -> None:
    """
    A rewritten query should be returned when the LLM succeeds.
    """

    query = "FastAPI"

    prompt_builder.build.return_value = "rewrite prompt"

    llm_service.generate.return_value = (
        "Explain FastAPI and its use cases."
    )

    rewritten = await query_rewriter.rewrite(query)

    assert rewritten == "Explain FastAPI and its use cases."

    prompt_builder.build.assert_called_once_with(query)

    llm_service.generate.assert_awaited_once_with(
        "rewrite prompt",
        temperature=0.2,
        max_tokens=128,
    )


@pytest.mark.asyncio
async def test_rewrite_strips_whitespace(
    query_rewriter: QueryRewriter,
    llm_service: AsyncMock,
    prompt_builder: MagicMock,
) -> None:
    """
    Leading and trailing whitespace should be removed from the rewritten
    query.
    """

    prompt_builder.build.return_value = "prompt"

    llm_service.generate.return_value = (
        "   Improved query   "
    )

    rewritten = await query_rewriter.rewrite(
        "original"
    )

    assert rewritten == "Improved query"


@pytest.mark.asyncio
async def test_rewrite_returns_original_when_llm_fails(
    query_rewriter: QueryRewriter,
    llm_service: AsyncMock,
    prompt_builder: MagicMock,
) -> None:
    """
    The original query should be returned if the LLM raises an
    exception.
    """

    query = "dependency injection"

    prompt_builder.build.return_value = "prompt"

    llm_service.generate.side_effect = RuntimeError(
        "LLM unavailable"
    )

    rewritten = await query_rewriter.rewrite(query)

    assert rewritten == query


@pytest.mark.asyncio
async def test_rewrite_returns_original_when_prompt_builder_fails(
    query_rewriter: QueryRewriter,
    prompt_builder: MagicMock,
) -> None:
    """
    Failures during prompt construction should fall back to the original
    query.
    """

    query = "dependency injection"

    prompt_builder.build.side_effect = ValueError(
        "Prompt error"
    )

    rewritten = await query_rewriter.rewrite(query)

    assert rewritten == query


@pytest.mark.asyncio
async def test_empty_query_raises_value_error(
    query_rewriter: QueryRewriter,
) -> None:
    """
    Empty queries should be rejected.
    """

    with pytest.raises(ValueError):
        await query_rewriter.rewrite("")


@pytest.mark.asyncio
async def test_whitespace_query_raises_value_error(
    query_rewriter: QueryRewriter,
) -> None:
    """
    Whitespace-only queries should be rejected.
    """

    with pytest.raises(ValueError):
        await query_rewriter.rewrite("     ")


def test_clean_response_removes_whitespace(
    query_rewriter: QueryRewriter,
) -> None:
    """
    The response cleaner should trim surrounding whitespace.
    """

    cleaned = query_rewriter._clean_response(
        "   hello world   "
    )

    assert cleaned == "hello world"


def test_clean_response_handles_empty_string(
    query_rewriter: QueryRewriter,
) -> None:
    """
    Empty responses should remain empty.
    """

    cleaned = query_rewriter._clean_response(
        "     "
    )

    assert cleaned == ""


def test_validate_query_accepts_valid_query(
    query_rewriter: QueryRewriter,
) -> None:
    """
    A valid query should pass validation.
    """

    query_rewriter._validate_query(
        "What is FastAPI?"
    )


def test_validate_query_rejects_empty_query(
    query_rewriter: QueryRewriter,
) -> None:
    """
    Validation should reject empty queries.
    """

    with pytest.raises(ValueError):
        query_rewriter._validate_query("")