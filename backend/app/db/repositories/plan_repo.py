"""Repository for optimization dispatch plans and historical runs."""
from typing import List, Optional, Dict, Any
from app.db.repositories.base import BaseRepository


class PlanRepository(BaseRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(table_name="dispatch_plans", initial_data=[])

    async def get_latest_plan(self) -> Optional[Dict[str, Any]]:
        plans = await self.get_all()
        if not plans:
            return None
        return sorted(plans, key=lambda x: str(x.get("created_at", "")), reverse=True)[0]


plan_repo = PlanRepository()
