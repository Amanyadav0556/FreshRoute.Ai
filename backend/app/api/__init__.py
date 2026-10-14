"""API router package for FreshRoute AI."""
from app.api import (
    health,
    dashboard,
    batches,
    destinations,
    vehicles,
    routes,
    orders,
    plans,
    discounts,
    alerts,
    evaluations,
    scenarios,
    assumptions,
)

__all__ = [
    "health",
    "dashboard",
    "batches",
    "destinations",
    "vehicles",
    "routes",
    "orders",
    "plans",
    "discounts",
    "alerts",
    "evaluations",
    "scenarios",
    "assumptions",
]
