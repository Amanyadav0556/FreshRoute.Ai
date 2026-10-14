"""App configuration using pydantic-settings."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = "https://YOUR_PROJECT_REF.supabase.co"
    supabase_service_role_key: str = ""
    database_url: str = ""

    # Optimization
    solver_timeout_seconds: int = 30
    solver_fallback: str = "greedy"

    # App
    env: str = "development"
    log_level: str = "info"
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    @property
    def supabase_configured(self) -> bool:
        return (
            self.supabase_url != "https://YOUR_PROJECT_REF.supabase.co"
            and bool(self.supabase_service_role_key)
        )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
