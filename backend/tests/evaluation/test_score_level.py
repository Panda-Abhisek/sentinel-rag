from app.evaluation.score_level import ScoreLevel


def test_returns_high_for_high_scores():
    assert ScoreLevel.level(0.90) == "HIGH"
    assert ScoreLevel.level(1.00) == "HIGH"


def test_returns_medium_for_medium_scores():
    assert ScoreLevel.level(0.65) == "MEDIUM"
    assert ScoreLevel.level(0.80) == "MEDIUM"


def test_returns_low_for_low_scores():
    assert ScoreLevel.level(0.40) == "LOW"
    assert ScoreLevel.level(0.00) == "LOW"


def test_boundary_values():
    assert ScoreLevel.level(0.85) == "HIGH"
    assert ScoreLevel.level(0.6499) == "LOW"