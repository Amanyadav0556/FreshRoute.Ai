"""Repositories package exporting data access singletons."""
from app.db.repositories.base import BaseRepository
from app.db.repositories.batch_repo import batch_repo, BatchRepository
from app.db.repositories.destination_repo import destination_repo, DestinationRepository
from app.db.repositories.vehicle_repo import vehicle_repo, VehicleRepository
from app.db.repositories.route_repo import route_repo, RouteRepository
from app.db.repositories.order_repo import order_repo, OrderRepository
from app.db.repositories.plan_repo import plan_repo, PlanRepository

__all__ = [
    "BaseRepository",
    "batch_repo",
    "BatchRepository",
    "destination_repo",
    "DestinationRepository",
    "vehicle_repo",
    "VehicleRepository",
    "route_repo",
    "RouteRepository",
    "order_repo",
    "OrderRepository",
    "plan_repo",
    "PlanRepository",
]
