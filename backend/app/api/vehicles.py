"""Fleet and transport vehicle management endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse, FleetSummary
from app.schemas.common import FleetStatus
from app.db.repositories.vehicle_repo import vehicle_repo

router = APIRouter()


@router.get("", response_model=List[VehicleResponse])
async def list_vehicles(
    status: Optional[FleetStatus] = None,
    is_refrigerated: Optional[bool] = None,
):
    """Retrieves fleet vehicles with status and refrigeration capability filters."""
    vehicles = await vehicle_repo.get_all()
    results = vehicles

    if status:
        results = [v for v in results if v.get("status") == status]
    if is_refrigerated is not None:
        results = [v for v in results if bool(v.get("is_refrigerated")) == is_refrigerated]

    return results


@router.get("/summary", response_model=FleetSummary)
async def get_fleet_summary():
    """Computes fleet availability, capacity, and active utilization metrics."""
    vehicles = await vehicle_repo.get_all()
    total = len(vehicles)
    avail = sum(1 for v in vehicles if v.get("status") == "available")
    en_route = sum(1 for v in vehicles if v.get("status") == "en_route")
    reefer = sum(1 for v in vehicles if v.get("is_refrigerated") is True)
    total_cap = sum(float(v.get("capacity_kg", 0.0)) for v in vehicles)
    avail_cap = sum(float(v.get("capacity_kg", 0.0)) for v in vehicles if v.get("status") == "available")

    return FleetSummary(
        total_vehicles=total,
        available_vehicles=avail,
        en_route_vehicles=en_route,
        refrigerated_count=reefer,
        total_capacity_kg=round(total_cap, 1),
        available_capacity_kg=round(avail_cap, 1),
    )


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: str):
    """Retrieves vehicle specifications by ID."""
    veh = await vehicle_repo.get_by_id(vehicle_id)
    if not veh:
        raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found.")
    return veh


@router.post("", response_model=VehicleResponse, status_code=201)
async def create_vehicle(vehicle_in: VehicleCreate):
    """Onboards a new transport vehicle or rental truck into the logistics network."""
    now = datetime.now(timezone.utc)
    new_id = f"veh-{uuid.uuid4().hex[:8]}"
    veh_data = vehicle_in.model_dump()
    veh_data.update({
        "id": new_id,
        "created_at": now,
        "updated_at": now,
    })
    return await vehicle_repo.create(veh_data)


@router.patch("/{vehicle_id}/status", response_model=VehicleResponse)
async def update_vehicle_status(vehicle_id: str, new_status: FleetStatus):
    """Updates vehicle availability status (available, en_route, maintenance, offline)."""
    updated = await vehicle_repo.update_status(vehicle_id, new_status.value)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found.")
    return updated
