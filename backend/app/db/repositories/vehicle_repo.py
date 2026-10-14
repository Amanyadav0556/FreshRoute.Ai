"""Repository for fleet vehicles and transport assets."""
from typing import List, Optional, Dict, Any
from app.db.repositories.base import BaseRepository
from app.db.sample_data import SAMPLE_VEHICLES


class VehicleRepository(BaseRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(table_name="vehicles", initial_data=SAMPLE_VEHICLES)

    async def get_available_vehicles(self) -> List[Dict[str, Any]]:
        vehicles = await self.get_all()
        return [v for v in vehicles if v.get("status") == "available"]

    async def get_refrigerated_vehicles(self) -> List[Dict[str, Any]]:
        vehicles = await self.get_all()
        return [v for v in vehicles if v.get("is_refrigerated") is True]

    async def update_status(self, vehicle_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        return await self.update(vehicle_id, {"status": new_status})


vehicle_repo = VehicleRepository()
