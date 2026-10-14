"""Repository for destination markets, wholesale mandis and retail hubs."""
from typing import List, Optional, Dict, Any
from app.db.repositories.base import BaseRepository
from app.db.sample_data import SAMPLE_DESTINATIONS


class DestinationRepository(BaseRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(table_name="destinations", initial_data=SAMPLE_DESTINATIONS)

    async def get_by_city(self, city: str) -> List[Dict[str, Any]]:
        all_dests = await self.get_all()
        return [d for d in all_dests if d.get("city", "").lower() == city.lower()]

    async def get_by_market_type(self, market_type: str) -> List[Dict[str, Any]]:
        all_dests = await self.get_all()
        return [d for d in all_dests if d.get("market_type", "").lower() == market_type.lower()]


destination_repo = DestinationRepository()
