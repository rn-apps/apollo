# Backend

Built by: E1

The backend is the Python package `apollo_api` in `apps/api/src/apollo_api/`. It
is layered one way and the layering is enforced by lint
([ADR-0019](../adr/ADR-0019.md)).

## Layers

Each layer imports only from layers above it in this table (lower number).

| # | Package | Holds |
| -- | -- | -- |
| 1 | `platform/` | `settings`, runtime paths, `errors` (`ApolloError` hierarchy), database engine and sessions, migrations runner, job runtime, event stream, logging. No music knowledge. |
| 2 | `media/` | Tag read and write (`tags`), artwork (`artwork`), audio probing (`quality`), tool detection (`tools`), file operations (`fsops`), custom beets fields (`mediafields`), the ID3v2.4 guard. |
| 3 | `index/` | The beets actor (`actor`), the track DTO projection (`dto`), snapshots (`cache`, `facets`, `stats`), offset paging (`paging`), scan (`scan`), path projection (`paths`), annotation lookup. |
| 4 | `proposals/`, `validation/`, `apple/` | Read-only tag proposals from path, filename and `.info.json`. Content checks (`checks`, `tagcheck`) and their fan-out. Music.app XML parsing, AppleScript calls, play statistics. |
| 5 | `workflows/` | The use cases: `tracks`, `audit`, `relocate`, `inbox`, `annotations`, `replacement`, `playlists`. Every dry run, audit entry and apply lives here. |
| 6 | `jobs/` | One handler per job type, each a thin adapter from a job context to a workflow. |
| 7 | `routes/` | HTTP only: validate, call one workflow or submit one job, translate the result. No domain logic. |

`proposals`, `validation` and `apple` are peers and do not import each other.
The contracts are in `.importlinter`, below kiln's block. ruff's complexity
limit of 10 stays as a backstop.

## Composition

`app.py` is the only composition root. It builds the module-level `app` as a
`FastApiApp`, mounts the routers under `/v1`, and passes a `lifespan`. Every
long-lived resource is created in the lifespan and stored on a typed state
object, not on untyped `app.state` attributes.

Startup order:

1. Settings load and validate.
1. Runtime directories under `.apollo/` are created.
1. `apollo.db` migrations run, forward only.
1. The beets actor starts and opens `library.db`.
1. Snapshot caches are constructed, empty and lazy.
1. The job worker starts: it recovers leftover jobs, then claims.
1. The event stream is enabled.

Shutdown drains in the reverse order. The worker stops claiming and waits up to
its shutdown grace for running handlers. The actor closes last among the users
of beets, then the engine is disposed.

## What platform wraps

| Platform piece | pykit symbol | Package |
| -- | -- | -- |
| Application object, security headers, body limit, health routes | `FastApiApp`, `AppConfig` | rn-forge-fastapi |
| Error hierarchy to problems | `register_hierarchy` on `ProblemRegistry` | rn-forge-web |
| Database engine | `create_sqlite_engine` | rn-forge-sqlalchemy |
| Migrations | `migrate.run_migrations`, called in a thread | rn-forge-sqlalchemy |
| Models | `Base`, `UTCDateTime`, `AuditMixin`, `VersionMixin` | rn-forge-sqlalchemy |
| Library actor | `ThreadActor[Library]` | rn-forge-commons |
| Fan-out inside handlers | `TaskPool.map_settled` | rn-forge-commons |
| Atomic write, move without clobber, prune empty parents, root guard | `PathUtils` | rn-forge-commons |
| Event stream framing, heartbeat, terminal error frame | `sse_response` (`rn_forge.fastapi.sse`) | rn-forge-fastapi |
| Logging, redaction | `AppLogger` | rn-forge-commons |
| Subprocesses (ffmpeg, ffprobe, osascript) | `Process.execute` | rn-forge-commons |

apollo keeps no copy of what these ship ([ADR-0002](../adr/ADR-0002.md)). The
job worker is apollo's own, on the async engine
([ADR-0007](../adr/ADR-0007.md)); the session factory is one
`async_sessionmaker` with `expire_on_commit=False`, provided by `platform`
([ADR-0021](../adr/ADR-0021.md)). Generic `platform` code carries no apollo
types, so a later move to pykit is mechanical.

## Settings

`platform/settings` is a pydantic-settings class with the `APOLLO_` prefix and
an optional `.env`. pykit has no environment-based settings loader.

| Variable | Default | Meaning |
| -- | -- | -- |
| `APOLLO_STATE_DIR` | `.apollo` | Root of the runtime tree ([Data](data.md)). |
| `APOLLO_LIBRARY_ROOT` | `~/Music/Library` | The managed music library. Not editable at run time. |
| `APOLLO_MUSIC_XML_PATH` | unset | A Music.app XML export to read instead of triggering a fresh one. |
| `APOLLO_DEFAULT_PAGE_SIZE` | 100 | Page size when a list request omits it. |
| `APOLLO_BIND_HOST` | `127.0.0.1` | Interface the server binds. |
| `APOLLO_APPLE_RELOCATION_VERIFIED` | false | Gates Music.app location updates. |
| `APOLLO_JOB_HISTORY_LIMIT` | 500 | Finished jobs kept; older rows are pruned. |

`APOLLO_JOBS_AUTOSTART` is gone: leftover work waits for Resume instead
([ADR-0007](../adr/ADR-0007.md)). Values that change at run time live in the
`setting` table and are read through `PATCH /v1/settings`. The settings class
also writes the generated beets configuration
([Data](data.md#beets-configuration)).

## Errors

Every `ApolloError` subclass carries a class-level `code` and `status_code`,
which `register_hierarchy` requires. The registry is built after all error
modules import. See [API](api.md#problems).
