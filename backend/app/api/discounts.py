"""Discount optimization and dynamic pricing recommendation endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.schemas.discount import DiscountRecommendationResponse
from app.db.repositories.batch_repo import batch_repo
from app.services.discount_engine import evaluate_discount_strategies

router = APIRouter()


@router.get("", response_model=List[DiscountRecommendationResponse])
async def get_all_discount_recommendations(threshold_hours: float = Query(36.0, ge=6.0, le=72.0)):
    """Computes 7-option discount pricing trade-offs for all produce batches approaching expiration."""
    batches = await batch_repo.get_all()
    results = []

    for b in batches:
        rsl = float(b.get("remaining_shelf_life_hours", 48.0))
        qty = float(b.get("current_quantity_kg", 0.0))
        if rsl <= threshold_hours and qty > 0:
            rec = evaluate_discount_strategies(b)
            results.append(rec)

    # Sort descending by urgency (lowest remaining shelf life first)
    results.sort(key=lambda r: r.remaining_shelf_life_hours)
    return results


@router.get("/{batch_id}", response_model=DiscountRecommendationResponse)
async def get_batch_discount_recommendation(batch_id: str):
    """Computes side-by-side 7 pricing options for a specific produce batch."""
    batch = await batch_repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")

    return evaluate_discount_strategies(batch)
