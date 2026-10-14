"""Fleet and transport vehicle schemas for FreshRoute AI."""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseDomainModel, ProvenanceMixin, FleetStatus


class VehicleBase(BaseDomainModel, ProvenanceMixin):
    plate_number: str = Field(..., description="Vehicle registration e.g. MH 15 AB 1234")
    model_type: str = Field(..., description="Tata Ace, Bolero Maxi Truck, Eicher 14ft, Reefer 20ft")
    vehicle_category: str = Field("mini_truck", description="mini_truck, medium_truck, reefer, electric_tempo")
    capacity_kg: float = Field(..., gt=0, description="Max legal load payload in kg")
    is_refrigerated: bool = Field(False, description="Whether vehicle has active temperature control reefer")
    fixed_booking_cost_inr: float = Field(500.0, ge=0, description="Base dispatch charge")
    per_km_cost_inr: float = Field(14.0, gt=0, description="Operating fuel & tyre cost per km")
    avg_speed_kmh: float = Field(45.0, gt=0, description="Estimated average speed including rural corridors")
    current_location: str = Field("Nashik Central Collection Centre", description="Current hub or coordinates")
    owner_role: str = Field("owned", description="owned, rental, contracted")
    status: FleetStatus = FleetStatus.AVAILABLE


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseDomainModel):
    status: Optional[FleetStatus] = None
    current_location: Optional[str] = None
    fixed_booking_cost_inr: Optional[float] = None
    per_km_cost_inr: Optional[float] = None


class VehicleResponse(VehicleBase):
    id: str
    created_at: datetime
    updated_at: datetime


class FleetSummary(BaseDomainModel):
    total_vehicles: int
    available_vehicles: int
    en_route_vehicles: int
    refrigerated_count: int
    total_capacity_kg: float
    available_capacity_kg: float
