"""Spoilage alert and emergency redistribution endpoints."""
from fastapi import APIRouter, Query
from typing import List

from app.schemas.alert import SpoilageAlert
from app.db.repositories.batch_repo import batch_repo
from app.db.repositories.destination_repo import destination_repo
from app.db.repositories.route_repo import route_repo
from app.services.alert_service import generate_spoilage_alerts

router = APIRouter()


@router.get("", response_model=List[SpoilageAlert])
async def list_spoilage_alerts(threshold_hours: float = Query(24.0, ge=4.0, le=72.0)):
    """Retrieves all batches at risk of spoilage with feasible emergency alternative destinations."""
    batches = await batch_repo.get_all()
    destinations = await destination_repo.get_all()
    routes = await route_repo.get_all()

    return generate_spoilage_alerts(
        batches=batches,
        destinations=destinations,
        routes=routes,
        threshold_hours=threshold_hours,
    )
