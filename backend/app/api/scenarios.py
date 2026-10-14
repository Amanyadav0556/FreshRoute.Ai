"""Disruption scenario catalog endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.services.scenario_runner import get_scenario_definitions

router = APIRouter()


def format_scenario(s: Dict[str, Any]) -> Dict[str, Any]:
    cat = s.get("category", "normal")
    type_map = {
        "infrastructure": "travel_time_increased",
        "weather": "shelf_life_reduced",
        "market_shock": "demand_increased",
        "operational": "vehicle_unavailable",
    }
    return {
        "id": s["id"],
        "name": s["name"],
        "description": s["description"],
        "category": cat,
        "scenario_type": type_map.get(cat, "normal"),
        "severity": s.get("severity", "medium"),
        "parameter_overrides": s.get("parameter_overrides", []),
        "is_held_out": False,
        "is_active": s.get("is_active", False),
        "impact_summary": s.get("impact_summary", ""),
        "provenance": s.get("provenance", "simulated"),
    }


@router.get("")
async def list_scenarios() -> List[Dict[str, Any]]:
    """Retrieves all 8 disruption scenarios with parameter overrides and provenance indicators."""
    scenarios = get_scenario_definitions()
    return [format_scenario(s) for s in scenarios]


@router.get("/{scenario_id}")
async def get_scenario(scenario_id: str) -> Dict[str, Any]:
    """Retrieves a specific disruption scenario by ID."""
    scenarios = get_scenario_definitions()
    scen = next((s for s in scenarios if s["id"] == scenario_id), None)
    if not scen:
        raise HTTPException(status_code=404, detail=f"Disruption scenario {scenario_id} not found.")
    return format_scenario(scen)
