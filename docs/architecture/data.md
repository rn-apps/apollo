# Data

Built by: E1

apollo keeps two SQLite databases and a runtime tree. Audio files stay the
source of truth ([ADR-0001](../adr/ADR-0001.md)).

## Two databases

|  | `library.db` | `apollo.db` |
| -- | -- | -- |
| Owner | beets | apollo |
| Access | only on the actor ([ADR-0005](../adr/ADR-0005.md)); no application SQL | one async SQLAlchemy engine ([ADR-0021](../adr/ADR-0021.md)) |
| Holds | beets `items`, `albums` and flexible attributes | jobs, audit, playlists, annotations, settings, check and Apple caches |
| Rebuilt by | a scan | not reconstructible as a whole; each table is state or a cache (below) |
| Schema change | beets' own startup migration | Alembic, forward only |

Both live in `.apollo/db/`. Back up that directory and the external library
before manual recovery.

## apollo.db

Engine: `create_sqlite_engine` with WAL, `busy_timeout` 5000 ms, foreign keys
on, `synchronous=NORMAL`. Transactions are short. Models derive from the kit
`Base` with its naming convention. Enums are stored as `VARCHAR` with no check
constraint, so a new value needs no migration.

Migrations ship inside the package as `apollo_api:migrations` and run at startup
through `run_migrations` in a thread. The history starts at one baseline that
creates every table below.

| Table | Holds | Kind |
| -- | -- | -- |
| `job` | type, state, progress, payload, result, timestamps | state |
| `job_log` | log lines per job | state |
| `audit_entry` | operation, inverse, `batch_id`, target, trash reference | state |
| `playlist` | name, kind (`static` or `smart`), query, Apple origin columns | state |
| `playlist_track` | ordered membership of a static playlist | state |
| `setting` | run-time settings changed through the API | state |
| `artist_annotation` | facts no frame can carry, keyed on the normalised artist name ([ADR-0010](../adr/ADR-0010.md)) | state |
| `album_annotation` | the same for albums, keyed on the album directory | state |
| `track_check` | check findings, keyed `(path, mtime)` | cache |
| `apple_stat` | play counts and loved flags from the Music.app XML, keyed on source path, with `imported_at` | cache |

There is no `saved_search` table ([ADR-0015](../adr/ADR-0015.md)). `AuditOp`
values are `tag_write`, `file_move`, `file_replace`, `item_add`, `item_remove`,
`inbox_promote`, `export` and `playlist_write`.

The annotation tables hold only artist type, sort name, dates, country, avatar,
notes and the no-split flag for artists, and edition, catalogue number, purchase
date and notes for albums. A test asserts that no annotation field duplicates
something a frame carries; the old `mb_artistid` is a known candidate and is not
ported without it.

## Cache rules

A table is either state or an explicit repeatable cache. A feature that stores
something new says which rule covers it.

- `track_check` is keyed `(path, mtime)`. A changed file invalidates its row by
  key. `checked_at` null means never checked and must not render as no errors.
- `apple_stat` is keyed on the source path and stamped with `imported_at`. The
  UI labels play counts and loved flags with that stamp. apollo never
  increments a count or writes one back.
- Snapshots in memory are never persisted
  ([Actor and caches](actor-and-caches.md#snapshots)).
- Scan-time attributes in `library.db` (`apollo_filesize`,
  `apollo_file_missing`, `apollo_has_art`, `apollo_multidisc`) mean "as of the
  last scan or check" ([ADR-0013](../adr/ADR-0013.md)). `apollo_has_art` is
  three-valued: unknown, present, absent.

## Runtime tree

`APOLLO_STATE_DIR` (default `.apollo/`, gitignored) holds everything apollo
writes outside the library.

| Path | Holds |
| -- | -- |
| `config/config.yaml` | generated beets configuration |
| `db/library.db`, `db/apollo.db` | the two databases |
| `db/backups/` | beets migration backups |
| `logs/` | rotating `apollo*` log files, readable from Maintenance |
| `inbox/` | staged media awaiting promotion ([ADR-0018](../adr/ADR-0018.md)) |
| `trash/` | audit backups: replaced and deleted files ([ADR-0009](../adr/ADR-0009.md)) |
| `cache/` | artwork thumbnails |
| `work/` | temporary files for replace and trim |
| `reports/` | generated reports and the Apple export file ([ADR-0017](../adr/ADR-0017.md)) |

`PathUtils.assert_within` guards every write against escaping its root. The
library root is `APOLLO_LIBRARY_ROOT`.

## Beets configuration

beets is the tag and index layer only: no autotag, no import. `Settings` writes
`config/config.yaml` at startup with these values:

| Key | Value |
| -- | -- |
| `id3v23` | false |
| `per_disc_numbering` | as in the old config (open: see E1) |
| `threaded` | false |
| `import.copy`, `move`, `write`, `autotag` | false |
| `import.incremental` | true |
| `import.duplicate_action` | skip |
| `asciify_paths` | true |
| `replace` | the character replacement map |
| `directory`, `library` | `APOLLO_LIBRARY_ROOT`, `db/library.db` |

Tags are written as ID3v2.4 and a guard asserts it. The custom fields are
registered in `media/mediafields`. Path expectations always come from beets' own
destination ([ADR-0014](../adr/ADR-0014.md)), so the asciify and replace
settings are part of the contract.

## Pruning

Pruning history deletes audit batches older than a TTL (default 90 days, run
manually) together with their trash backups in one transaction. Emptying trash
removes only payloads no audit entry references. Both are audited
([ADR-0009](../adr/ADR-0009.md)).
