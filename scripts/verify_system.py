#!/usr/bin/env python3
"""FreshRoute AI — Automated System Verification Script
Executes internal tests of shelf life decay, 7-strategy discounts,
HiGHS optimizer, plan validation, and benchmark evaluation.
"""
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.sample_data import (
    SAMPLE_BATCHES,
    SAMPLE_DESTINATIONS,
    SAMPLE_VEHICLES,
    SAMPLE_ROUTES,
    SAMPLE_ORDERS,
)
from app.services.shelf_life import estimate_spoilage_risk, calculate_temperature_acceleration
from app.services.discount_engine import evaluate_discount_strategies
from app.services.optimizer.highs_solver import solve_with_highs
from app.services.optimizer.greedy_solver import solve_with_greedy
from app.services.optimizer.validator import validate_dispatch_plan
from app.services.evaluator import run_benchmark_evaluation


def run_checks():
    print("=" * 60)
    print("  FreshRoute AI - Verification & Integrity Test")
    print("=" * 60)

    # 1. Test Thermal Decay
    accel = calculate_temperature_acceleration(30.0, "tomatoes")
    assert accel > 1.5, f"Thermal acceleration {accel} expected > 1.5"
    print("  [PASS] 1. Thermal Q10 model verified.")

    # 2. Test Spoilage Risk
    risk = estimate_spoilage_risk(
        remaining_shelf_life_hours=14.0,
        transit_hours=4.0,
        ambient_temp_celsius=32.0,
        commodity="tomatoes",
        is_refrigerated=False,
    )
    assert risk["is_feasible"] is True, "Expected feasible"
    assert risk["spoilage_risk_percent"] > 0.0, "Expected positive risk"
    print("  [PASS] 2. Spoilage risk transit calculation verified.")

    # 3. Test Discount Engine
    disc_rec = evaluate_discount_strategies(SAMPLE_BATCHES[0])
    assert len(disc_rec.options) == 7, f"Expected 7 options, got {len(disc_rec.options)}"
    assert any(opt.is_recommended for opt in disc_rec.options), "Expected recommended option"
    print("  [PASS] 3. 7-strategy discount pricing engine verified.")

    # 4. Test Greedy Solver
    greedy_plan = solve_with_greedy(
        SAMPLE_BATCHES, SAMPLE_DESTINATIONS, SAMPLE_VEHICLES, SAMPLE_ROUTES, SAMPLE_ORDERS
    )
    assert len(greedy_plan.allocations) > 0, "Greedy plan should have allocations"
    print(f"  [PASS] 4. Greedy heuristic solver verified ({len(greedy_plan.allocations)} allocations).")

    # 5. Test HiGHS Solver
    opt_plan = solve_with_highs(
        SAMPLE_BATCHES, SAMPLE_DESTINATIONS, SAMPLE_VEHICLES, SAMPLE_ROUTES, SAMPLE_ORDERS
    )
    assert opt_plan is not None, "HiGHS should return a valid plan"
    assert opt_plan.net_economic_value_inr > 0, "Net value should be positive"
    print(f"  [PASS] 5. HiGHS LP solver verified (INR {opt_plan.net_economic_value_inr:,.2f} net value).")

    # 6. Test Validator
    val = validate_dispatch_plan(opt_plan.allocations, SAMPLE_BATCHES, SAMPLE_VEHICLES, SAMPLE_DESTINATIONS)
    assert val.is_valid is True, f"Validation failed: {val.checks}"
    print(f"  [PASS] 6. Plan validator verified ({val.passed_checks}/{val.total_checks} checks passed).")

    # 7. Test Benchmark Evaluator
    bench = run_benchmark_evaluation(
        SAMPLE_BATCHES, SAMPLE_DESTINATIONS, SAMPLE_VEHICLES, SAMPLE_ROUTES, SAMPLE_ORDERS
    )
    assert len(bench.strategies) == 4, "Expected 4 benchmark strategies"
    print("  [PASS] 7. Multi-strategy benchmark comparison verified.")

    print("=" * 60)
    print("  ALL 7 CORE SYSTEM TESTS PASSED SUCCESSFULLY! ")
    print("=" * 60)


if __name__ == "__main__":
    run_checks()
