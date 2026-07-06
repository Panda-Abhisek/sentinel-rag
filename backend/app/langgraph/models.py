from typing import Literal

from pydantic import BaseModel


class CriticDecision(BaseModel):
    critic_route: Literal["finish", "rewrite"]
    reason: str
    confidence: float
    rewritten_query: str | None = None
    
class PlannerDecision(BaseModel):
    planner_route: Literal["retrieve", "rewrite"]
    reason: str