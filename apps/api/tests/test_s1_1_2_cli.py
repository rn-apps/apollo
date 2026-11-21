"""S1.1.2: ``apollo-api serve`` runs the app."""

from collections.abc import Iterator

import pytest
import uvicorn

from apollo_api.cli import main, uvicorn_config
from apollo_api.platform.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.delenv("APOLLO_BIND_HOST", raising=False)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_s1_1_2_1_serve_builds_uvicorn_config(monkeypatch: pytest.MonkeyPatch) -> None:
    config = uvicorn_config(Settings(_env_file=None, bind_host="0.0.0.0"))
    assert config.host == "0.0.0.0"
    assert config.port == 8000
    assert config.app == "apollo_api.app:app"

    monkeypatch.setenv("APOLLO_BIND_HOST", "127.0.0.2")
    configs: list[uvicorn.Config] = []

    def fake_run(self: uvicorn.Server, *args: object, **kwargs: object) -> None:
        configs.append(self.config)

    monkeypatch.setattr(uvicorn.Server, "run", fake_run)
    assert main.run(["serve"]) == 0
    assert len(configs) == 1
    assert configs[0].host == "127.0.0.2"
    assert configs[0].port == 8000
