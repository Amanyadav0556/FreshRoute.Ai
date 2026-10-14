"""Services package for FreshRoute AI."""
from app.services.shelf_life import (
    calculate_temperature_acceleration,
    calculate_transit_shelf_life_consumption,
    estimate_spoilage_risk,
)
from app.services.discount_engine import evaluate_discount_strategies
from app.services.alert_service import generate_spoilage_alerts
from app.services.scenario_runner import get_scenario_definitions, apply_scenario_disruptions
from app.services.evaluator import run_benchmark_evaluation
from app.services.optimizer import (
    solve_with_highs,
    solve_with_greedy,
    run_fefo_baseline,
    run_highest_price_baseline,
    validate_dispatch_plan,
    generate_dispatch_explanation,
)

__all__ = [
    "calculate_temperature_acceleration",
    "calculate_transit_shelf_life_consumption",
    "estimate_spoilage_risk",
    "evaluate_discount_strategies",
    "generate_spoilage_alerts",
    "get_scenario_definitions",
    "apply_scenario_disruptions",
    "run_benchmark_evaluation",
    "solve_with_highs",
    "solve_with_greedy",
    "run_fefo_baseline",
    "run_highest_price_baseline",
    "validate_dispatch_plan",
    "generate_dispatch_explanation",
]
