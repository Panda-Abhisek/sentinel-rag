from pydantic import BaseModel, Field, computed_field
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def priority(self) -> int:
        priorities = {
            RiskLevel.LOW: 0,
            RiskLevel.MEDIUM: 1,
            RiskLevel.HIGH: 2,
        }
        return priorities[self]
    
class RetrievalMetrics(BaseModel):
    average_similarity: float
    max_similarity: float
    min_similarity: float
    similarity_std: float

    retrieved_documents: int
    unique_sources: int

    average_chunk_length: float
    duplicate_ratio: float
    
class ConfidenceScore(BaseModel):
    score: float
    level: str
    
class LatencyMetrics(BaseModel):
    retrieval_ms: float
    generation_ms: float
    evaluation_ms: float
    total_ms: float
    
class RetrievalEvaluation(BaseModel):
    confidence: ConfidenceScore
    metrics: RetrievalMetrics
    warnings: list[str] = Field(default_factory=list)


class AnswerEvaluation(BaseModel):
    faithfulness: float
    answer_relevancy: float
    context_utilization: float
    completeness: float

    @computed_field
    @property
    def overall_score(self) -> float:
        return round(
            (
                self.faithfulness
                + self.answer_relevancy
                + self.context_utilization
                + self.completeness
            ) / 4,
            2,
        )
    
    
class HallucinationEvaluation(BaseModel):
    hallucination_score: float

    @computed_field
    @property
    def risk_level(self) -> RiskLevel:
        if self.hallucination_score <= 0.20:
            return RiskLevel.LOW

        if self.hallucination_score <= 0.50:
            return RiskLevel.MEDIUM

        return RiskLevel.HIGH

    @computed_field
    @property
    def grounded(self) -> bool:
        return self.hallucination_score <= 0.20
    
    
    
class EvaluationReport(BaseModel):
    retrieval: RetrievalEvaluation
    answer: AnswerEvaluation | None = None
    hallucination: HallucinationEvaluation | None = None