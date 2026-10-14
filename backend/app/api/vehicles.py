"""Fleet and transport vehicle management endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from app.schemas.vehicle import VehicleCreate, FleetSummary
from app.schemas.common import FleetStatus
from app.db.repositories.vehicle_repo import vehicle_repo

router = APIRouter()


def format_vehicle(v: Dict[str, Any]) -> Dict[str, Any]:
    is_reefer = bool(v.get("is_refrigerated", False))
    fixed = float(v.get("fixed_booking_cost_inr", 400.0))
    per_km = float(v.get("per_km_cost_inr", 14.0))
    avg_trip_km = 160.0
    trip_cost = round(fixed + (avg_trip_km * per_km), 2)

    return {
        "id": v["id"],
        "vehicle_code": v.get("plate_number", ""),
        "plate_number": v.get("plate_number", ""),
        "model_type": v.get("model_type", ""),
        "vehicle_type": "refrigerated" if is_reefer else "normal",
        "vehicle_category": v.get("vehicle_category", "mini_truck"),
        "capacity_kg": float(v.get("capacity_kg", 1500.0)),
        "is_refrigerated": is_reefer,
        "fixed_booking_cost_inr": fixed,
        "per_km_cost_inr": per_km,
        "cost_per_trip_inr": trip_cost,
        "avg_speed_kmh": float(v.get("avg_speed_kmh", 45.0)),
        "cabin_temperature_c": 4.0 if is_reefer else None,
        "current_location": v.get("current_location", "Nashik Central Hub"),
        "owner_role": v.get("owner_role", "owned"),
        "status": v.get("status", "available"),
        "provenance": v.get("provenance", "real"),
        "created_at": str(v.get("created_at")),
        "updated_at": str(v.get("updated_at")),
    }


@router.get("")
async def list_vehicles(
    status: Optional[str] = None,
    is_refrigerated: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Retrieves fleet vehicles with status and refrigeration capability filters."""
    vehicles = await vehicle_repo.get_all()
    results = vehicles

    if status:
        results = [v for v in results if v.get("status") == status]
    if is_refrigerated is not None:
        results = [v for v in results if bool(v.get("is_refrigerated")) == is_refrigerated]

    return [format_vehicle(v) for v in results]


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


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: str) -> Dict[str, Any]:
    """Retrieves vehicle specifications by ID."""
    veh = await vehicle_repo.get_by_id(vehicle_id)
    if not veh:
        raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found.")
    return format_vehicle(veh)


@router.post("", status_code=201)
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
    created = await vehicle_repo.create(veh_data)
    return format_vehicle(created)


@router.patch("/{vehicle_id}/status")
async def update_vehicle_status(vehicle_id: str, new_status: FleetStatus):
    """Updates vehicle availability status (available, en_route, maintenance, offline)."""
    updated = await vehicle_repo.update_status(vehicle_id, new_status.value)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found.")
    return format_vehicle(updated)
