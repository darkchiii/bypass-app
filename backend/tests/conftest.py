# backend/tests/conftest.py

import sys
from pathlib import Path
import logging
import pytest


backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Skonfiguruj logging dla wszystkich testów"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


@pytest.fixture
def test_client():
    """Stwórz test client dla FastAPI"""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)