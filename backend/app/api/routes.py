"""Logistics routes and transit corridor endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timezone
import uuid

from app.schemas.route import RouteCreate, RouteResponse
from app.db.repositories.route_repo import route_repo

router = APIRouter()


@router.get("", response_model=List[RouteResponse])
async def list_routes():
    """Retrieves all standard transit corridors and distance-time matrices."""
    return await route_repo.get_all()


@router.get("/{destination_id}", response_model=RouteResponse)
async def get_route_by_destination(destination_id: str):
    """Retrieves route transit details to a specific destination hub."""
    route = await route_repo.get_route(origin_name="Nashik", destination_id=destination_id)
    if not route:
        raise HTTPException(status_code=404, detail=f"Route to destination {destination_id} not found.")
    return route


@router.post("", response_model=RouteResponse, status_code=201)
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
    return await route_repo.create(route_data)
