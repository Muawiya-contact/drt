"""Shared pytest fixtures for drt tests."""

import pytest


@pytest.fixture
def sample_row() -> dict:
    return {"name": "Alice", "email": "alice@example.com", "id": 42}
