"""The ASGI application: `task api:dev` serves `app`."""

from __future__ import annotations

from rn_forge.fastapi import AppConfig, FastApiApp
from rn_forge.web import NOT_FOUND, default_registry

from apollo_api.errors import ItemNotFound
from apollo_api.routes import router

registry = default_registry().register(ItemNotFound, NOT_FOUND)

app = FastApiApp(
    AppConfig(registry=registry),
    routers=(router,),
    title="apollo",
)
