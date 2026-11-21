"""S1.9.1: fixtures and the library-mutation guard."""

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

import pytest

Spec = Mapping[str, str | int]


def test_s1_9_1_1_fixture_library(
    fixture_library: Callable[[Sequence[Spec]], Path],
    configured_env: dict[str, Path],
    probe_tags_fn: Callable[[Path], dict[str, str]],
) -> None:
    tracks: list[Spec] = [
        {
            "title": "So What",
            "artist": "Miles Davis",
            "album": "Kind of Blue",
            "genre": "Jazz",
            "track": 1,
            "ext": "mp3",
        },
        {
            "title": "Freddie Freeloader",
            "artist": "Miles Davis",
            "album": "Kind of Blue",
            "genre": "Jazz",
            "track": 2,
            "ext": "m4a",
        },
        {
            "title": "Army of Me",
            "artist": "Björk",
            "album": "Post",
            "genre": "Electronic",
            "ext": "flac",
        },
    ]
    root = fixture_library(tracks)
    assert root == configured_env["library"]
    for spec in tracks:
        path = (
            root
            / str(spec["genre"])
            / str(spec.get("albumartist", spec["artist"]))
            / str(spec["album"])
            / f"{spec['title']}.{spec['ext']}"
        )
        assert path.is_file()
        tags = probe_tags_fn(path)
        for key in ("title", "artist", "album", "genre"):
            assert tags[key] == spec[key]
        assert tags["track"].startswith(str(spec.get("track", 1)))


def test_s1_9_1_2_guard(pytester: pytest.Pytester) -> None:
    pytester.makeconftest(Path(__file__).with_name("conftest.py").read_text())
    pytester.makepyfile(
        """
        import pytest

        def test_noop():
            pass

        def test_outside(monkeypatch):
            monkeypatch.setenv("APOLLO_LIBRARY_ROOT", "/somewhere/else")

        @pytest.mark.library_mutation
        def test_marked(monkeypatch):
            monkeypatch.setenv("APOLLO_LIBRARY_ROOT", "/somewhere/else")
        """
    )
    result = pytester.runpytest("-p", "no:cacheprovider")
    result.assert_outcomes(passed=3, errors=1)
    result.stdout.fnmatch_lines(["*outside tmp_path; mark the test library_mutation*"])
