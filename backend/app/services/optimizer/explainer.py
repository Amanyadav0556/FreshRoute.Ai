"""Explainability module for FreshRoute AI optimization decisions.
Transforms mathematical allocations into natural-language business rationale,
citing shelf-life margins, price capture, and vehicle suitability.
"""
from typing import Dict, Any


def generate_dispatch_explanation(
    batch: Dict[str, Any],
    destination: Dict[str, Any],
    vehicle: Dict[str, Any],
    quantity_kg: float,
    rsl_on_arrival_hours: float,
    spoilage_risk_percent: float,
    unit_margin: float,
) -> str:
    commodity = batch.get("commodity", "Produce")
    dest_name = destination.get("name", "Market Hub")
    plate = vehicle.get("plate_number", "")
    is_reefer = vehicle.get("is_refrigerated", False)
    veh_type = "Reefer" if is_reefer else "Ambient Truck"
    rsl = float(batch.get("remaining_shelf_life_hours", 24.0))

    if rsl < 12.0:
        urgency_phrase = f"Emergency fast-track dispatch ({rsl:.1f}h remaining)"
    elif rsl < 24.0:
        urgency_phrase = f"High-priority dispatch ({rsl:.1f}h remaining)"
    else:
        urgency_phrase = f"Standard scheduled dispatch ({rsl:.1f}h freshness)"

    cooling_note = "with active cold-chain protection" if is_reefer else "via ambient transit"
    margin_phrase = f"yielding ₹{unit_margin:.2f}/kg net margin"

    return (
        f"{urgency_phrase}: Routed {quantity_kg:.0f} kg to {dest_name} via {veh_type} ({plate}) {cooling_note}. "
        f"Leaves {rsl_on_arrival_hours:.1f}h freshness buffer upon arrival (estimated spoilage risk {spoilage_risk_percent:.1f}%), {margin_phrase}."
    )
