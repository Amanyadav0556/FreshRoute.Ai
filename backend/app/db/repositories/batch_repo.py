"""Repository for perishable produce batches."""
from typing import List, Optional, Dict, Any
from app.db.repositories.base import BaseRepository
from app.db.sample_data import SAMPLE_BATCHES


class BatchRepository(BaseRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(table_name="produce_batches", initial_data=SAMPLE_BATCHES)

    async def get_at_risk_batches(self, threshold_hours: float = 24.0) -> List[Dict[str, Any]]:
        batches = await self.get_all()
        return [
            b for b in batches
            if float(b.get("remaining_shelf_life_hours", 999.0)) <= threshold_hours
            and float(b.get("current_quantity_kg", 0.0)) > 0
        ]

    async def update_remaining_quantities(self, batch_id: str, allocated_kg: float) -> Optional[Dict[str, Any]]:
        batch = await self.get_by_id(batch_id)
        if not batch:
            return None
        new_qty = max(0.0, float(batch.get("current_quantity_kg", 0.0)) - allocated_kg)
        return await self.update(batch_id, {"current_quantity_kg": new_qty})


batch_repo = BatchRepository()
