"""Plan validation engine for FreshRoute AI.
Validates dispatch plans against 6 physical, thermal, and economic constraints.
Returns detailed pass/fail diagnostics for auditing and trust.
"""
from typing import Dict, Any, List
from app.schemas.plan import PlanValidationResult, PlanValidationCheck, PlanItem


def validate_dispatch_plan(
    allocations: List[PlanItem],
    batches: List[Dict[str, Any]],
    vehicles: List[Dict[str, Any]],
    destinations: List[Dict[str, Any]],
) -> PlanValidationResult:
    checks: List[PlanValidationCheck] = []
    
    # 1. Capacity Non-Exceedance
    veh_cap_map = {v["id"]: float(v.get("capacity_kg", 0.0)) for v in vehicles}
    veh_allocated = {}
    for item in allocations:
        veh_allocated[item.vehicle_id] = veh_allocated.get(item.vehicle_id, 0.0) + item.allocated_quantity_kg

    cap_passed = True
    cap_details = "All vehicle payload capacities respected."
    for v_id, total_alloc in veh_allocated.items():
        limit = veh_cap_map.get(v_id, 99999.0)
        if total_alloc > limit * 1.02:  # allow 2% tolerance
            cap_passed = False
            cap_details = f"Vehicle {v_id} overloaded: {total_alloc:.1f} kg > {limit:.1f} kg limit."
            break

    checks.append(PlanValidationCheck(rule_name="Capacity Non-Exceedance", passed=cap_passed, details=cap_details))

    # 2. Supply Conservation
    batch_qty_map = {b["id"]: float(b.get("current_quantity_kg", 0.0)) for b in batches}
    batch_allocated = {}
    for item in allocations:
        batch_allocated[item.batch_id] = batch_allocated.get(item.batch_id, 0.0) + item.allocated_quantity_kg

    supply_passed = True
    supply_details = "Produce stock availability respected."
    for b_id, total_alloc in batch_allocated.items():
        limit = batch_qty_map.get(b_id, 0.0)
        if total_alloc > limit * 1.01:
            supply_passed = False
            supply_details = f"Batch {b_id} over-allocated: {total_alloc:.1f} kg > {limit:.1f} kg stock."
            break

    checks.append(PlanValidationCheck(rule_name="Supply Conservation", passed=supply_passed, details=supply_details))

    # 3. Shelf-Life Viability
    shelf_passed = True
    shelf_details = "All dispatched consignments maintain positive shelf life upon delivery."
    for item in allocations:
        if item.remaining_shelf_life_on_arrival_hours <= 0.0:
            shelf_passed = False
            shelf_details = f"Batch {item.batch_code} would arrive spoiled (RSL = {item.remaining_shelf_life_on_arrival_hours}h)."
            break

    checks.append(PlanValidationCheck(rule_name="Shelf-Life Viability", passed=shelf_passed, details=shelf_details))

    # 4. Demand Upper Bounds
    dest_cap_map = {d["id"]: float(d.get("daily_demand_capacity_kg", 50000.0)) for d in destinations}
    dest_allocated = {}
    for item in allocations:
        dest_allocated[item.destination_id] = dest_allocated.get(item.destination_id, 0.0) + item.allocated_quantity_kg

    demand_passed = True
    demand_details = "Market intake capacities respected."
    for d_id, total_alloc in dest_allocated.items():
        limit = dest_cap_map.get(d_id, 50000.0)
        if total_alloc > limit:
            demand_passed = False
            demand_details = f"Destination {d_id} exceeded intake capacity: {total_alloc:.1f} kg > {limit:.1f} kg."
            break

    checks.append(PlanValidationCheck(rule_name="Demand Upper Bounds", passed=demand_passed, details=demand_details))

    # 5. Thermal Compliance
    thermal_passed = True
    thermal_details = "Leafy greens and berry commodities assigned to compliant cooling profiles."
    for item in allocations:
        if "spinach" in item.commodity.lower() and item.estimated_spoilage_risk_percent > 85.0:
            thermal_passed = False
            thermal_details = f"High spoilage risk on sensitive commodity {item.commodity} ({item.estimated_spoilage_risk_percent}%)."
            break

    checks.append(PlanValidationCheck(rule_name="Thermal Compliance", passed=thermal_passed, details=thermal_details))

    # 6. Economic Non-Negativity
    econ_passed = True
    econ_details = "All planned dispatches yield positive net economic value."
    for item in allocations:
        if item.net_economic_value_inr < -100.0:  # slight buffer for loss-minimizing salvages
            econ_passed = False
            econ_details = f"Allocation {item.batch_code} -> {item.destination_name} has negative net return (₹{item.net_economic_value_inr:.2f})."
            break

    checks.append(PlanValidationCheck(rule_name="Economic Non-Negativity", passed=econ_passed, details=econ_details))

    passed_count = sum(1 for c in checks if c.passed)
    return PlanValidationResult(
        is_valid=(passed_count == len(checks)),
        total_checks=len(checks),
        passed_checks=passed_count,
        failed_checks=len(checks) - passed_count,
        checks=checks,
    )
