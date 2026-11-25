"""Command line entry point: ``apollo-api serve``."""

import uvicorn
from rn_forge.cli import CliApp

from apollo_api.platform.settings import Settings, get_settings

PORT = 8000
APP = "apollo_api.app:app"

main = CliApp("apollo-api", "Run the apollo API.")


def uvicorn_config(settings: Settings) -> uvicorn.Config:
    """Build the uvicorn configuration for the given settings."""
    return uvicorn.Config(APP, host=settings.bind_host, port=PORT)


@main.command()
def serve() -> None:
    """Serve the API on APOLLO_BIND_HOST, port 8000."""
    uvicorn.Server(uvicorn_config(get_settings())).run()
