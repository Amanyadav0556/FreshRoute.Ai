"""Disruption scenario catalog endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.scenario import ScenarioDefinition
from app.services.scenario_runner import get_scenario_definitions

router = APIRouter()


@router.get("", response_model=List[ScenarioDefinition])
async def list_scenarios():
    """Retrieves all 8 disruption scenarios with parameter overrides and provenance indicators."""
    return get_scenario_definitions()


@router.get("/{scenario_id}", response_model=ScenarioDefinition)
async def get_scenario(scenario_id: str):
    """Retrieves a specific disruption scenario by ID."""
    scenarios = get_scenario_definitions()
    scen = next((s for s in scenarios if s["id"] == scenario_id), None)
    if not scen:
        raise HTTPException(status_code=404, detail=f"Disruption scenario {scenario_id} not found.")
    return scen
