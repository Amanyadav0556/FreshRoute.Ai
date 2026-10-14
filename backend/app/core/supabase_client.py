"""Supabase client — service-role key stays server-side only.
Includes graceful fallback if the supabase-py SDK is not installed in the environment.
"""
from typing import Optional, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = Any

_client: Optional[Any] = None


def get_supabase() -> Optional[Any]:
    """Return Supabase client or None when credentials are missing or SDK not installed."""
    global _client
    if _client is not None:
        return _client
    if not settings.supabase_configured:
        logger.warning("Supabase not configured — running in sample data mode.")
        return None
    if create_client is None:
        logger.warning("Supabase SDK not installed — falling back to sample data mode.")
        return None
    try:
        _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        return _client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None


get_supabase_client = get_supabase
