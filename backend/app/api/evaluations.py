"""Multi-strategy benchmark evaluation endpoints."""
from fastapi import APIRouter, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from app.db.repositories.batch_repo import batch_repo
from app.db.repositories.destination_repo import destination_repo
from app.db.repositories.vehicle_repo import vehicle_repo
from app.db.repositories.route_repo import route_repo
from app.db.repositories.order_repo import order_repo
from app.services.scenario_runner import apply_scenario_disruptions, get_scenario_definitions
from app.services.evaluator import run_benchmark_evaluation

router = APIRouter()


async def compute_evaluations_list(scenario_id: Optional[str] = None) -> List[Dict[str, Any]]:
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

    bench = run_benchmark_evaluation(
        batches=batches,
        destinations=destinations,
        vehicles=vehicles,
        routes=routes,
        orders=orders,
        scenario_id=target_scen_id,
        scenario_name=scenario_name,
    )

    eval_list = []
    strat_key_map = {
        "fefo_baseline": "fefo",
        "highest_price_baseline": "highest_price",
        "greedy_baseline": "greedy",
        "freshroute_optimizer": "freshroute",
    }

    now_iso = datetime.now(timezone.utc).isoformat()
    for s in bench.strategies:
        s_key = strat_key_map.get(s.strategy_name, s.strategy_name)
        unmet = max(0.0, round(bench.total_market_demand_kg * (1.0 - s.order_fulfillment_rate_percent / 100.0), 1))
        eval_list.append({
            "id": f"eval-{s_key}",
            "plan_id": f"plan-{s_key}",
            "strategy": s_key,
            "scenario_id": scenario_id,
            "spoilage_percent": float(s.spoilage_rate_percent),
            "demand_fulfilment_percent": float(s.order_fulfillment_rate_percent),
            "unmet_demand_kg": unmet,
            "net_value_inr": float(s.net_economic_value_inr),
            "transport_cost_inr": float(s.total_transport_cost_inr),
            "discount_cost_inr": 0.0,
            "violation_count": 0,
            "runtime_seconds": round(s.computation_time_ms / 1000.0, 3) or 0.05,
            "created_at": now_iso,
        })

    return eval_list


@router.get("")
async def list_evaluations() -> List[Dict[str, Any]]:
    """Retrieves comparative strategy evaluations matching frontend Evaluation[] interface."""
    return await compute_evaluations_list()


@router.post("/run")
async def run_evaluation(payload: Dict[str, Any] = Body(default={})) -> List[Dict[str, Any]]:
    """Runs evaluations for the given scenario and returns Evaluation[]."""
    scenario_id = payload.get("scenario_id") if isinstance(payload, dict) else None
    return await compute_evaluations_list(scenario_id=scenario_id)
