"""The ASGI application: `task api:dev` serves `app`.

The lifespan prepares the runtime tree and initialises logging to its
`logs/` directory once at startup.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rn_forge.commons import AppLogger
from rn_forge.fastapi import AppConfig, FastApiApp
from rn_forge.fastapi.problem import log_server_errors
from rn_forge.web import NOT_FOUND, default_registry

from apollo_api.errors import ItemNotFound
from apollo_api.platform.runtime import prepare
from apollo_api.platform.settings import get_settings
from apollo_api.routes import router

registry = default_registry().register(ItemNotFound, NOT_FOUND)

_LOG = AppLogger.get_logger("apollo")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """Prepare the runtime tree and start logging to its log file."""
    settings = get_settings()
    prepare(settings)
    AppLogger.initialize(
        root_logger_name="apollo",
        level=logging.INFO,
        file=str(settings.logs_path / "apollo"),
        update_loggers={
            "beets": logging.WARNING,
            "uvicorn.access": logging.WARNING,
            "uvicorn.error": logging.INFO,
        },
        force_reconfigure=True,
    )
    _LOG.info("apollo started | state_dir={}", settings.state_dir.resolve())
    yield


def create_app() -> FastApiApp:
    """Build the application, logging 5xx problems under the `apollo` logger."""
    return FastApiApp(
        AppConfig(
            registry=registry,
            log=log_server_errors(AppLogger.get_logger("apollo.http")),
        ),
        routers=(router,),
        title="apollo",
        lifespan=lifespan,
    )


app = create_app()
