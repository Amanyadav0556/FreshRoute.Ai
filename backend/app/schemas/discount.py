"""Discount optimization and dynamic pricing schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin


class DiscountOption(BaseDomainModel):
    strategy_key: str = Field(..., description="no_discount, dynamic_10, clearance_20, salvage_35, elasticity_based, auction_processor, donation_tax")
    strategy_label: str = Field(..., description="Human-friendly label")
    discount_percent: float = Field(..., ge=0.0, le=100.0)
    proposed_price_per_kg: float = Field(..., ge=0.0)
    expected_clearance_kg: float = Field(..., ge=0.0)
    expected_revenue_inr: float = Field(..., ge=0.0)
    expected_spoilage_kg: float = Field(..., ge=0.0)
    expected_salvage_loss_inr: float = Field(..., ge=0.0)
    net_recovery_inr: float = Field(...)
    is_recommended: bool = False
    tradeoff_summary: str = Field(..., description="Explanation of tradeoffs and assumptions")


class DiscountRecommendationResponse(BaseDomainModel, ProvenanceMixin):
    batch_id: str
    batch_code: str
    commodity: str
    current_quantity_kg: float
    base_price_per_kg: float
    procurement_cost_per_kg: float
    remaining_shelf_life_hours: float
    urgency_level: str
    recommended_strategy: str
    options: List[DiscountOption]
    generated_at: datetime
    elasticity_assumption_note: str = "Assumes -1.25 price elasticity for retail mandis; processor demand capped at daily processing batch size."
