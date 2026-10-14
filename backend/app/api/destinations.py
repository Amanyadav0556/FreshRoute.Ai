"""Destination markets, APMC mandis, and retail hub endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.destination import DestinationCreate, DestinationResponse
from app.db.repositories.destination_repo import destination_repo

router = APIRouter()


@router.get("", response_model=List[DestinationResponse])
async def list_destinations(
    city: Optional[str] = None,
    market_type: Optional[str] = None,
):
    """Retrieves all destination markets, wholesale mandis, and retail hubs."""
    if city:
        return await destination_repo.get_by_city(city)
    if market_type:
        return await destination_repo.get_by_market_type(market_type)
    return await destination_repo.get_all()


@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(destination_id: str):
    """Retrieves a specific destination hub by ID."""
    dest = await destination_repo.get_by_id(destination_id)
    if not dest:
        raise HTTPException(status_code=404, detail=f"Destination {destination_id} not found.")
    return dest


@router.post("", response_model=DestinationResponse, status_code=201)
async def create_destination(destination_in: DestinationCreate):
    """Registers a new destination mandi or retail hub."""
    now = datetime.now(timezone.utc)
    new_id = f"dest-{uuid.uuid4().hex[:8]}"
    dest_data = destination_in.model_dump()
    dest_data.update({
        "id": new_id,
        "active_orders_count": 0,
        "created_at": now,
        "updated_at": now,
    })
    return await destination_repo.create(dest_data)
