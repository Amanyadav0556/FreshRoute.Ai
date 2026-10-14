"""FreshRoute AI — FastAPI Backend Entry Point
"""
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
import logging

from app.core.config import settings
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

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FreshRoute AI backend starting up...")
    logger.info(f"Environment: {settings.env}")
    if not settings.supabase_configured:
        logger.warning(
            "⚠️  Supabase credentials not configured. "
            "Running in high-fidelity standalone SAMPLE DATA mode."
        )
    yield
    logger.info("FreshRoute AI backend shutting down.")


app = FastAPI(
    title="FreshRoute AI",
    description="Intelligent Perishable Produce Distribution & Discount Optimization API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, tags=["Health"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(batches.router, prefix="/api/batches", tags=["Batches"])
app.include_router(destinations.router, prefix="/api/destinations", tags=["Destinations"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(routes.router, prefix="/api/routes", tags=["Routes"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(plans.router, prefix="/api/plans", tags=["Plans"])
app.include_router(discounts.router, prefix="/api/discounts", tags=["Discounts"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(evaluations.router, prefix="/api/evaluations", tags=["Evaluations"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["Scenarios"])
app.include_router(assumptions.router, prefix="/api/assumptions", tags=["Assumptions"])


@app.post("/api/replans", tags=["Plans"])
async def replan_endpoint(payload: Dict[str, Any] = Body(default={})):
    """Replanning endpoint triggered on disruption changes."""
    scenario_id = payload.get("scenario_id")
    return await plans.execute_optimization(strategy="freshroute", scenario_id=scenario_id)
