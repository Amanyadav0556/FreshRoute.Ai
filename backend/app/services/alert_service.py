"""Emergency spoilage alert and redistribution solver service.
Identifies critical batches approaching end-of-life and computes feasible immediate
rerouting candidates with transit buffer validation and infeasibility explanations.
"""
from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid

from app.schemas.alert import SpoilageAlert, RedistributionCandidate
from app.schemas.common import UrgencyLevel


def generate_spoilage_alerts(
    batches: List[Dict[str, Any]],
    destinations: List[Dict[str, Any]],
    routes: List[Dict[str, Any]],
    threshold_hours: float = 24.0,
) -> List[SpoilageAlert]:
    alerts: List[SpoilageAlert] = []
    route_map = {r["destination_id"]: r for r in routes}

    for b in batches:
        rsl = float(b.get("remaining_shelf_life_hours", 48.0))
        qty = float(b.get("current_quantity_kg", 0.0))
        if rsl > threshold_hours or qty <= 0:
            continue

        proc_cost = float(b.get("procurement_cost_per_kg", 20.0))
        commodity = b.get("commodity", "")
        financial_exposure = round(qty * proc_cost, 2)

        urgency = UrgencyLevel.CRITICAL if rsl < 12.0 else UrgencyLevel.HIGH

        candidates: List[RedistributionCandidate] = []
        for d in destinations:
            d_id = d["id"]
            d_name = d["name"]
            route = route_map.get(d_id, {})
            dist = float(route.get("distance_km", 150.0))
            travel_time = float(route.get("standard_travel_time_hours", 3.5))
            unloading_buffer = 1.0
            total_buffer = travel_time + unloading_buffer

            price_mult = float(d.get("avg_selling_price_multiplier", 1.0))
            bid_price = float(b.get("min_selling_price_per_kg", 25.0)) * price_mult * 0.90  # 10% emergency discount
            handling = float(d.get("unloading_handling_fee_per_kg", 0.50))
            trans_cost_per_kg = (dist * 13.0 + 350.0) / 1500.0

            is_feasible = (total_buffer < rsl)
            infeasibility_reason = None
            if not is_feasible:
                deficit = total_buffer - rsl
                infeasibility_reason = (
                    f"Infeasible: Transit time ({travel_time:.1f}h) + unloading ({unloading_buffer:.1f}h) "
                    f"exceeds remaining shelf life ({rsl:.1f}h) by {deficit:.1f} hours."
                )

            net_recovery = round(
                (bid_price - proc_cost - handling - trans_cost_per_kg) * min(qty, float(d.get("daily_demand_capacity_kg", 5000.0))),
                2,
            ) if is_feasible else 0.0

            candidates.append(
                RedistributionCandidate(
                    destination_id=d_id,
                    destination_name=d_name,
                    distance_km=dist,
                    travel_time_hours=travel_time,
                    unloading_handling_hours=unloading_buffer,
                    total_transit_buffer_hours=round(total_buffer, 1),
                    remaining_shelf_life_hours=rsl,
                    is_feasible=is_feasible,
                    infeasibility_reason=infeasibility_reason,
                    buyer_demand_kg=float(d.get("daily_demand_capacity_kg", 5000.0)),
                    offered_price_per_kg=round(bid_price, 2),
                    estimated_net_recovery_inr=net_recovery,
                )
            )

        # Sort candidates: feasible first, then highest net recovery
        candidates.sort(key=lambda c: (c.is_feasible, c.estimated_net_recovery_inr), reverse=True)

        if urgency == UrgencyLevel.CRITICAL:
            recommended_action = "Immediate priority dispatch to nearest feasible mandi or local agro-processor contract."
        else:
            recommended_action = "Apply 10-20% proactive discount promo and route via high-speed transit corridor."

        alerts.append(
            SpoilageAlert(
                id=f"alert-{b.get('id', uuid.uuid4().hex[:6])}",
                batch_id=b["id"],
                batch_code=b.get("batch_code", ""),
                commodity=commodity,
                quantity_kg=qty,
                remaining_shelf_life_hours=rsl,
                urgency_level=urgency,
                storage_condition=b.get("storage_condition", "ambient"),
                procurement_cost_inr=proc_cost,
                financial_exposure_inr=financial_exposure,
                flagged_at=datetime.now(timezone.utc),
                recommended_action=recommended_action,
                candidates=candidates,
            )
        )

    return alerts
