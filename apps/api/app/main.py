from fastapi import FastAPI

from app import __version__
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import engine
from app.integrations.redis import close_redis
from app.integrations.sentry import init_sentry


def create_app() -> FastAPI:
    configure_logging()
    init_sentry()

    app = FastAPI(title=settings.app_name, version=__version__)
    app.include_router(health_router)

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await close_redis()
        await engine.dispose()

    return app


app = create_app()
