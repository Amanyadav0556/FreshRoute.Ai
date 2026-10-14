"""Optimization dispatch planning and solver trigger endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from app.schemas.plan import PlanRequest, PlanResponse
from app.db.repositories.batch_repo import batch_repo
from app.db.repositories.destination_repo import destination_repo
from app.db.repositories.vehicle_repo import vehicle_repo
from app.db.repositories.route_repo import route_repo
from app.db.repositories.order_repo import order_repo
from app.db.repositories.plan_repo import plan_repo

from app.services.scenario_runner import apply_scenario_disruptions, get_scenario_definitions
from app.services.optimizer.highs_solver import solve_with_highs
from app.services.optimizer.greedy_solver import solve_with_greedy

router = APIRouter()


@router.post("/optimize", response_model=PlanResponse)
async def generate_optimization_plan(request: PlanRequest):
    """Executes the SciPy HiGHS LP solver (with greedy fallback) for produce dispatch."""
    batches = await batch_repo.get_all()
    destinations = await destination_repo.get_all()
    vehicles = await vehicle_repo.get_all()
    routes = await route_repo.get_all()
    orders = await order_repo.get_all()

    # Apply scenario mutations if specified
    scenario_name = "Normal Operation"
    if request.scenario_id:
        scenarios = get_scenario_definitions()
        scen = next((s for s in scenarios if s["id"] == request.scenario_id), None)
        if scen:
            scenario_name = scen["name"]
        batches, destinations, vehicles, routes, orders = apply_scenario_disruptions(
            scenario_id=request.scenario_id,
            batches=batches,
            destinations=destinations,
            vehicles=vehicles,
            routes=routes,
            orders=orders,
        )

    # Solve with HiGHS
    plan = solve_with_highs(
        batches=batches,
        destinations=destinations,
        vehicles=vehicles,
        routes=routes,
        orders=orders,
        strategy=request.strategy,
        timeout_seconds=request.solver_timeout_seconds,
    )

    # If HiGHS fails or is infeasible, fall back to heuristic greedy solver
    if not plan:
        plan = solve_with_greedy(
            batches=batches,
            destinations=destinations,
            vehicles=vehicles,
            routes=routes,
            orders=orders,
            strategy=request.strategy,
        )

    plan.scenario_name = scenario_name

    # Save generated plan to repository
    plan_dict = plan.model_dump()
    await plan_repo.create(plan_dict)

    return plan


@router.get("/latest", response_model=PlanResponse)
async def get_latest_plan():
    """Retrieves the most recent dispatch plan or runs a fresh baseline plan."""
    latest = await plan_repo.get_latest_plan()
    if latest:
        return latest

    # If no plan generated yet, run standard balanced plan
    return await generate_optimization_plan(PlanRequest(strategy="balanced"))


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan_by_id(plan_id: str):
    """Retrieves an existing plan by ID."""
    plan = await plan_repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail=f"Plan {plan_id} not found.")
    return plan


@router.post("/{plan_id}/confirm", response_model=PlanResponse)
async def confirm_plan(plan_id: str):
    """Confirms and commits a dispatch plan, deducting inventory and locking vehicle dispatches."""
    plan = await plan_repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail=f"Plan {plan_id} not found.")

    for item in plan.get("allocations", []):
        b_id = item.get("batch_id")
        qty = float(item.get("allocated_quantity_kg", 0.0))
        await batch_repo.update_remaining_quantities(b_id, qty)

        v_id = item.get("vehicle_id")
        await vehicle_repo.update_status(v_id, "en_route")

    plan["status"] = "confirmed"
    await plan_repo.update(plan_id, {"status": "confirmed"})
    return plan
