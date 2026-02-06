from __future__ import annotations

import asyncio
import logging

from app.core.logging import configure_logging
from app.db.session import engine
from app.integrations.redis import close_redis, get_redis
from app.integrations.sentry import init_sentry


async def run() -> None:
    configure_logging()
    init_sentry()

    logger = logging.getLogger("worker")
    logger.info("worker starting")

    try:
        redis = get_redis()
        await redis.ping()
        logger.info("redis ping ok")
    except Exception:
        logger.exception("redis ping failed")

    try:
        while True:
            await asyncio.sleep(5)
    finally:
        await close_redis()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run())
