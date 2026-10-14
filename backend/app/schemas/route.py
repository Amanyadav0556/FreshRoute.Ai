"""Logistics route and transit schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin


class RouteBase(BaseDomainModel, ProvenanceMixin):
    origin_name: str = Field(..., description="Origin collection centre name")
    destination_id: str = Field(..., description="Target destination ID")
    destination_name: str = Field(..., description="Target destination market name")
    distance_km: float = Field(..., gt=0, description="Road distance in kilometers")
    standard_travel_time_hours: float = Field(..., gt=0, description="Baseline transit duration")
    toll_charges_inr: float = Field(0.0, ge=0, description="NHAI highway toll expenses")
    road_quality_factor: float = Field(1.0, gt=0, description="1.0 = smooth expressway; >1.0 = rough ghat/monsoon road causing produce vibration")
    ambient_temp_celsius: float = Field(28.0, description="Expected average daytime transit temperature")


class RouteCreate(RouteBase):
    pass


class RouteResponse(RouteBase):
    id: str
    effective_travel_time_hours: float = Field(0.0, gt=0)
    created_at: datetime
    updated_at: datetime
