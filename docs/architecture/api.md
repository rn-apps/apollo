# API

Built by: E1

The API is `rn_forge.fastapi.FastApiApp` at `/v1`, served on `127.0.0.1` with no
auth and no CORS ([ADR-0020](../adr/ADR-0020.md)). The browser reaches it
same-origin through the dev proxy. The interactive schema is at `/openapi.json`.

## Surface

Paths are relative to `/v1`. Deprecated routes of the old app (`/searches*`,
`/playlists/from-search`, `/apple/import-playlist`) are not ported
([ADR-0015](../adr/ADR-0015.md)). Every mutating route accepts `dry_run`
([ADR-0009](../adr/ADR-0009.md)).

| Area | Routes |
| -- | -- |
| Tracks | `GET /tracks`, `GET /tracks/{id}`, `GET /tracks/{id}/audio`, `PATCH /tracks/{id}`, `POST /tracks/bulk-edit`, `POST /tracks/common-tags`, `POST /tracks/{id}/clean-tags`, `GET /tracks/{id}/check` |
| Albums, facets | `GET /albums`, `GET /albums/{id}/tracks`, `GET /fields`, `GET /facets/{field}` |
| Artwork | `GET`, `PUT`, `DELETE /tracks/{id}/artwork`; `PUT /albums/{id}/artwork`; `GET`, `PUT`, `DELETE /inbox/artwork` |
| Annotations | `GET`, `POST /annotations/artists/{name}`; `GET`, `POST /annotations/albums/{key}`; `GET /annotations/orphans`; `POST /annotations/relink`; `DELETE /annotations/{kind}/{key}` |
| Inbox, intake | `GET`, `DELETE /inbox`; `GET /inbox/audio`; `GET /inbox/probe`; `GET /inbox/{path}/check`; `POST /inbox/edit`, `/inbox/clean-tags`, `/inbox/common-tags`, `/inbox/bulk-edit`, `/inbox/promote`, `/inbox/trim`; `POST /intake/onboard` |
| Proposals | `POST /proposals`, `POST /proposals/accept` |
| Trim, replace | `POST /tracks/{id}/trim`, `POST /tracks/{id}/replace` |
| Relocate | `POST /relocate/plan`, `POST /relocate/apply` |
| Checks | `GET /errors`, `GET /errors/summary`, `POST /errors/recheck` |
| Jobs | `POST /jobs`, `GET /jobs`, `GET /jobs/{id}`, `POST /jobs/{id}/cancel`, `GET`, `POST /jobs/worker` |
| Events | `GET /events` ([Jobs and events](jobs-and-events.md#the-event-stream)) |
| Playlists | `GET`, `POST /playlists`; `GET`, `PATCH`, `DELETE /playlists/{id}`; `POST /playlists/{id}/export` |
| Apple Music | `GET /apple/status`, `GET /apple/stats`, `GET /apple/reconcile`, `POST /apple/import-stats`, `POST /apple/import-playlists`, `POST /apple/push-playlist` |
| Audit and maintenance | `GET /audit`, `GET /audit/batches`, `POST /audit/batches/{id}/undo`; `GET /maintenance`, `GET /maintenance/config`, `GET /maintenance/logs/{name}`, `POST /maintenance/caches/rebuild`; prune history and empty trash (new) |
| System | `GET /status`, `POST /status/refresh`, `GET /dashboard`, `GET`, `PATCH /settings` |

The kit adds `GET /livez` and `GET /readyz` at the root, outside `/v1`.
`/health` and the `/api/v1` prefix are gone. Status refresh is
`POST /status/refresh` (F1.7); the prune and empty-trash routes are E14's.

Long operations return 202 with `jobId` and run as jobs. Synchronous exceptions
are the inbox path-backed bulk edits ([ADR-0018](../adr/ADR-0018.md)) and
single-item tag edits.

## Problems

Errors are RFC 9457 `application/problem+json`. `ApolloError` subclasses carry a
stable hyphenated `code` and a `status_code`, and are registered with
`register_hierarchy`.

| Field | Content |
| -- | -- |
| `type` | `/problems/<code>` |
| `title`, `status`, `detail` | from the registry and the exception |
| extensions | the error's structured detail, for example the refusal reason of a relocation |
| `traceId` | the kit's trace id, in place of the old `X-Request-ID` |

The hierarchy is the 15 old subclasses, codes hyphenated, plus `plan-stale`
(new): `not-found`, `conflict`, `file-missing`, `write-failed`, `validation`,
`artwork-fetch`, `artwork-invalid-image`, `job-failed`, `icloud-sync-active`,
`invalid-source`, `inbox-preview-stale`, `trim-range`, `trim-result-too-short`,
`capability-unavailable`, `invalid-query`, `plan-stale`. Every class sets `code`
and `status_code`. Request validation failures map to the kit's validation
problem with field errors. An unhandled exception is a 500 problem with no
detail, and 5xx responses are logged with their traceback through
`log_server_errors`.

Content-check failures (missing tags, path and tag disagreement, unreadable
stream, missing file) are data in `track_check`, not exceptions. The client
matches on `type` through ngkit's problem helpers.

## Paging

| List | Source | Paging |
| -- | -- | -- |
| Tracks, albums, inbox | beets | offset, response carries `total` |
| Jobs, audit, playlists | `apollo.db` | the kit's cursor pagination |

Offset paging exists because the virtual grid needs the full height to scroll
and seek ([ADR-0020](../adr/ADR-0020.md)). The kit's `keyset` serves SQLAlchemy
selects only. This is apollo's one departure from the kit's API rules. Offset
responses follow the API's casing rule like every body: camelCase on the wire,
snake_case in Python, through `rn_forge.web.WireModel`. Beets fields are
camelCased too, for example `mb_artistid` is `mbArtistid` (pykit rule
`casing.response-bodies-are-camel-case`).

## Artwork

Art is served by `GET /tracks/{id}/artwork` with a content type, a strong `ETag`
and thumbnails, and is never inlined in a list. The track DTO carries
`hasArtwork` as `bool | None`. `GET /tracks/{id}?artwork=true` is the one opt-in
for inline bytes ([ADR-0011](../adr/ADR-0011.md)).

## Status

`GET /v1/status` returns the app version, tool versions (ffmpeg, ffprobe,
yt-dlp, osascript), capabilities, worker state, error counts and track counts. A
capability the host lacks, such as trim without ffmpeg or artwork-by-URL while
iCloud Sync Library is active, is reported there with its reason, and the UI
shows the operation disabled with that reason. The same status frame travels on
`/v1/events`.

## Body limit and tracing

The kit's 1 MiB body limit is raised to 25 MiB for artwork uploads. Security
headers stay on. Tracing is the kit's: `traceId` in problems, with no custom
request-id middleware.

## Generated client

TypeScript types are generated from `/openapi.json` by a repo task, committed
under `apps/web`, and never hand-edited. A test fails if the committed types are
stale. The generator is a dev dependency, since pykit has no codegen extra.
Operation ids are deterministic from the kit, which keeps the generated names
stable.
