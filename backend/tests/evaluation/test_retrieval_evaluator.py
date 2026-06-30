from langchain_core.documents import Document

from app.evaluation.retrieval_evaluator import RetrievalEvaluator


def test_retrieval_evaluation():
    evaluator = RetrievalEvaluator()

    documents = [
        (
            Document(
                page_content="FastAPI tutorial",
                metadata={"source": "fastapi.pdf"},
            ),
            0.85,
        ),
        (
            Document(
                page_content="Dependency injection",
                metadata={"source": "fastapi.pdf"},
            ),
            0.80,
        ),
    ]

    report = evaluator.evaluate(documents)

    assert report.metrics.retrieved_documents == 2
    assert report.metrics.unique_sources == 1
    assert report.confidence.level in {
        "HIGH",
        "MEDIUM",
        "LOW",
    }