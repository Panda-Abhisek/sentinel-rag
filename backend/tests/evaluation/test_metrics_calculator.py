from langchain_core.documents import Document

from app.evaluation.metrics import MetricsCalculator


def sample_results():
    return [
        (
            Document(
                page_content="FastAPI is a web framework.",
                metadata={"source": "doc1.pdf"},
            ),
            0.90,
        ),
        (
            Document(
                page_content="HTTPException handles errors.",
                metadata={"source": "doc1.pdf"},
            ),
            0.80,
        ),
        (
            Document(
                page_content="Dependency Injection example.",
                metadata={"source": "doc2.pdf"},
            ),
            0.70,
        ),
    ]


def test_metrics_calculation():
    calculator = MetricsCalculator()

    metrics = calculator.calculate(sample_results())

    assert metrics.retrieved_documents == 3
    assert metrics.unique_sources == 2

    assert metrics.max_similarity == 0.90
    assert metrics.min_similarity == 0.70
    assert metrics.average_similarity > 0

    assert metrics.average_chunk_length > 0
    assert metrics.duplicate_ratio == 0.0


def test_empty_results():
    calculator = MetricsCalculator()

    metrics = calculator.calculate([])

    assert metrics.retrieved_documents == 0
    assert metrics.unique_sources == 0
    assert metrics.average_similarity == 0.0