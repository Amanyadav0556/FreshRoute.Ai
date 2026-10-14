"""Destination market and hub schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin


class DestinationBase(BaseDomainModel, ProvenanceMixin):
    name: str = Field(..., description="Mandi or market name, e.g. Vashi APMC Navi Mumbai")
    city: str = Field(..., description="Target city: Mumbai, Pune, Thane, etc.")
    state: str = Field("Maharashtra", description="State in India")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    market_type: str = Field("wholesale_mandi", description="wholesale_mandi, modern_retail, processor, local_haat")
    unloading_handling_fee_per_kg: float = Field(0.50, ge=0.0, description="Handling cost in INR/kg")
    avg_selling_price_multiplier: float = Field(1.0, gt=0.0, description="Market price index factor relative to base")
    daily_demand_capacity_kg: float = Field(10000.0, gt=0.0, description="Estimated total intake capacity per day")


class DestinationCreate(DestinationBase):
    pass


class DestinationResponse(DestinationBase):
    id: str
    active_orders_count: int = 0
    created_at: datetime
    updated_at: datetime
