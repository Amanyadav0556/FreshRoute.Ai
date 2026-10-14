"""
FreshRoute AI — FastAPI Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api import health, batches, destinations, vehicles, routes, orders, plans, evaluations, assumptions, dashboard

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FreshRoute AI backend starting up...")
    logger.info(f"Environment: {settings.env}")
    if not settings.supabase_url or settings.supabase_url == "https://YOUR_PROJECT_REF.supabase.co":
        logger.warning(
            "⚠️  Supabase credentials not configured. "
            "Running in SAMPLE DATA mode — no data will be persisted."
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
app.include_router(evaluations.router, prefix="/api/evaluations", tags=["Evaluations"])
app.include_router(assumptions.router, prefix="/api/assumptions", tags=["Assumptions"])
