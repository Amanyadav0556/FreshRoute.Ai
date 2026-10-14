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

    response_summary = client.get("/api/dashboard/summary")
    assert response_summary.status_code == 200
    assert response_summary.json()["total_inventory_kg"] > 0


def test_list_batches_endpoint(client: TestClient):
    response = client.get("/api/batches")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0
    assert "batch_code" in data["items"][0]


def test_plan_optimize_endpoint(client: TestClient):
    payload = {"strategy": "freshroute", "solver_timeout_seconds": 15}
    response = client.post("/api/plans", json=payload)
    assert response.status_code == 200
    plan = response.json()
    assert plan["strategy"] == "freshroute"
    assert len(plan["recommendations"]) > 0
    assert plan["status"] == "valid"
