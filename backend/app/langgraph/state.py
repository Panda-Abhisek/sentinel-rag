from typing import TypedDict, Optional, List


class SentinelState(TypedDict):
    query: str

    rewritten_query: Optional[str]

    retrieved_documents: List

    answer: Optional[str]

    retry_count: int

    should_retry: bool

    finished: bool