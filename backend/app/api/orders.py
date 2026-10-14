"""Buyer orders and market demand endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.order import OrderCreate, OrderResponse
from app.db.repositories.order_repo import order_repo

router = APIRouter()


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    commodity: Optional[str] = None,
    status: Optional[str] = None,
):
    """Retrieves buyer purchase orders with commodity and status filters."""
    orders = await order_repo.get_all()
    results = orders
    if commodity:
        results = [o for o in results if commodity.lower() in o.get("commodity", "").lower()]
    if status:
        results = [o for o in results if o.get("status") == status]
    return results


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """Retrieves order specifications by ID."""
    order = await order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found.")
    return order


@router.post("", response_model=OrderResponse, status_code=201)
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
    return await order_repo.create(order_data)
