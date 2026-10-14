#!/usr/bin/env python3
"""FreshRoute AI — Synthetic Batch Generator
Generates realistic agricultural produce batches with randomized shelf lives,
quantities, and price thresholds for stress testing the LP optimizer.
"""
import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

COMMODITIES = [
    {"name": "Tomatoes", "base_price": 24.0, "shelf_hours": 72.0, "cost": 18.0},
    {"name": "Spinach (Palak)", "base_price": 20.0, "shelf_hours": 28.0, "cost": 12.0},
    {"name": "Grapes", "base_price": 60.0, "shelf_hours": 120.0, "cost": 45.0},
    {"name": "Onions", "base_price": 26.0, "shelf_hours": 480.0, "cost": 19.0},
    {"name": "Mangoes", "base_price": 95.0, "shelf_hours": 96.0, "cost": 65.0},
    {"name": "Capsicum", "base_price": 38.0, "shelf_hours": 60.0, "cost": 28.0},
]


def generate_batches(count: int = 50) -> List[Dict[str, Any]]:
    batches = []
    now = datetime.now(timezone.utc)

    for i in range(1, count + 1):
        comm = random.choice(COMMODITIES)
        init_shelf = comm["shelf_hours"]
        # Generate shelf life distribution: 20% critical (<12h), 30% urgent (<24h), 50% normal
        p = random.random()
        if p < 0.20:
            rsl = round(random.uniform(4.0, 11.5), 1)
        elif p < 0.50:
            rsl = round(random.uniform(12.0, 23.5), 1)
        else:
            rsl = round(random.uniform(24.0, init_shelf), 1)

        qty = round(random.uniform(400.0, 4500.0), 0)
        cost = comm["cost"] * random.uniform(0.9, 1.1)
        floor_price = cost * random.uniform(1.15, 1.35)

        batches.append({
            "id": f"synth-batch-{i:03d}",
            "batch_code": f"BATCH-SYNTH-{comm['name'][:3].upper()}-{i:03d}",
            "commodity": comm["name"],
            "collection_centre_id": "hub-nashik-01",
            "initial_quantity_kg": qty,
            "current_quantity_kg": qty,
            "harvest_date": (now - timedelta(hours=init_shelf - rsl)).isoformat(),
            "initial_shelf_life_hours": init_shelf,
            "remaining_shelf_life_hours": rsl,
            "storage_condition": "ambient",
            "procurement_cost_per_kg": round(cost, 2),
            "min_selling_price_per_kg": round(floor_price, 2),
            "quality_grade": random.choice(["Grade A", "Grade B"]),
            "provenance": "simulated",
        })

    return batches


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    batches = generate_batches(count)
    print(f"Generated {len(batches)} synthetic produce batches successfully.")
    print(f"Sample: {batches[0]}")
