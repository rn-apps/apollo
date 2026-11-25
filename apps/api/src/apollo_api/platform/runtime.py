"""The ``.apollo/`` runtime tree and the generated beets configuration."""

from pathlib import Path
from typing import Any

from rn_forge.commons import YamlUtils

from apollo_api.platform.settings import Settings

#: Directory part of Apollo's one path template. beets 2.13 stores genres plurally;
#: ``$genre`` resolves to the literal string "$genre", and bare ``$genres`` would join
#: a multi-genre track into a "Jazz; Blues" directory, so ``%first`` picks one folder.
PARENT = "%first{$genres}/$albumartist/$album"

#: Where every item belongs. One template, applied to singletons and compilations
#: alike; see the ``paths`` block in :func:`beets_config`.
TEMPLATE = f"{PARENT}/$title"


def runtime_dirs(settings: Settings) -> tuple[Path, ...]:
    """Return every directory of the runtime tree, parents first."""
    return (
        settings.state_dir,
        settings.config_path.parent,
        settings.beets_db_path.parent,
        settings.backups_path,
        settings.logs_path,
        settings.inbox_path,
        settings.trash_path,
        settings.cache_path,
        settings.work_path,
        settings.reports_path,
    )


def beets_config(settings: Settings) -> dict[str, Any]:
    """Return the generated beets configuration as plain data."""
    return {
        "directory": str(settings.library_root.expanduser().resolve()),
        "library": str(settings.beets_db_path.expanduser().resolve()),
        "id3v23": False,
        "per_disc_numbering": True,
        "threaded": False,
        "timid": True,
        "quiet_fallback": "skip",
        "import": {
            "copy": False,
            "move": False,
            "write": False,
            "autotag": False,
            "incremental": True,
            "resume": False,
            "duplicate_action": "skip",
        },
        "asciify_paths": True,
        "replace": {
            "[\\\\/]": "_",
            "[:]": "_",
            "[\\x00-\\x1f]": "",
            "^\\.": "_",
            "^\\s+": "",
            "\\s+$": "",
        },
        # ``singleton`` and ``comp`` must be stated even though they repeat
        # ``default``: beets' own config supplies them (``Non-Album/$artist/$title``
        # and ``Compilations/...``) and a user ``paths`` block merges over that map
        # rather than replacing it. Apollo scans files in place, so every item is a
        # singleton and beets' key won; ``Item.destination()`` answered
        # ``Non-Album/<artist>/<title>`` for the whole library. That made every
        # expected path wrong, silently emptied the Errors page's path-agreement
        # finding (the three-component path is too shallow for ``tags_from_path``),
        # and would have had Relocate propose moving the library into ``Non-Album``.
        "paths": {
            "apollo_multidisc:1": f"{PARENT}/Disc $disc/$title",
            "default": TEMPLATE,
            "singleton": TEMPLATE,
            "comp": TEMPLATE,
        },
        "plugins": [],
        "musicbrainz": {"enabled": False, "searchlimit": 5},
    }


def prepare(settings: Settings) -> None:
    """Create the runtime tree and write the beets configuration.

    The library root is deliberately not created: a typo in ``APOLLO_LIBRARY_ROOT``
    must stay visible.
    """
    for path in runtime_dirs(settings):
        path.expanduser().resolve().mkdir(parents=True, exist_ok=True)
    YamlUtils.write_file(
        beets_config(settings), settings.config_path.expanduser().resolve()
    )
