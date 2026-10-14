"""Spoilage alerts and emergency redistribution schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, UrgencyLevel


class RedistributionCandidate(BaseDomainModel):
    destination_id: str
    destination_name: str
    distance_km: float
    travel_time_hours: float
    unloading_handling_hours: float = 1.0
    total_transit_buffer_hours: float
    remaining_shelf_life_hours: float
    is_feasible: bool
    infeasibility_reason: Optional[str] = None
    buyer_demand_kg: float
    offered_price_per_kg: float
    estimated_net_recovery_inr: float


class SpoilageAlert(BaseDomainModel):
    id: str
    batch_id: str
    batch_code: str
    commodity: str
    quantity_kg: float
    remaining_shelf_life_hours: float
    urgency_level: UrgencyLevel
    storage_condition: str
    procurement_cost_inr: float
    financial_exposure_inr: float
    flagged_at: datetime
    recommended_action: str
    candidates: List[RedistributionCandidate]
