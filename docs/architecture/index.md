# Architecture

These pages describe the design that E1–E4 build, and become the description of
current behaviour as those epics close.

apollo is a local-first, single-user music workstation
([ADR-0001](../adr/ADR-0001.md)). A browser single-page app (Angular) calls a
FastAPI service under `/v1`. Routes validate input and call one workflow or
submit one job. Workflows plan, audit and apply every change. They reach the tag
index through one beets actor thread, `apollo.db` through one async engine, the
audio files through the media layer, and external tools (ffmpeg, ffprobe,
yt-dlp, osascript) through subprocesses. Long operations run as durable jobs in
the same process, and one server-sent event stream carries their progress and
the app status back to the browser.

```text
browser SPA ──HTTP /v1──▶ routes ──▶ workflows ──▶ beets actor ──▶ library.db
     ▲                       │            │──────▶ apollo.db (async SQLAlchemy)
     │                       ▼            │──────▶ media: audio files, trash, inbox
     └──── /v1/events ◀── job worker      └──────▶ ffmpeg, ffprobe, yt-dlp, osascript
```

| Page | Built by | Describes |
| -- | -- | -- |
| [Backend](backend.md) | E1 | The seven layers, app composition, lifespan order, settings and the pykit pieces under `platform`. |
| [Actor and caches](actor-and-caches.md) | E1 | The beets actor rules, the three-phase pattern, snapshot caches and paging into beets SQL. |
| [Jobs and events](jobs-and-events.md) | E1 | Job states, the worker, restart recovery, job types, the event stream and invalidation. |
| [Data](data.md) | E1 | `library.db` and `apollo.db`, the baseline tables, cache rules and the `.apollo/` tree. |
| [API](api.md) | E1 | The `/v1` surface by area, problems, paging, status and the generated client. |
| [Frontend](frontend.md) | E2, E3, E4 | The four layers, ngkit pieces, shared domain components, state, theming and routes. |

The decisions behind these pages are in the [decision log](../adr/index.md).
