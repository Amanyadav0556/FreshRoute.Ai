"""Produce batch schemas for FreshRoute AI."""
from pydantic import Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin, UrgencyLevel, DataProvenance


class BatchBase(BaseDomainModel, ProvenanceMixin):
    batch_code: str = Field(..., description="Unique human-readable identifier, e.g. BATCH-NSK-2026-001")
    commodity: str = Field(..., description="Produce name: Tomatoes, Onions, Grapes, Spinach, etc.")
    variety: Optional[str] = Field(None, description="Agricultural variety, e.g. Nashik Red, Flame Seedless")
    collection_centre_id: str = Field(..., description="Origin collection hub or FPO centre ID")
    initial_quantity_kg: float = Field(..., gt=0, description="Harvested weight in kg")
    current_quantity_kg: float = Field(..., ge=0, description="Remaining unallocated weight in kg")
    harvest_date: datetime = Field(..., description="Timestamp of harvest")
    initial_shelf_life_hours: float = Field(..., gt=0, description="Expected shelf life under ambient conditions")
    remaining_shelf_life_hours: float = Field(..., ge=0, description="Estimated current hours before spoilage")
    storage_condition: str = Field("ambient", description="Storage environment: ambient, precool, cold_storage")
    procurement_cost_per_kg: float = Field(..., ge=0, description="Cost paid to farmer in INR/kg")
    min_selling_price_per_kg: float = Field(..., ge=0, description="Floor threshold price in INR/kg")
    quality_grade: str = Field("Grade A", description="Grade A, Grade B, or Grade C")


class BatchCreate(BatchBase):
    pass


class BatchUpdate(BaseDomainModel):
    current_quantity_kg: Optional[float] = Field(None, ge=0)
    remaining_shelf_life_hours: Optional[float] = Field(None, ge=0)
    storage_condition: Optional[str] = None
    quality_grade: Optional[str] = None
    provenance: Optional[DataProvenance] = None


class BatchResponse(BatchBase):
    id: str
    urgency_level: UrgencyLevel = UrgencyLevel.NORMAL
    spoilage_risk_percent: float = Field(0.0, ge=0.0, le=100.0)
    created_at: datetime
    updated_at: datetime

    @field_validator("urgency_level", mode="before")
    def calculate_urgency(cls, v, values):
        if v:
            return v
        rsl = values.data.get("remaining_shelf_life_hours", 48.0)
        if rsl < 12.0:
            return UrgencyLevel.CRITICAL
        elif rsl < 24.0:
            return UrgencyLevel.HIGH
        elif rsl < 48.0:
            return UrgencyLevel.NORMAL
        return UrgencyLevel.LOW


class BatchFilter(BaseDomainModel):
    commodity: Optional[str] = None
    collection_centre_id: Optional[str] = None
    urgency_level: Optional[UrgencyLevel] = None
    min_shelf_life_hours: Optional[float] = None
    max_shelf_life_hours: Optional[float] = None
    storage_condition: Optional[str] = None
