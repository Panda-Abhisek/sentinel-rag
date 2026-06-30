from pydantic import BaseModel

from app.evaluation.models import EvaluationReport, LatencyMetrics

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    
    
class SourceDocument(BaseModel):
    page: int
    source: str
    score: float | None = None
    content: str
    
class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
    evaluation: EvaluationReport | None = None
    latency: LatencyMetrics