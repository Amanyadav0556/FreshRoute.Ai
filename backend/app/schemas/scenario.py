"""Disruption scenario and parameter override schemas."""
from pydantic import Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin


class ScenarioParameterOverride(BaseDomainModel):
    parameter_key: str
    parameter_label: str
    default_value: Any
    override_value: Any
    unit: str
    provenance: str = "simulated"


class ScenarioDefinition(BaseDomainModel, ProvenanceMixin):
    id: str
    name: str
    category: str = Field(..., description="weather, infrastructure, market_shock, operational")
    description: str
    severity: str = "medium"  # low, medium, high, severe
    is_active: bool = False
    parameter_overrides: List[ScenarioParameterOverride]
    impact_summary: str


class ScenarioRunRequest(BaseDomainModel):
    scenario_id: str
    temporary_overrides: Optional[Dict[str, Any]] = None
