"""Repository for transit routes and distance matrix."""
from typing import List, Optional, Dict, Any
from app.db.repositories.base import BaseRepository
from app.db.sample_data import SAMPLE_ROUTES


class RouteRepository(BaseRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(table_name="routes", initial_data=SAMPLE_ROUTES)

    async def get_route(self, origin_name: str, destination_id: str) -> Optional[Dict[str, Any]]:
        routes = await self.get_all()
        for r in routes:
            if (
                r.get("destination_id") == destination_id
                and origin_name.lower() in r.get("origin_name", "").lower()
            ):
                return r
        # Fallback by destination_id
        for r in routes:
            if r.get("destination_id") == destination_id:
                return r
        return None


route_repo = RouteRepository()
