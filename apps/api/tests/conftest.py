"""Shared fixtures: temporary state and library, tagged audio, the mutation guard."""

import json
import os
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from typing import Required, TypedDict

import pytest
from rn_forge.commons import Process

from apollo_api.platform.settings import get_settings

pytest_plugins = ["pytester"]


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "library_mutation: touches a library outside tmp_path; run only by the acceptance procedure",
    )


class TrackSpec(TypedDict, total=False):
    title: Required[str]
    artist: Required[str]
    album: Required[str]
    genre: Required[str]
    albumartist: str
    track: int
    ext: str


_CODECS: dict[str, list[str]] = {
    "base.mp3": ["-c:a", "libmp3lame"],
    "base.m4a": ["-c:a", "aac"],
    "base.flac": ["-c:a", "flac"],
}


@pytest.fixture(scope="session")
def audio_fixtures(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("audio")
    for name, codec in _CODECS.items():
        Process.execute(
            f"fixture-{name}",
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=0.2",
            *codec,
            str(root / name),
        )
    return root


@pytest.fixture(autouse=True)
def configured_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest
) -> Iterator[dict[str, Path]]:
    state = tmp_path / ".apollo"
    library = tmp_path / "library"
    monkeypatch.setenv("APOLLO_STATE_DIR", str(state))
    monkeypatch.setenv("APOLLO_LIBRARY_ROOT", str(library))
    get_settings.cache_clear()
    yield {"state": state, "library": library}
    get_settings.cache_clear()
    value = os.environ.get("APOLLO_LIBRARY_ROOT")
    if request.node.get_closest_marker("library_mutation") or value is None:
        return
    if not Path(value).resolve().is_relative_to(tmp_path.resolve()):
        pytest.fail(
            f"APOLLO_LIBRARY_ROOT={value} is outside tmp_path; mark the test library_mutation",
            pytrace=False,
        )


@pytest.fixture
def fixture_library(
    audio_fixtures: Path, configured_env: dict[str, Path]
) -> Callable[[Sequence[TrackSpec]], Path]:
    library = configured_env["library"]

    def build(tracks: Sequence[TrackSpec]) -> Path:
        for spec in tracks:
            ext = spec.get("ext", "mp3")
            albumartist = spec.get("albumartist", spec["artist"])
            dest = (
                library
                / spec["genre"]
                / albumartist
                / spec["album"]
                / f"{spec['title']}.{ext}"
            )
            dest.parent.mkdir(parents=True, exist_ok=True)
            Process.execute(
                f"fixture-{spec['title']}",
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(audio_fixtures / f"base.{ext}"),
                "-c",
                "copy",
                "-metadata",
                f"title={spec['title']}",
                "-metadata",
                f"artist={spec['artist']}",
                "-metadata",
                f"album_artist={albumartist}",
                "-metadata",
                f"album={spec['album']}",
                "-metadata",
                f"genre={spec['genre']}",
                "-metadata",
                f"track={spec.get('track', 1)}",
                str(dest),
            )
        return library

    return build


def probe_tags(path: Path) -> dict[str, str]:
    result = Process.execute(
        "probe-tags",
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format_tags",
        "-of",
        "json",
        str(path),
    )
    data = json.loads(result.stdout or "{}")
    tags: dict[str, str] = data.get("format", {}).get("tags", {})
    return {key.lower(): value for key, value in tags.items()}


@pytest.fixture
def probe_tags_fn() -> Callable[[Path], dict[str, str]]:
    return probe_tags
