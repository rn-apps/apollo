"""S1.2.1: settings and the runtime tree."""

from pathlib import Path

import pytest
from rn_forge.commons import YamlUtils

from apollo_api.platform.runtime import beets_config, prepare
from apollo_api.platform.settings import Settings

ENV_NAMES = (
    "APOLLO_STATE_DIR",
    "APOLLO_LIBRARY_ROOT",
    "APOLLO_MUSIC_XML_PATH",
    "APOLLO_DEFAULT_PAGE_SIZE",
    "APOLLO_BIND_HOST",
    "APOLLO_APPLE_RELOCATION_VERIFIED",
    "APOLLO_JOB_HISTORY_LIMIT",
)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        _env_file=None,
        state_dir=tmp_path / "state",
        library_root=tmp_path / "library",
    )


def _snapshot(root: Path) -> dict[Path, bytes | None]:
    return {p: (p.read_bytes() if p.is_file() else None) for p in root.rglob("*")}


def test_s1_2_1_1_defaults():
    settings = Settings(_env_file=None)
    assert settings.state_dir == Path(".apollo")
    assert settings.library_root == Path.home() / "Music" / "Library"
    assert settings.music_xml_path is None
    assert settings.default_page_size == 100
    assert settings.bind_host == "127.0.0.1"
    assert settings.apple_relocation_verified is False
    assert settings.job_history_limit == 500
    assert not hasattr(settings, "jobs_autostart")


def test_s1_2_1_2_env_overrides(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    env_file = tmp_path / ".env"
    env_file.write_text("APOLLO_DEFAULT_PAGE_SIZE=10\nAPOLLO_JOB_HISTORY_LIMIT=7\n")
    monkeypatch.setenv("APOLLO_DEFAULT_PAGE_SIZE", "25")
    monkeypatch.setenv("APOLLO_BIND_HOST", "0.0.0.0")
    monkeypatch.setenv("APOLLO_APPLE_RELOCATION_VERIFIED", "true")
    settings = Settings(_env_file=env_file)
    assert settings.default_page_size == 25
    assert settings.job_history_limit == 7
    assert settings.bind_host == "0.0.0.0"
    assert settings.apple_relocation_verified is True


def test_s1_2_1_3_prepare_creates_tree(tmp_path: Path):
    settings = _settings(tmp_path)
    prepare(settings)
    state = tmp_path / "state"
    for name in (
        "config",
        "db",
        "db/backups",
        "logs",
        "inbox",
        "trash",
        "cache",
        "work",
        "reports",
    ):
        assert (state / name).is_dir()
    assert (state / "config" / "config.yaml").exists()
    assert not (tmp_path / "library").exists()
    before = _snapshot(state)
    prepare(settings)
    assert _snapshot(state) == before


def test_s1_2_1_4_beets_config(tmp_path: Path):
    settings = _settings(tmp_path)
    prepare(settings)
    read = YamlUtils.read_file(tmp_path / "state" / "config" / "config.yaml")
    assert read == beets_config(settings)
    assert read["id3v23"] is False
    assert read["per_disc_numbering"] is True
    assert read["threaded"] is False
    assert read["timid"] is True
    imp = read["import"]
    assert imp["copy"] is False
    assert imp["move"] is False
    assert imp["write"] is False
    assert imp["autotag"] is False
    assert imp["incremental"] is True
    assert imp["duplicate_action"] == "skip"
    assert read["asciify_paths"] is True
    assert read["replace"] == {
        "[\\\\/]": "_",
        "[:]": "_",
        "[\\x00-\\x1f]": "",
        "^\\.": "_",
        "^\\s+": "",
        "\\s+$": "",
    }
    assert read["directory"] == str((tmp_path / "library").resolve())
    assert read["library"] == str((tmp_path / "state" / "db" / "library.db").resolve())
    assert read["paths"]["default"] == "%first{$genres}/$albumartist/$album/$title"
