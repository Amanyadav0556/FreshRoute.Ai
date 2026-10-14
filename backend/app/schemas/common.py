"""Common enums, base models and utility schemas."""
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

T = TypeVar("T")


class DataProvenance(str, Enum):
    REAL = "real"
    ESTIMATED = "estimated"
    SIMULATED = "simulated"


class UrgencyLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class FleetStatus(str, Enum):
    AVAILABLE = "available"
    EN_ROUTE = "en_route"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class AllocationStatus(str, Enum):
    DRAFT = "draft"
    OPTIMIZED = "optimized"
    CONFIRMED = "confirmed"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class BaseDomainModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True
    )


class ProvenanceMixin(BaseModel):
    provenance: DataProvenance = DataProvenance.REAL
    provenance_source: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
    page_size: int = 50
    has_next: bool = False
