from enum import Enum

from pydantic import BaseModel, Field

from app.evaluation.models import EvaluationReport
from app.schemas.retrieval import QueryResponse

class RetryReason(str, Enum):
    LOW_RETRIEVAL_CONFIDENCE = "low_retrieval_confidence"
    HIGH_HALLUCINATION_RISK = "high_hallucination_risk"
    LOW_ANSWER_QUALITY = "low_answer_quality"
    DUPLICATE_CONTEXT = "duplicate_context"
    UNKNOWN = "unknown"
    
class SelectedAnswer(str, Enum):
    ORIGINAL = "original"
    HEALED = "healed"

class HealingDecision(BaseModel):
    should_retry: bool
    rewrite_query: bool = True
    retry_reason: RetryReason | None = None
    max_attempts: int = Field(default=1, ge=1)
    
class WinnerReason(str, Enum):
    HIGHER_ANSWER_QUALITY = "higher_answer_quality"
    LOWER_HALLUCINATION = "lower_hallucination"
    HIGHER_RETRIEVAL_CONFIDENCE = "higher_retrieval_confidence"
    ORIGINAL_RETAINED = "original_retained"
    
class HealingReport(BaseModel):
    original_query: str = Field(description="Original user query.")
    
    rewritten_query: str | None = None
    
    healing_attempted: bool = False
    healing_success: bool = False
    
    retry_count: int = 0
    retry_reason: RetryReason | None = Field(
        default=None,
        description="Reason the healing pipeline decided to retry."
    )
    
    selected_answer: SelectedAnswer | None = None
    winner_reason: WinnerReason | None = None
    
    original_score: float = Field(ge=0.0, le=1.0)
    healed_score: float | None = Field(default=None,ge=0.0,le=1.0,)
    
    latency_overhead_ms: float = Field(default=0.0,ge=0.0,)
    
class HealingResponse(BaseModel):
    response: QueryResponse
    healing: HealingReport
    
class SelectionResult(BaseModel):
    response: QueryResponse
    selected_answer: SelectedAnswer
    winner_reason: WinnerReason