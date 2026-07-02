"""
Unit tests for RetryStrategy.
"""

from unittest.mock import AsyncMock

import pytest

from app.healing.retry_strategy import RetryStrategy
from app.healing.query_rewriter import QueryRewriter


@pytest.fixture
def query_rewriter() -> AsyncMock:
    """
    Mock QueryRewriter.
    """
    return AsyncMock(spec=QueryRewriter)


@pytest.fixture
def retry_strategy(
    query_rewriter: AsyncMock,
) -> RetryStrategy:
    """
    RetryStrategy under test.
    """
    return RetryStrategy(
        query_rewriter=query_rewriter,
    )


@pytest.mark.asyncio
async def test_retry_returns_rewritten_query(
    retry_strategy: RetryStrategy,
    query_rewriter: AsyncMock,
) -> None:
    """
    Retry should return the rewritten query.
    """

    query_rewriter.rewrite.return_value = (
        "Explain dependency injection in FastAPI."
    )

    rewritten = await retry_strategy.retry(
        "dependency injection"
    )

    assert (
        rewritten
        == "Explain dependency injection in FastAPI."
    )

    query_rewriter.rewrite.assert_awaited_once_with(
        "dependency injection"
    )


@pytest.mark.asyncio
async def test_retry_preserves_original_when_rewriter_returns_original(
    retry_strategy: RetryStrategy,
    query_rewriter: AsyncMock,
) -> None:
    """
    Retry should return the original query when no rewrite occurs.
    """

    query = "FastAPI"

    query_rewriter.rewrite.return_value = query

    rewritten = await retry_strategy.retry(query)

    assert rewritten == query


@pytest.mark.asyncio
async def test_retry_propagates_rewriter_result(
    retry_strategy: RetryStrategy,
    query_rewriter: AsyncMock,
) -> None:
    """
    RetryStrategy should simply return the QueryRewriter output.
    """

    expected = "What is dependency injection?"

    query_rewriter.rewrite.return_value = expected

    result = await retry_strategy.retry("DI")

    assert result == expected


@pytest.mark.asyncio
async def test_retry_rejects_empty_query(
    retry_strategy: RetryStrategy,
) -> None:
    """
    Empty queries should raise ValueError.
    """

    with pytest.raises(ValueError):
        await retry_strategy.retry("")


@pytest.mark.asyncio
async def test_retry_rejects_whitespace_query(
    retry_strategy: RetryStrategy,
) -> None:
    """
    Whitespace-only queries should raise ValueError.
    """

    with pytest.raises(ValueError):
        await retry_strategy.retry("      ")


def test_validate_query_accepts_valid_query(
    retry_strategy: RetryStrategy,
) -> None:
    """
    Valid queries should pass validation.
    """

    retry_strategy._validate_query(
        "dependency injection"
    )


def test_validate_query_rejects_empty_query(
    retry_strategy: RetryStrategy,
) -> None:
    """
    Validation should reject empty queries.
    """

    with pytest.raises(ValueError):
        retry_strategy._validate_query("")