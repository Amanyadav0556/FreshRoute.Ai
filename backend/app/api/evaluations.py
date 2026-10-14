"""Multi-strategy benchmark evaluation endpoints."""
from fastapi import APIRouter, Query
from typing import Optional

from app.schemas.evaluation import BenchmarkResult
from app.db.repositories.batch_repo import batch_repo
from app.db.repositories.destination_repo import destination_repo
from app.db.repositories.vehicle_repo import vehicle_repo
from app.db.repositories.route_repo import route_repo
from app.db.repositories.order_repo import order_repo
from app.services.scenario_runner import apply_scenario_disruptions, get_scenario_definitions
from app.services.evaluator import run_benchmark_evaluation

router = APIRouter()


@router.get("", response_model=BenchmarkResult)
@router.post("/run", response_model=BenchmarkResult)
async def evaluate_strategies(scenario_id: Optional[str] = Query(None, description="Scenario ID to test under")):
    """Executes all 4 strategies (FEFO, Highest Price, Greedy, HiGHS) and computes comparative scoreboard."""
    batches = await batch_repo.get_all()
    destinations = await destination_repo.get_all()
    vehicles = await vehicle_repo.get_all()
    routes = await route_repo.get_all()
    orders = await order_repo.get_all()

    scenario_name = "Normal Operation"
    target_scen_id = scenario_id or "scen-01"

    if scenario_id and scenario_id != "scen-01":
        scenarios = get_scenario_definitions()
        scen = next((s for s in scenarios if s["id"] == scenario_id), None)
        if scen:
            scenario_name = scen["name"]
        batches, destinations, vehicles, routes, orders = apply_scenario_disruptions(
            scenario_id=scenario_id,
            batches=batches,
            destinations=destinations,
            vehicles=vehicles,
            routes=routes,
            orders=orders,
        )

    return run_benchmark_evaluation(
        batches=batches,
        destinations=destinations,
        vehicles=vehicles,
        routes=routes,
        orders=orders,
        scenario_id=target_scen_id,
        scenario_name=scenario_name,
    )
