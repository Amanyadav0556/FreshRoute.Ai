"""Supabase client — service-role key stays server-side only."""
from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

_client: Client | None = None


def get_supabase() -> Client | None:
    """Return Supabase client or None when credentials are missing."""
    global _client
    if _client is not None:
        return _client
    if not settings.supabase_configured:
        logger.warning("Supabase not configured — returning None (sample data mode)")
        return None
    _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _client
