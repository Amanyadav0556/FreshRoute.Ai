"""Pydantic schemas package for FreshRoute AI."""
from app.schemas.common import DataProvenance, UrgencyLevel, FleetStatus, AllocationStatus
from app.schemas.batch import BatchCreate, BatchUpdate, BatchResponse, BatchFilter
from app.schemas.destination import DestinationCreate, DestinationResponse
from app.schemas.vehicle import VehicleCreate, VehicleResponse, FleetSummary
from app.schemas.route import RouteCreate, RouteResponse
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.plan import PlanRequest, PlanResponse, PlanItem, PlanValidationResult
from app.schemas.discount import DiscountOption, DiscountRecommendationResponse
from app.schemas.alert import SpoilageAlert, RedistributionCandidate
from app.schemas.evaluation import BenchmarkResult, StrategyMetrics
from app.schemas.scenario import ScenarioDefinition, ScenarioRunRequest
from app.schemas.dashboard import DashboardMetrics

__all__ = [
    "DataProvenance",
    "UrgencyLevel",
    "FleetStatus",
    "AllocationStatus",
    "BatchCreate",
    "BatchUpdate",
    "BatchResponse",
    "BatchFilter",
    "DestinationCreate",
    "DestinationResponse",
    "VehicleCreate",
    "VehicleResponse",
    "FleetSummary",
    "RouteCreate",
    "RouteResponse",
    "OrderCreate",
    "OrderResponse",
    "PlanRequest",
    "PlanResponse",
    "PlanItem",
    "PlanValidationResult",
    "DiscountOption",
    "DiscountRecommendationResponse",
    "SpoilageAlert",
    "RedistributionCandidate",
    "BenchmarkResult",
    "StrategyMetrics",
    "ScenarioDefinition",
    "ScenarioRunRequest",
    "DashboardMetrics",
]
