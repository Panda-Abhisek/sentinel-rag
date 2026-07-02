import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from app.services.retrieval_service import RetrievalService

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

@pytest.fixture
def retrieval_service():
    service = AsyncMock(spec=RetrievalService)
    return service