"""Integration tests for FastAPI HTTP endpoints."""
from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "FreshRoute AI" in data["service"]


def test_dashboard_endpoint(client: TestClient):
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_inventory_kg"] > 0
    assert len(data["shelf_life_distribution"]) == 4


def test_list_batches_endpoint(client: TestClient):
    response = client.get("/api/batches")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) > 0
    assert "batch_code" in batches[0]


def test_plan_optimize_endpoint(client: TestClient):
    payload = {"strategy": "balanced", "solver_timeout_seconds": 15}
    response = client.post("/api/plans/optimize", json=payload)
    assert response.status_code == 200
    plan = response.json()
    assert plan["strategy"] == "balanced"
    assert len(plan["allocations"]) > 0
    assert plan["validation"]["is_valid"] is True
