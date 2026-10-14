"""Integration tests for FastAPI HTTP endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "FreshRoute AI" in data["service"]


@pytest.mark.asyncio
async def test_dashboard_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_inventory_kg"] > 0
    assert len(data["shelf_life_distribution"]) == 4


@pytest.mark.asyncio
async def test_list_batches_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/batches")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) > 0
    assert "batch_code" in batches[0]


@pytest.mark.asyncio
async def test_plan_optimize_endpoint(async_client: AsyncClient):
    payload = {"strategy": "balanced", "solver_timeout_seconds": 15}
    response = await async_client.post("/api/plans/optimize", json=payload)
    assert response.status_code == 200
    plan = response.json()
    assert plan["strategy"] == "balanced"
    assert len(plan["allocations"]) > 0
    assert plan["validation"]["is_valid"] is True
