"""Destination markets, APMC mandis, and retail hub endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from app.schemas.destination import DestinationCreate
from app.db.repositories.destination_repo import destination_repo

router = APIRouter()


def format_destination(d: Dict[str, Any]) -> Dict[str, Any]:
    cap = float(d.get("daily_demand_capacity_kg", 15000.0))
    mult = float(d.get("avg_selling_price_multiplier", 1.0))
    handling_fee = float(d.get("unloading_handling_fee_per_kg", 0.50))
    return {
        "id": d["id"],
        "name": d["name"],
        "location_description": f"{d.get('city')}, {d.get('state', 'Maharashtra')}",
        "city": d.get("city"),
        "state": d.get("state", "Maharashtra"),
        "latitude": float(d.get("latitude", 19.0)),
        "longitude": float(d.get("longitude", 73.0)),
        "demand_kg": cap,
        "confirmed_order_kg": round(cap * 0.40, 1),
        "predicted_demand_kg": cap,
        "base_price_inr_per_kg": round(28.0 * mult, 2),
        "handling_time_hours": 1.0,
        "handling_cost_inr_per_kg": handling_fee,
        "unloading_handling_fee_per_kg": handling_fee,
        "avg_selling_price_multiplier": mult,
        "daily_demand_capacity_kg": cap,
        "active_orders_count": int(d.get("active_orders_count", 2)),
        "provenance": d.get("provenance", "real"),
        "provenance_source": d.get("provenance_source"),
        "created_at": str(d.get("created_at")),
        "updated_at": str(d.get("updated_at")),
    }


@router.get("")
async def list_destinations(city: Optional[str] = None, market_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all destination markets with complete frontend and backend field mappings."""
    if city:
        dests = await destination_repo.get_by_city(city)
    elif market_type:
        dests = await destination_repo.get_by_market_type(market_type)
    else:
        dests = await destination_repo.get_all()
    return [format_destination(d) for d in dests]


@router.get("/{destination_id}")
async def get_destination(destination_id: str) -> Dict[str, Any]:
    """Retrieves a specific destination hub by ID."""
    dest = await destination_repo.get_by_id(destination_id)
    if not dest:
        raise HTTPException(status_code=404, detail=f"Destination {destination_id} not found.")
    return format_destination(dest)


@router.post("", status_code=201)
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
    created = await destination_repo.create(dest_data)
    return format_destination(created)
