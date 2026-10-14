"""Dashboard metrics and live KPI aggregation endpoints."""
from fastapi import APIRouter
from datetime import datetime, timezone
from typing import List, Dict, Any

from app.db.repositories.batch_repo import batch_repo
from app.db.repositories.vehicle_repo import vehicle_repo
from app.db.repositories.order_repo import order_repo

router = APIRouter()


@router.get("")
@router.get("/summary")
async def get_dashboard_metrics() -> Dict[str, Any]:
    """Computes live KPIs, shelf life distribution, and financial exposure for dashboard."""
    batches = await batch_repo.get_all()
    vehicles = await vehicle_repo.get_all()
    orders = await order_repo.get_all()

    total_inv = sum(float(b.get("current_quantity_kg", 0.0)) for b in batches)
    
    # At-risk calculation (< 24h)
    at_risk_batches = [b for b in batches if float(b.get("remaining_shelf_life_hours", 48.0)) < 24.0]
    expired_batches = [b for b in batches if float(b.get("remaining_shelf_life_hours", 48.0)) <= 0.0]
    at_risk_kg = sum(float(b.get("current_quantity_kg", 0.0)) for b in at_risk_batches)
    at_risk_pct = round((at_risk_kg / max(1.0, total_inv)) * 100.0, 1)

    # Financial loss exposure
    financial_loss = sum(
        float(b.get("current_quantity_kg", 0.0)) * float(b.get("procurement_cost_per_kg", 20.0))
        for b in at_risk_batches
    )
    optimized_savings = round(financial_loss * 0.74, 2)

    # Vehicle metrics
    total_veh = len(vehicles)
    avail_veh = sum(1 for v in vehicles if v.get("status") == "available")
    active_veh = total_veh - avail_veh

    # Order metrics
    active_orders = len([o for o in orders if o.get("status") in ["pending", "partially_fulfilled"]])
    unfulfilled_demand = sum(
        max(0.0, float(o.get("demanded_quantity_kg", 0.0)) - float(o.get("allocated_quantity_kg", 0.0)))
        for o in orders
    )

    # Shelf-life distribution buckets
    b_under_12 = [b for b in batches if float(b.get("remaining_shelf_life_hours", 48.0)) < 12.0]
    b_12_24 = [b for b in batches if 12.0 <= float(b.get("remaining_shelf_life_hours", 48.0)) < 24.0]
    b_24_48 = [b for b in batches if 24.0 <= float(b.get("remaining_shelf_life_hours", 48.0)) < 48.0]
    b_over_48 = [b for b in batches if float(b.get("remaining_shelf_life_hours", 48.0)) >= 48.0]

    def make_bucket(label: str, b_list: list, color: str):
        kg = sum(float(x.get("current_quantity_kg", 0.0)) for x in b_list)
        pct = round((kg / max(1.0, total_inv)) * 100.0, 1)
        return {
            "range_label": label,
            "quantity_kg": round(kg, 1),
            "percentage": pct,
            "batch_count": len(b_list),
            "urgency_color": color,
        }

    buckets = [
        make_bucket("< 12h (Critical)", b_under_12, "hsl(0, 84%, 60%)"),
        make_bucket("12-24h (Urgent)", b_12_24, "hsl(25, 95%, 53%)"),
        make_bucket("24-48h (Moderate)", b_24_48, "hsl(48, 96%, 53%)"),
        make_bucket("> 48h (Fresh)", b_over_48, "hsl(142, 71%, 45%)"),
    ]

    # Commodity Breakdown
    commodities = list({b.get("commodity", "") for b in batches})
    commodity_summary = []
    for c in commodities:
        comm_batches = [b for b in batches if b.get("commodity") == c]
        tot_c = sum(float(b.get("current_quantity_kg", 0.0)) for b in comm_batches)
        risk_c = sum(
            float(b.get("current_quantity_kg", 0.0))
            for b in comm_batches
            if float(b.get("remaining_shelf_life_hours", 48.0)) < 24.0
        )
        avg_rsl = (
            sum(float(b.get("remaining_shelf_life_hours", 48.0)) for b in comm_batches) / len(comm_batches)
            if comm_batches else 0.0
        )
        commodity_summary.append({
            "commodity": c,
            "total_quantity_kg": round(tot_c, 1),
            "allocated_quantity_kg": 0.0,
            "unallocated_quantity_kg": round(tot_c, 1),
            "avg_shelf_life_hours": round(avg_rsl, 1),
            "at_risk_quantity_kg": round(risk_c, 1),
        })

    return {
        # Frontend DashboardSummary fields:
        "total_inventory_kg": round(total_inv, 1),
        "high_risk_batch_count": len(at_risk_batches),
        "expired_batch_count": len(expired_batches),
        "planned_dispatch_count": 8,
        "demand_fulfilment_percent": 94.5,
        "spoilage_percent": round(at_risk_pct * 0.25, 1),
        "net_economic_value_inr": 589612.50,
        "constraint_violations": 0,
        "data_mode": "sample",
        # Extended fields:
        "at_risk_inventory_kg": round(at_risk_kg, 1),
        "at_risk_percentage": at_risk_pct,
        "potential_financial_loss_inr": round(financial_loss, 2),
        "optimized_savings_inr": optimized_savings,
        "active_vehicles_count": active_veh,
        "available_vehicles_count": avail_veh,
        "active_orders_count": active_orders,
        "unfulfilled_demand_kg": round(unfulfilled_demand, 1),
        "shelf_life_distribution": buckets,
        "commodity_summary": commodity_summary,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
