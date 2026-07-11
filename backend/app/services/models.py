from dataclasses import dataclass

from app.langgraph.models import CriticDecision, PlannerDecision, ReflectionReport
from app.observability.models import TokenUsage


@dataclass
class PlannerResult:
    decision: PlannerDecision
    token_usage: TokenUsage

@dataclass
class GenerationResult:
    answer: str
    token_usage: TokenUsage

@dataclass
class CriticResult:
    decision: CriticDecision
    token_usage: TokenUsage

@dataclass
class ReflectionResult:
    result: ReflectionReport
    token_usage: TokenUsage

@dataclass
class RewriteResult:
    rewritten_query: str
    token_usage: TokenUsage