"""Buyer orders and market demand endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from app.schemas.order import OrderCreate
from app.db.repositories.order_repo import order_repo

router = APIRouter()


def format_order(o: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": o["id"],
        "order_code": o.get("order_code", ""),
        "destination_id": o.get("destination_id", ""),
        "destination": {
            "id": o.get("destination_id", ""),
            "name": o.get("destination_name", ""),
            "location_description": o.get("destination_name", ""),
        },
        "commodity_id": f"comm-{o.get('commodity', '').lower()[:6]}",
        "commodity": {
            "id": f"comm-{o.get('commodity', '').lower()[:6]}",
            "name": o.get("commodity", ""),
        },
        "quantity_kg": float(o.get("demanded_quantity_kg", 0.0)),
        "demanded_quantity_kg": float(o.get("demanded_quantity_kg", 0.0)),
        "allocated_quantity_kg": float(o.get("allocated_quantity_kg", 0.0)),
        "offered_price_per_kg": float(o.get("offered_price_per_kg", 0.0)),
        "confirmed": True,
        "delivery_deadline": str(o.get("delivery_deadline")),
        "due_time": str(o.get("delivery_deadline")),
        "min_acceptable_grade": o.get("min_acceptable_grade", "Grade B"),
        "min_shelf_life_upon_arrival_hours": float(o.get("min_shelf_life_upon_arrival_hours", 8.0)),
        "status": o.get("status", "pending"),
        "fulfillment_rate_percent": float(o.get("fulfillment_rate_percent", 0.0)),
        "provenance": o.get("provenance", "real"),
        "created_at": str(o.get("created_at")),
        "updated_at": str(o.get("updated_at")),
    }


@router.get("")
async def list_orders(
    commodity: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Retrieves buyer purchase orders with commodity and status filters."""
    orders = await order_repo.get_all()
    results = orders
    if commodity:
        results = [o for o in results if commodity.lower() in o.get("commodity", "").lower()]
    if status:
        results = [o for o in results if o.get("status") == status]
    return [format_order(o) for o in results]


@router.get("/{order_id}")
async def get_order(order_id: str) -> Dict[str, Any]:
    """Retrieves order specifications by ID."""
    order = await order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found.")
    return format_order(order)


@router.post("", status_code=201)
async def create_order(order_in: OrderCreate):
    """Submits a new buyer purchase order into the system."""
    now = datetime.now(timezone.utc)
    new_id = f"ord-{uuid.uuid4().hex[:8]}"
    order_data = order_in.model_dump()
    order_data.update({
        "id": new_id,
        "allocated_quantity_kg": 0.0,
        "fulfillment_rate_percent": 0.0,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    })
    created = await order_repo.create(order_data)
    return format_order(created)
