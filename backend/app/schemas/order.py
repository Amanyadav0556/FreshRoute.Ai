"""Buyer order and market demand schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin


class OrderBase(BaseDomainModel, ProvenanceMixin):
    order_code: str = Field(..., description="Unique order reference e.g. ORD-BOM-042")
    destination_id: str = Field(..., description="Destination market or buyer ID")
    destination_name: str = Field(..., description="Buyer or Mandi hub name")
    commodity: str = Field(..., description="Produce commodity ordered")
    variety: Optional[str] = None
    demanded_quantity_kg: float = Field(..., gt=0, description="Requested purchase weight in kg")
    offered_price_per_kg: float = Field(..., gt=0, description="Purchase bid price in INR/kg")
    delivery_deadline: datetime = Field(..., description="Must-arrive-by timestamp")
    min_acceptable_grade: str = Field("Grade B", description="Grade A, Grade B, Grade C")
    min_shelf_life_upon_arrival_hours: float = Field(12.0, ge=0, description="Minimum acceptable freshness remaining upon delivery")
    penalty_per_kg_unfulfilled: float = Field(2.0, ge=0, description="Shortage breach penalty INR/kg")


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: str
    allocated_quantity_kg: float = 0.0
    fulfillment_rate_percent: float = 0.0
    status: str = "pending"
    created_at: datetime
    updated_at: datetime
