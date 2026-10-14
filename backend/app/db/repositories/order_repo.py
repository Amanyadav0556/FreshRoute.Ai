"""Repository for buyer purchase orders and market demand."""
from typing import List, Optional, Dict, Any
from app.db.repositories.base import BaseRepository
from app.db.sample_data import SAMPLE_ORDERS


class OrderRepository(BaseRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(table_name="orders", initial_data=SAMPLE_ORDERS)

    async def get_active_orders(self) -> List[Dict[str, Any]]:
        orders = await self.get_all()
        return [o for o in orders if o.get("status") in ["pending", "allocated"]]

    async def get_orders_by_commodity(self, commodity: str) -> List[Dict[str, Any]]:
        orders = await self.get_all()
        return [o for o in orders if commodity.lower() in o.get("commodity", "").lower()]

    async def record_allocation(self, order_id: str, allocated_kg: float) -> Optional[Dict[str, Any]]:
        order = await self.get_by_id(order_id)
        if not order:
            return None
        current_alloc = float(order.get("allocated_quantity_kg", 0.0)) + allocated_kg
        demanded = float(order.get("demanded_quantity_kg", 1.0))
        rate = round(min(100.0, (current_alloc / demanded) * 100.0), 1)
        status = "fulfilled" if current_alloc >= demanded else "partially_fulfilled"
        return await self.update(
            order_id,
            {
                "allocated_quantity_kg": current_alloc,
                "fulfillment_rate_percent": rate,
                "status": status,
            },
        )


order_repo = OrderRepository()
