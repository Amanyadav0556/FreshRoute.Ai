#!/usr/bin/env python3
"""FreshRoute AI — Metrics Exporter
Runs all benchmark strategies and exports a clean JSON report for hackathon presentation.
"""
import sys
import os
import json

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


def export():
    result = run_benchmark_evaluation(
        batches=SAMPLE_BATCHES,
        destinations=SAMPLE_DESTINATIONS,
        vehicles=SAMPLE_VEHICLES,
        routes=SAMPLE_ROUTES,
        orders=SAMPLE_ORDERS,
    )

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "benchmark_summary.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(mode="json"), f, indent=2)

    print(f"Exported benchmark summary to: {out_path}")


if __name__ == "__main__":
    export()
