"""Base repository abstraction providing dual-mode data access:
1. Supabase PostgreSQL via supabase client when credentials exist
2. High-fidelity in-memory state fallback when running standalone / demo mode
"""
from typing import Generic, TypeVar, List, Optional, Dict, Any
from app.core.config import settings
from app.core.supabase_client import get_supabase_client

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, table_name: str, initial_data: Optional[List[Dict[str, Any]]] = None):
        self.table_name = table_name
        self._memory_store: List[Dict[str, Any]] = [dict(item) for item in (initial_data or [])]
        self._client = get_supabase_client() if settings.supabase_configured else None

    @property
    def is_supabase(self) -> bool:
        return self._client is not None

    async def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if self.is_supabase:
            query = self._client.table(self.table_name).select("*")
            if filters:
                for k, v in filters.items():
                    query = query.eq(k, v)
            resp = query.execute()
            return resp.data or []
        
        # Memory fallback
        results = self._memory_store
        if filters:
            results = [
                item for item in results
                if all(item.get(k) == v for k, v in filters.items())
            ]
        return results

    async def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        if self.is_supabase:
            resp = self._client.table(self.table_name).select("*").eq("id", item_id).execute()
            return resp.data[0] if resp.data else None
        
        for item in self._memory_store:
            if item.get("id") == item_id:
                return item
        return None

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.is_supabase:
            resp = self._client.table(self.table_name).insert(data).execute()
            return resp.data[0] if resp.data else data
        
        self._memory_store.append(data)
        return data

    async def update(self, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self.is_supabase:
            resp = self._client.table(self.table_name).update(updates).eq("id", item_id).execute()
            return resp.data[0] if resp.data else None
        
        for i, item in enumerate(self._memory_store):
            if item.get("id") == item_id:
                self._memory_store[i].update(updates)
                return self._memory_store[i]
        return None

    async def delete(self, item_id: str) -> bool:
        if self.is_supabase:
            self._client.table(self.table_name).delete().eq("id", item_id).execute()
            return True
        
        before_len = len(self._memory_store)
        self._memory_store = [x for x in self._memory_store if x.get("id") != item_id]
        return len(self._memory_store) < before_len
