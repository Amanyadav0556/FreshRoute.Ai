"""Dispatch optimization plan schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.common import BaseDomainModel, AllocationStatus


class PlanRequest(BaseDomainModel):
    strategy: str = Field("balanced", description="balanced, max_margin, min_spoilage, max_volume")
    scenario_id: Optional[str] = Field(None, description="Optional disruption scenario ID to simulate")
    solver_timeout_seconds: int = Field(30, ge=5, le=120)
    enable_emergency_redistribution: bool = Field(True)
    custom_overrides: Optional[Dict[str, Any]] = None


class PlanItem(BaseDomainModel):
    batch_id: str
    batch_code: str
    commodity: str
    destination_id: str
    destination_name: str
    vehicle_id: str
    vehicle_plate: str
    allocated_quantity_kg: float
    offered_price_per_kg: float
    discount_applied_percent: float = 0.0
    effective_selling_price_per_kg: float
    estimated_revenue_inr: float
    estimated_transport_cost_inr: float
    estimated_spoilage_risk_percent: float
    remaining_shelf_life_on_arrival_hours: float
    net_economic_value_inr: float
    dispatch_explanation: str


class PlanValidationCheck(BaseDomainModel):
    rule_name: str
    passed: bool
    details: str
    severity: str = "warning"  # info, warning, critical_error


class PlanValidationResult(BaseDomainModel):
    is_valid: bool
    total_checks: int
    passed_checks: int
    failed_checks: int
    checks: List[PlanValidationCheck]


class PlanResponse(BaseDomainModel):
    id: str
    strategy: str
    scenario_name: str = "Normal Operation"
    solver_used: str = "HiGHS LP/MILP (SciPy)"  # or Greedy Heuristic Fallback
    solver_duration_ms: float
    status: AllocationStatus = AllocationStatus.OPTIMIZED
    total_allocated_kg: float
    total_revenue_inr: float
    total_transport_cost_inr: float
    total_discount_loss_inr: float
    net_economic_value_inr: float
    spoilage_prevented_kg: float
    average_spoilage_risk_percent: float
    total_dispatches: int
    allocations: List[PlanItem]
    validation: PlanValidationResult
    created_at: datetime
