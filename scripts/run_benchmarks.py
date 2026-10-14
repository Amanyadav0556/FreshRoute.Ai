#!/usr/bin/env python3
"""FreshRoute AI — CLI Benchmark Runner
Executes multi-strategy optimization benchmarks and outputs comparative terminal tables.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.sample_data import (
    SAMPLE_BATCHES,
    SAMPLE_DESTINATIONS,
    SAMPLE_VEHICLES,
    SAMPLE_ROUTES,
    SAMPLE_ORDERS,
)
from app.services.evaluator import run_benchmark_evaluation


def main():
    print("=" * 80)
    print("  FreshRoute AI — Multi-Strategy Benchmark Evaluation Suite")
    print("  Testing: FEFO vs. Highest Price vs. Greedy Heuristic vs. HiGHS Optimizer")
    print("=" * 80)

    result = run_benchmark_evaluation(
        batches=SAMPLE_BATCHES,
        destinations=SAMPLE_DESTINATIONS,
        vehicles=SAMPLE_VEHICLES,
        routes=SAMPLE_ROUTES,
        orders=SAMPLE_ORDERS,
    )

    print(f"\nScenario: {result.scenario_name}")
    print(f"Total Produce Volume: {result.total_batch_volume_kg:,.1f} kg")
    print(f"Total Market Demand: {result.total_market_demand_kg:,.1f} kg\n")

    header = f"{'Strategy':<38} | {'Net Value (₹)':<14} | {'Revenue (₹)':<13} | {'Spoil (kg)':<10} | {'Fulfill %':<9} | {'Time (ms)':<9}"
    print(header)
    print("-" * len(header))

    for strat in result.strategies:
        print(
            f"{strat.strategy_label:<38} | "
            f"₹{strat.net_economic_value_inr:>12,.2f} | "
            f"₹{strat.total_revenue_inr:>11,.2f} | "
            f"{strat.spoilage_quantity_kg:>8,.1f}kg | "
            f"{strat.order_fulfillment_rate_percent:>7.1f}% | "
            f"{strat.computation_time_ms:>7.1f}ms"
        )

    print("\n" + "=" * 80)
    print("  Key Value Add: FreshRoute HiGHS Optimizer vs Industry FEFO Baseline")
    print("=" * 80)

    for comp in result.comparisons:
        print(
            f"• {comp.metric_label}: {comp.freshroute_optimizer:,.1f} {comp.unit} "
            f"(vs FEFO {comp.fefo_baseline:,.1f} {comp.unit}) -> "
            f"Improvement: {comp.improvement_vs_fefo_percent:+.1f}%"
        )

    print("\n[SUCCESS] Benchmark simulation completed with valid mathematical constraints.\n")


if __name__ == "__main__":
    main()
