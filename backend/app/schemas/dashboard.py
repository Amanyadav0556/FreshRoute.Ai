"""Dashboard metrics, shelf life distribution, and live KPI schemas."""
from pydantic import Field
from typing import Optional, List, Dict
from datetime import datetime
from app.schemas.common import BaseDomainModel


class ShelfLifeBucket(BaseDomainModel):
    range_label: str  # "< 12h", "12-24h", "24-48h", "> 48h"
    quantity_kg: float
    percentage: float
    batch_count: int
    urgency_color: str


class CommodityBreakdown(BaseDomainModel):
    commodity: str
    total_quantity_kg: float
    allocated_quantity_kg: float
    unallocated_quantity_kg: float
    avg_shelf_life_hours: float
    at_risk_quantity_kg: float


class DashboardMetrics(BaseDomainModel):
    total_inventory_kg: float
    at_risk_inventory_kg: float
    at_risk_percentage: float
    potential_financial_loss_inr: float
    optimized_savings_inr: float
    active_vehicles_count: int
    available_vehicles_count: int
    active_orders_count: int
    unfulfilled_demand_kg: float
    shelf_life_distribution: List[ShelfLifeBucket]
    commodity_summary: List[CommodityBreakdown]
    last_updated: datetime
