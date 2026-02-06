from __future__ import annotations

from dataclasses import dataclass
import os


def _get_env(key: str, default: str) -> str:
    value = os.getenv(key)
    return value if value is not None else default


def _get_bool(key: str, default: bool) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_float(key: str, default: float) -> float:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = _get_env("APP_NAME", "project-be-api")
    app_env: str = _get_env("APP_ENV", "local")
    log_level: str = _get_env("LOG_LEVEL", "INFO")

    database_url: str = _get_env(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/project_be",
    )
    redis_url: str = _get_env("REDIS_URL", "redis://localhost:6379/0")

    sentry_dsn: str = _get_env("SENTRY_DSN", "")
    sentry_traces_sample_rate: float = _get_float("SENTRY_TRACES_SAMPLE_RATE", 0.0)

    enable_health_checks: bool = _get_bool("ENABLE_HEALTH_CHECKS", True)


settings = Settings()
