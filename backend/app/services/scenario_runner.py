"""Disruption scenario execution and parametric mutation engine for FreshRoute AI.
Transforms baseline supply chain state based on scenario parameter overrides.
"""
from typing import Dict, Any, List, Tuple
from copy import deepcopy
from app.db.sample_data import SAMPLE_SCENARIOS


def get_scenario_definitions() -> List[Dict[str, Any]]:
    return SAMPLE_SCENARIOS


def apply_scenario_disruptions(
    scenario_id: str,
    batches: List[Dict[str, Any]],
    destinations: List[Dict[str, Any]],
    vehicles: List[Dict[str, Any]],
    routes: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Applies deep-copied parameter overrides for the selected disruption scenario."""
    b_copy = [deepcopy(b) for b in batches]
    d_copy = [deepcopy(d) for d in destinations]
    v_copy = [deepcopy(v) for v in vehicles]
    r_copy = [deepcopy(r) for r in routes]
    o_copy = [deepcopy(o) for o in orders]

    if not scenario_id or scenario_id in ["scen-01", "normal"]:
        return b_copy, d_copy, v_copy, r_copy, o_copy

    if scenario_id == "scen-02":  # Kasara Ghat Landslide Closure
        for r in r_copy:
            if "vashi" in r.get("destination_id", "") or "dadar" in r.get("destination_id", ""):
                r["standard_travel_time_hours"] = float(r.get("standard_travel_time_hours", 4.0)) + 3.5
                r["distance_km"] = float(r.get("distance_km", 160.0)) + 95.0
                r["road_quality_factor"] = float(r.get("road_quality_factor", 1.0)) * 1.30

    elif scenario_id == "scen-03":  # Peak Summer Heatwave (+7°C)
        for r in r_copy:
            r["ambient_temp_celsius"] = float(r.get("ambient_temp_celsius", 30.0)) + 7.0
        for b in b_copy:
            if b.get("storage_condition") != "cold_storage":
                b["remaining_shelf_life_hours"] = max(2.0, float(b.get("remaining_shelf_life_hours", 24.0)) * 0.70)

    elif scenario_id == "scen-04":  # Diesel Price Spike (+30%)
        for v in v_copy:
            v["per_km_cost_inr"] = float(v.get("per_km_cost_inr", 14.0)) * 1.30

    elif scenario_id == "scen-05":  # Bumper Tomato Harvest Glut (-35% Price)
        for o in o_copy:
            if "tomato" in o.get("commodity", "").lower():
                o["offered_price_per_kg"] = float(o.get("offered_price_per_kg", 25.0)) * 0.65

    elif scenario_id == "scen-06":  # Reefer Fleet Breakdown
        for v in v_copy:
            if v.get("is_refrigerated"):
                v["status"] = "maintenance"

    elif scenario_id == "scen-07":  # APMC Mandi Flash Strike (Vashi)
        for d in d_copy:
            if "vashi" in d.get("id", ""):
                d["daily_demand_capacity_kg"] = 0.0
        for o in o_copy:
            if "vashi" in o.get("destination_id", ""):
                o["demanded_quantity_kg"] = 0.0

    elif scenario_id == "scen-08":  # Quick Commerce Flash Surge (+50%)
        for o in o_copy:
            if "retail" in o.get("destination_id", "") or "blk" in o.get("order_code", "").lower():
                o["demanded_quantity_kg"] = float(o.get("demanded_quantity_kg", 1000.0)) * 1.50
                o["offered_price_per_kg"] = float(o.get("offered_price_per_kg", 80.0)) * 1.15

    return b_copy, d_copy, v_copy, r_copy, o_copy
