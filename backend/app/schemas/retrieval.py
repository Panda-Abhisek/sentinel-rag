from pydantic import BaseModel

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