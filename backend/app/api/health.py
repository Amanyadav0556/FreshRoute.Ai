"""Health and system readiness endpoints."""
from fastapi import APIRouter
from datetime import datetime, timezone
from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """Returns service health status, environment, and database mode."""
    return {
        "status": "healthy",
        "service": "FreshRoute AI Optimization Engine",
        "version": "1.0.0",
        "environment": settings.env,
        "supabase_configured": settings.supabase_configured,
        "data_mode": "supabase_postgresql" if settings.supabase_configured else "in_memory_sample_mode",
        "solver": "HiGHS LP/MILP (SciPy) + Greedy Fallback",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
