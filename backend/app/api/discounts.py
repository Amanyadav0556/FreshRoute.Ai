"""Discount optimization and dynamic pricing recommendation endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any

from app.db.repositories.batch_repo import batch_repo
from app.db.repositories.destination_repo import destination_repo
from app.services.discount_engine import evaluate_discount_strategies

router = APIRouter()


def format_discount_rec(rec_obj, batch: Dict[str, Any], dest: Dict[str, Any]) -> Dict[str, Any]:
    options = []
    for opt in rec_obj.options:
        options.append({
            "discount_percent": float(opt.discount_percent),
            "recommended_price_inr_per_kg": float(opt.proposed_price_per_kg),
            "expected_quantity_kg": float(opt.expected_clearance_kg),
            "estimated_revenue_inr": float(opt.expected_revenue_inr),
            "transport_cost_inr": round(float(opt.expected_clearance_kg) * 1.5, 2),
            "handling_cost_inr": round(float(opt.expected_clearance_kg) * 0.5, 2),
            "net_value_inr": float(opt.net_recovery_inr),
            "demand_response_assumption": opt.tradeoff_summary,
        })

    rsl = float(batch.get("remaining_shelf_life_hours", 24.0))
    action = "discount" if rsl >= 12.0 else "salvage"

    return {
        "batch_id": batch["id"],
        "batch": {
            "id": batch["id"],
            "batch_code": batch.get("batch_code", ""),
            "commodity": {"name": batch.get("commodity", "")},
            "quantity_kg": float(batch.get("current_quantity_kg", 0.0)),
            "remaining_shelf_life_hours": rsl,
        },
        "destination_id": dest.get("id", "dest-vashi-01"),
        "destination": {
            "id": dest.get("id", "dest-vashi-01"),
            "name": dest.get("name", "Vashi APMC Mandi Hub"),
        },
        "recommended_action": action,
        "recommended_discount_percent": 15 if action == "discount" else 35,
        "options": options,
        "explanation": f"Batch {batch.get('batch_code')} ({batch.get('commodity')}) has {rsl:.1f}h shelf-life remaining. Dynamic markdown balances clearance velocity against potential salvage loss.",
        "assumptions": [
            "Price elasticity calibrated to ICAR post-harvest market study (-1.25 to -1.80)",
            "Guaranteed processing plant offtake floor available at 95% procurement cost",
            "Section 80G tax write-off applies to zero-waste food bank charitable donations",
        ],
        "uncertainty_note": "Local spot demand may vary with intra-day mandi arrival volumes.",
        "walk_away_price_available": True,
    }


@router.get("")
async def get_all_discount_recommendations(threshold_hours: float = Query(36.0, ge=6.0, le=72.0)) -> List[Dict[str, Any]]:
    """Computes 7-option discount pricing trade-offs for all produce batches approaching expiration."""
    batches = await batch_repo.get_all()
    destinations = await destination_repo.get_all()
    first_dest = destinations[0] if destinations else {"id": "dest-vashi-01", "name": "Vashi APMC"}

    results = []
    for b in batches:
        rsl = float(b.get("remaining_shelf_life_hours", 48.0))
        qty = float(b.get("current_quantity_kg", 0.0))
        if rsl <= threshold_hours and qty > 0:
            rec_obj = evaluate_discount_strategies(b)
            results.append(format_discount_rec(rec_obj, b, first_dest))

    return results


@router.get("/{batch_id}")
async def get_batch_discount_recommendation(batch_id: str) -> Dict[str, Any]:
    """Computes side-by-side 7 pricing options for a specific produce batch."""
    batch = await batch_repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Produce batch {batch_id} not found.")

    destinations = await destination_repo.get_all()
    first_dest = destinations[0] if destinations else {"id": "dest-vashi-01", "name": "Vashi APMC"}

    rec_obj = evaluate_discount_strategies(batch)
    return format_discount_rec(rec_obj, batch, first_dest)
