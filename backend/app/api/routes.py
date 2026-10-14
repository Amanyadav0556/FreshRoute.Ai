"""Logistics routes and transit corridor endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timezone
import uuid

from app.schemas.route import RouteCreate
from app.db.repositories.route_repo import route_repo

router = APIRouter()


def format_route(r: Dict[str, Any]) -> Dict[str, Any]:
    dist = float(r.get("distance_km", 160.0))
    travel_time = float(r.get("standard_travel_time_hours", 4.0))
    toll = float(r.get("toll_charges_inr", 0.0))
    cost = round(toll + (dist * 14.0) + 400.0, 2)

    return {
        "id": r["id"],
        "origin_id": "hub-nashik-01",
        "origin": {
            "id": "hub-nashik-01",
            "name": r.get("origin_name", "Nashik Central Hub"),
            "location_description": "Nashik Agri Logistics Park, Maharashtra",
        },
        "destination_id": r.get("destination_id"),
        "destination": {
            "id": r.get("destination_id"),
            "name": r.get("destination_name"),
            "location_description": r.get("destination_name"),
        },
        "distance_km": dist,
        "standard_travel_time_hours": travel_time,
        "travel_time_hours": travel_time,
        "travel_time_low_hours": max(0.5, round(travel_time * 0.9, 1)),
        "travel_time_high_hours": round(travel_time * 1.25, 1),
        "toll_charges_inr": toll,
        "transport_cost_inr": cost,
        "road_quality_factor": float(r.get("road_quality_factor", 1.0)),
        "ambient_temp_celsius": float(r.get("ambient_temp_celsius", 28.0)),
        "effective_travel_time_hours": float(r.get("effective_travel_time_hours", travel_time)),
        "provenance": r.get("provenance", "real"),
        "created_at": str(r.get("created_at")),
        "updated_at": str(r.get("updated_at")),
    }


@router.get("")
async def list_routes() -> List[Dict[str, Any]]:
    """Retrieves all standard transit corridors and distance-time matrices."""
    routes = await route_repo.get_all()
    return [format_route(r) for r in routes]


@router.get("/{destination_id}")
async def get_route_by_destination(destination_id: str) -> Dict[str, Any]:
    """Retrieves route transit details to a specific destination hub."""
    route = await route_repo.get_route(origin_name="Nashik", destination_id=destination_id)
    if not route:
        raise HTTPException(status_code=404, detail=f"Route to destination {destination_id} not found.")
    return format_route(route)


@router.post("", status_code=201)
async def create_route(route_in: RouteCreate):
    """Defines a new transit route corridor with distance and ambient temperature."""
    now = datetime.now(timezone.utc)
    new_id = f"route-{uuid.uuid4().hex[:8]}"
    route_data = route_in.model_dump()
    route_data.update({
        "id": new_id,
        "effective_travel_time_hours": route_in.standard_travel_time_hours * route_in.road_quality_factor,
        "created_at": now,
        "updated_at": now,
    })
    created = await route_repo.create(route_data)
    return format_route(created)
