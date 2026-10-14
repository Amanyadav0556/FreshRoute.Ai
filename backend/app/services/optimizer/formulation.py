"""Mathematical formulation and data structure preparation for FreshRoute AI LP/MILP optimizer.
"""
from typing import Dict, Any, List, Tuple
from app.services.shelf_life import estimate_spoilage_risk


def build_candidate_triplets(
    batches: List[Dict[str, Any]],
    destinations: List[Dict[str, Any]],
    vehicles: List[Dict[str, Any]],
    routes: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
    strategy: str = "balanced",
) -> List[Dict[str, Any]]:
    """Builds all feasible (batch b, destination d, vehicle v) dispatch candidate triplets.
    Filters out any triplet where transit duration exceeds batch remaining shelf life.
    """
    dest_map = {d["id"]: d for d in destinations}
    route_map = {r["destination_id"]: r for r in routes}
    
    # Calculate total demand per destination and commodity
    demand_lookup = {}
    for ord in orders:
        key = (ord["destination_id"], ord["commodity"].lower())
        demand_lookup[key] = demand_lookup.get(key, 0.0) + float(ord.get("demanded_quantity_kg", 0.0))

    candidates = []

    for b in batches:
        b_qty = float(b.get("current_quantity_kg", 0.0))
        if b_qty <= 0:
            continue
        b_commodity = b.get("commodity", "")
        b_rsl = float(b.get("remaining_shelf_life_hours", 24.0))
        b_proc_cost = float(b.get("procurement_cost_per_kg", 20.0))
        b_base_price = float(b.get("min_selling_price_per_kg", 25.0))

        for d in destinations:
            d_id = d["id"]
            d_name = d["name"]
            handling_fee = float(d.get("unloading_handling_fee_per_kg", 0.50))
            price_mult = float(d.get("avg_selling_price_multiplier", 1.0))
            
            # Find matching order price if available, else derive from destination multiplier
            matching_order = next(
                (o for o in orders if o["destination_id"] == d_id and o["commodity"].lower() == b_commodity.lower()),
                None,
            )
            if matching_order:
                selling_price = float(matching_order.get("offered_price_per_kg", b_base_price * price_mult))
            else:
                selling_price = b_base_price * price_mult

            route = route_map.get(d_id)
            dist_km = float(route.get("distance_km", 150.0)) if route else 150.0
            std_time = float(route.get("standard_travel_time_hours", 3.5)) if route else 3.5
            toll = float(route.get("toll_charges_inr", 0.0)) if route else 0.0
            ambient_temp = float(route.get("ambient_temp_celsius", 30.0)) if route else 30.0
            road_factor = float(route.get("road_quality_factor", 1.0)) if route else 1.0

            for v in vehicles:
                if v.get("status") != "available":
                    continue
                v_id = v["id"]
                is_reefer = bool(v.get("is_refrigerated", False))
                fixed_cost = float(v.get("fixed_booking_cost_inr", 400.0))
                per_km_cost = float(v.get("per_km_cost_inr", 14.0))
                capacity_kg = float(v.get("capacity_kg", 1500.0))
                
                # Check shelf life and transit viability
                spoil_analysis = estimate_spoilage_risk(
                    remaining_shelf_life_hours=b_rsl,
                    transit_hours=std_time,
                    ambient_temp_celsius=ambient_temp,
                    commodity=b_commodity,
                    is_refrigerated=is_reefer,
                    road_quality_factor=road_factor,
                )

                if not spoil_analysis["is_feasible"]:
                    continue  # Hard transit constraint: batch would spoil before arrival

                rsl_on_arrival = spoil_analysis["remaining_on_arrival_hours"]
                spoil_risk_pct = spoil_analysis["spoilage_risk_percent"]

                # Transport cost allocation per kg assuming load share
                route_transport_cost = fixed_cost + (dist_km * per_km_cost) + toll
                transport_cost_per_kg = route_transport_cost / max(100.0, capacity_kg)

                # Objective weight adjustments based on strategy
                margin_per_kg = selling_price - b_proc_cost - handling_fee - transport_cost_per_kg
                spoilage_penalty = (spoil_risk_pct / 100.0) * b_proc_cost

                if strategy == "max_margin":
                    score = margin_per_kg - (0.5 * spoilage_penalty)
                elif strategy == "min_spoilage":
                    score = (100.0 - spoil_risk_pct) * 2.0 + (margin_per_kg * 0.5)
                elif strategy == "max_volume":
                    score = 50.0 + margin_per_kg
                else:  # balanced
                    score = margin_per_kg - spoilage_penalty

                candidates.append({
                    "batch": b,
                    "destination": d,
                    "vehicle": v,
                    "route": route,
                    "distance_km": dist_km,
                    "travel_time_hours": std_time,
                    "selling_price_per_kg": round(selling_price, 2),
                    "procurement_cost_per_kg": b_proc_cost,
                    "transport_cost_per_kg": round(transport_cost_per_kg, 2),
                    "fixed_vehicle_cost": fixed_cost,
                    "per_km_cost": per_km_cost,
                    "toll_cost": toll,
                    "spoilage_risk_percent": spoil_risk_pct,
                    "remaining_shelf_life_on_arrival": rsl_on_arrival,
                    "unit_margin_inr": round(margin_per_kg, 2),
                    "optimization_score": round(score, 4),
                })

    return candidates
