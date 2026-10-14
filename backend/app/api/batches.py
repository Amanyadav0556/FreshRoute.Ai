"""Produce batch management and inventory endpoints."""
from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from app.schemas.batch import BatchCreate, BatchUpdate, BatchResponse
from app.schemas.common import UrgencyLevel
from app.db.repositories.batch_repo import batch_repo

router = APIRouter()


def format_batch_for_frontend(b: Dict[str, Any]) -> Dict[str, Any]:
    rsl = float(b.get("remaining_shelf_life_hours", 48.0))
    comm_name = b.get("commodity", "")
    if rsl < 12.0:
        risk = "high"
        urgency = "critical"
    elif rsl < 24.0:
        risk = "medium"
        urgency = "high"
    else:
        risk = "low"
        urgency = "low"

    return {
        "id": str(b.get("id")),
        "batch_code": b.get("batch_code", ""),
        "commodity_id": f"comm-{comm_name.lower().replace(' ', '-')[:8]}",
        "commodity": {
            "id": f"comm-{comm_name.lower().replace(' ', '-')[:8]}",
            "name": comm_name,
            "base_shelf_life_hours": float(b.get("initial_shelf_life_hours", 72.0)),
            "provenance": b.get("provenance", "real"),
        },
        "collection_centre_id": b.get("collection_centre_id", "hub-nashik-01"),
        "collection_centre": {
            "id": b.get("collection_centre_id", "hub-nashik-01"),
            "name": "Nashik Central Aggregation Hub",
            "location_description": "Nashik Agri Logistics Park, Maharashtra",
            "created_at": str(b.get("created_at")),
        },
        "quantity_kg": float(b.get("current_quantity_kg", 0.0)),
        "current_quantity_kg": float(b.get("current_quantity_kg", 0.0)),
        "initial_quantity_kg": float(b.get("initial_quantity_kg", 0.0)),
        "remaining_shelf_life_hours": rsl,
        "initial_shelf_life_hours": float(b.get("initial_shelf_life_hours", 72.0)),
        "storage_condition": b.get("storage_condition", "ambient"),
        "procurement_cost_per_kg": float(b.get("procurement_cost_per_kg", 20.0)),
        "min_selling_price_per_kg": float(b.get("min_selling_price_per_kg", 25.0)),
        "quality_grade": "A" if "A" in str(b.get("quality_grade", "A")) else "B",
        "arrival_time": str(b.get("harvest_date")),
        "harvest_date": str(b.get("harvest_date")),
        "urgency_level": urgency,
        "risk_level": risk,
        "spoilage_risk_percent": float(b.get("spoilage_risk_percent", 0.0)),
        "provenance": b.get("provenance", "real"),
        "provenance_source": b.get("provenance_source", "Maharashtra APMC"),
        "created_at": str(b.get("created_at")),
        "updated_at": str(b.get("updated_at")),
    }


@router.get("")
async def list_batches(
    commodity: Optional[str] = None,
    urgency_level: Optional[str] = None,
    risk: Optional[str] = None,
    min_shelf_life: Optional[float] = None,
    max_shelf_life: Optional[float] = None,
    page: int = Query(1, ge=1),
    size: Optional[int] = Query(None),
) -> Any:
    """Retrieves produce batches with filtering, returning PaginatedResponse matching frontend contract."""
    raw_batches = await batch_repo.get_all()
    filtered = []

    for b in raw_batches:
        if commodity and commodity.lower() not in b.get("commodity", "").lower():
            continue
        rsl = float(b.get("remaining_shelf_life_hours", 48.0))
        if min_shelf_life is not None and rsl < min_shelf_life:
            continue
        if max_shelf_life is not None and rsl > max_shelf_life:
            continue

        item = format_batch_for_frontend(b)
        if risk and item["risk_level"] != risk:
            continue
        if urgency_level and item["urgency_level"] != urgency_level:
            continue

        filtered.append(item)

    limit = size or len(filtered) or 50
    return {
        "items": filtered[:limit],
        "total": len(filtered),
        "page": page,
        "size": limit,
    }


@router.get("/at-risk")
async def get_at_risk_batches(threshold_hours: float = Query(24.0, ge=1.0, le=72.0)):
    """Returns produce batches approaching shelf-life expiration."""
    batches = await batch_repo.get_at_risk_batches(threshold_hours=threshold_hours)
    return [format_batch_for_frontend(b) for b in batches]


@router.get("/{batch_id}")
async def get_batch_by_id(batch_id: str):
    """Retrieves a specific produce batch by its unique ID."""
    batch = await batch_repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")
    return format_batch_for_frontend(batch)


@router.post("", status_code=201)
async def create_batch(batch_in: BatchCreate):
    """Registers a new harvested produce batch into inventory."""
    now = datetime.now(timezone.utc)
    new_id = f"batch-{uuid.uuid4().hex[:8]}"

    batch_dict = {
        "id": new_id,
        "batch_code": batch_in.batch_code,
        "commodity": batch_in.commodity,
        "variety": batch_in.variety,
        "collection_centre_id": batch_in.collection_centre_id,
        "initial_quantity_kg": batch_in.initial_quantity_kg,
        "current_quantity_kg": batch_in.current_quantity_kg,
        "harvest_date": batch_in.harvest_date,
        "initial_shelf_life_hours": batch_in.initial_shelf_life_hours,
        "remaining_shelf_life_hours": batch_in.remaining_shelf_life_hours,
        "storage_condition": batch_in.storage_condition,
        "procurement_cost_per_kg": batch_in.procurement_cost_per_kg,
        "min_selling_price_per_kg": batch_in.min_selling_price_per_kg,
        "quality_grade": batch_in.quality_grade,
        "urgency_level": "normal",
        "spoilage_risk_percent": 15.0,
        "provenance": batch_in.provenance,
        "provenance_source": batch_in.provenance_source,
        "created_at": now,
        "updated_at": now,
    }

    created = await batch_repo.create(batch_dict)
    return format_batch_for_frontend(created)


@router.patch("/{batch_id}")
async def update_batch(batch_id: str, updates: BatchUpdate):
    """Updates batch status, quantity, or remaining shelf life."""
    update_data = updates.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    updated = await batch_repo.update(batch_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")
    return format_batch_for_frontend(updated)


@router.delete("/{batch_id}", status_code=204)
async def delete_batch(batch_id: str):
    """Deletes or archives a produce batch."""
    success = await batch_repo.delete(batch_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")
    return None
