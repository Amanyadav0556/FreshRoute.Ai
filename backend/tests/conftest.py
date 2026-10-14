"""Pytest fixtures and test environment setup for FreshRoute AI."""
import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os

# Ensure backend root is in pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.db.sample_data import (
    SAMPLE_BATCHES,
    SAMPLE_DESTINATIONS,
    SAMPLE_VEHICLES,
    SAMPLE_ROUTES,
    SAMPLE_ORDERS,
)


@pytest.fixture
def sample_batches():
    return [dict(b) for b in SAMPLE_BATCHES]


@pytest.fixture
def sample_destinations():
    return [dict(d) for d in SAMPLE_DESTINATIONS]


@pytest.fixture
def sample_vehicles():
    return [dict(v) for v in SAMPLE_VEHICLES]


@pytest.fixture
def sample_routes():
    return [dict(r) for r in SAMPLE_ROUTES]


@pytest.fixture
def sample_orders():
    return [dict(o) for o in SAMPLE_ORDERS]


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
