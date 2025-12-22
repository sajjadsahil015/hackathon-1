"""Pytest configuration and fixtures for RAG chatbot tests."""

import os
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set test environment variables before importing app
os.environ.setdefault("GOOGLE_API_KEY", "test_api_key")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("DEBUG", "true")


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    from rag_chatbot.main import app
    return TestClient(app)


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_api_key")
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
    monkeypatch.setenv("RELEVANCE_THRESHOLD", "0.7")
    monkeypatch.setenv("DEBUG", "true")


@pytest.fixture
def sample_query_request():
    """Sample query request for testing."""
    return {
        "question": "What is sensor fusion in humanoid robots?",
        "mode": "full_book",
    }


@pytest.fixture
def sample_selected_text_request():
    """Sample selected text query request for testing."""
    return {
        "question": "What does this mean?",
        "mode": "selected_text",
        "selected_text": (
            "Sensor fusion combines data from multiple sensors to produce "
            "more accurate estimates than any single sensor could provide alone."
        ),
    }


@pytest.fixture
def sample_chunk_data():
    """Sample chunk data for testing."""
    return {
        "id": "test-chunk-1",
        "text": "Sensor fusion in humanoid robots combines data from IMUs, cameras, and force sensors.",
        "chapter_number": 5,
        "chapter_title": "Perception and Sensing",
        "section_number": 3,
        "section_title": "Multi-Sensor Integration",
        "page_start": 142,
        "page_end": 145,
        "chunk_index": 0,
        "score": 0.89,
    }
