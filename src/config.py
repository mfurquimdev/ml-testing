"""Module containing configuration for both backend server and cli."""
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    server_address: str = "http://localhost"
    port_number: int = 44681


backend_settings = BackendSettings()


__all__ = ["backend_settings"]
