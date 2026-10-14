"""Produce batch management and inventory endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.batch import BatchCreate, BatchUpdate, BatchResponse
from app.schemas.common import UrgencyLevel
from app.db.repositories.batch_repo import batch_repo

router = APIRouter()


@router.get("", response_model=List[BatchResponse])
async def list_batches(
    commodity: Optional[str] = None,
    urgency_level: Optional[UrgencyLevel] = None,
    min_shelf_life: Optional[float] = None,
    max_shelf_life: Optional[float] = None,
):
    """Retrieves all inventory produce batches with optional multi-attribute filters."""
    batches = await batch_repo.get_all()
    results = []

    for b in batches:
        # Commodity filter
        if commodity and commodity.lower() not in b.get("commodity", "").lower():
            continue

        rsl = float(b.get("remaining_shelf_life_hours", 48.0))

        # Shelf life bounds
        if min_shelf_life is not None and rsl < min_shelf_life:
            continue
        if max_shelf_life is not None and rsl > max_shelf_life:
            continue

        # Urgency level
        calculated_urgency = b.get("urgency_level")
        if not calculated_urgency:
            if rsl < 12.0:
                calculated_urgency = UrgencyLevel.CRITICAL
            elif rsl < 24.0:
                calculated_urgency = UrgencyLevel.HIGH
            elif rsl < 48.0:
                calculated_urgency = UrgencyLevel.NORMAL
            else:
                calculated_urgency = UrgencyLevel.LOW

        if urgency_level and calculated_urgency != urgency_level:
            continue

        results.append(b)

    return results


@router.get("/at-risk", response_model=List[BatchResponse])
async def get_at_risk_batches(threshold_hours: float = Query(24.0, ge=1.0, le=72.0)):
    """Returns produce batches approaching shelf-life expiration."""
    return await batch_repo.get_at_risk_batches(threshold_hours=threshold_hours)


@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch_by_id(batch_id: str):
    """Retrieves a specific produce batch by its unique ID."""
    batch = await batch_repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")
    return batch


@router.post("", response_model=BatchResponse, status_code=201)
async def create_batch(batch_in: BatchCreate):
    """Registers a new harvested produce batch into inventory."""
    now = datetime.now(timezone.utc)
    new_id = f"batch-{uuid.uuid4().hex[:8]}"

    rsl = batch_in.remaining_shelf_life_hours
    if rsl < 12.0:
        urgency = UrgencyLevel.CRITICAL
        spoil_risk = 65.0
    elif rsl < 24.0:
        urgency = UrgencyLevel.HIGH
        spoil_risk = 35.0
    else:
        urgency = UrgencyLevel.LOW
        spoil_risk = 8.0

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
        "remaining_shelf_life_hours": rsl,
        "storage_condition": batch_in.storage_condition,
        "procurement_cost_per_kg": batch_in.procurement_cost_per_kg,
        "min_selling_price_per_kg": batch_in.min_selling_price_per_kg,
        "quality_grade": batch_in.quality_grade,
        "urgency_level": urgency,
        "spoilage_risk_percent": spoil_risk,
        "provenance": batch_in.provenance,
        "provenance_source": batch_in.provenance_source,
        "created_at": now,
        "updated_at": now,
    }

    created = await batch_repo.create(batch_dict)
    return created


@router.patch("/{batch_id}", response_model=BatchResponse)
async def update_batch(batch_id: str, updates: BatchUpdate):
    """Updates batch status, quantity, or remaining shelf life."""
    update_data = updates.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    updated = await batch_repo.update(batch_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")
    return updated


@router.delete("/{batch_id}", status_code=204)
async def delete_batch(batch_id: str):
    """Deletes or archives a produce batch."""
    success = await batch_repo.delete(batch_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")
    return None
