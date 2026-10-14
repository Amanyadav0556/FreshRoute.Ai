"""Optimization engine package for FreshRoute AI."""
from app.services.optimizer.highs_solver import solve_with_highs
from app.services.optimizer.greedy_solver import solve_with_greedy
from app.services.optimizer.fefo_baseline import run_fefo_baseline
from app.services.optimizer.highest_price_baseline import run_highest_price_baseline
from app.services.optimizer.validator import validate_dispatch_plan
from app.services.optimizer.explainer import generate_dispatch_explanation
from app.services.optimizer.formulation import build_candidate_triplets

__all__ = [
    "solve_with_highs",
    "solve_with_greedy",
    "run_fefo_baseline",
    "run_highest_price_baseline",
    "validate_dispatch_plan",
    "generate_dispatch_explanation",
    "build_candidate_triplets",
]
