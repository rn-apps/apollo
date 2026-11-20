"""S1.2.2: logging to the runtime tree."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apollo_api.app import create_app
from apollo_api.platform.settings import get_settings


@pytest.fixture(autouse=True)
def runtime_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("APOLLO_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("APOLLO_LIBRARY_ROOT", str(tmp_path / "library"))
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def _log_text(tmp_path: Path) -> str:
    files = sorted((tmp_path / "state" / "logs").glob("apollo*"))
    return "".join(f.read_text() for f in files)


def test_s1_2_2_1_log_file_written(tmp_path: Path) -> None:
    with TestClient(create_app()):
        pass
    assert list((tmp_path / "state" / "logs").glob("apollo*"))
    assert "apollo started" in _log_text(tmp_path)
    assert (tmp_path / "state" / "config" / "config.yaml").exists()


def test_s1_2_2_2_server_error_logged(tmp_path: Path) -> None:
    application = create_app()

    async def boom() -> None:
        raise RuntimeError("kaboom")

    application.add_api_route("/boom", boom)
    with TestClient(application, raise_server_exceptions=False) as client:
        assert client.get("/boom").status_code == 500
    text = _log_text(tmp_path)
    assert "problem.server_error" in text
    assert "RuntimeError: kaboom" in text
