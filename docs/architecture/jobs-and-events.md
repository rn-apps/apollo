# Jobs and events

Built by: E1

Every long-running operation is a durable job: a row in `apollo.db`, claimed and
run by an in-process worker, with progress delivered over one event stream
([ADR-0007](../adr/ADR-0007.md), [ADR-0008](../adr/ADR-0008.md)). There is no
broker.

## States

```text
pending ──claim──▶ running ──▶ succeeded
   │                  ├──────▶ failed
   └──cancel──▶ cancelled ◀───┘ (cooperative)
```

`JobState` is stored as `VARCHAR`. A job is `running` only once a worker thread
holds it, never while queued in an executor.

## The worker

`platform/jobs` holds the worker, written on the async engine in the shape of
pykit's sketched queue: `Job` and `JobLog` models, an async claim loop and a
handler that receives a job context.

- **Claiming** is bounded by capacity: `max_workers - inflight`. `POST /v1/jobs`
  calls `worker.notify()`, so a submitted job starts at once. Otherwise the
  poller wakes every 2 s.
- **Context.** A handler receives `JobContext` with `progress`, `log`,
  `checkpoint` and `cancelled`. Progress and log lines are written to `job`
  and `job_log` as the job runs.
- **Cancellation** is cooperative. `POST /v1/jobs/{id}/cancel` sets a flag.
  `checkpoint()` reads it at most twice a second and raises `JobCancelled`.
- **Blocking work.** A handler runs its blocking work through the actor or
  `asyncio.to_thread`. Its database writes stay on the loop
  ([ADR-0021](../adr/ADR-0021.md)). Fan-out inside a handler uses
  `TaskPool.map_settled`, never the job runtime.
- **Shutdown** waits for running handlers for a bounded grace, then stops.
- **Pruning.** Finished jobs beyond `APOLLO_JOB_HISTORY_LIMIT` (500) are deleted
  with their logs.
- **Pause.** `POST /v1/jobs/worker` pauses or resumes claiming.

## Restart recovery

At startup the worker inspects jobs left by the previous run:

| Found | Becomes |
| -- | -- |
| `running` | `failed`, "interrupted by restart" |
| `pending` | held: not claimed |

Held jobs run only after an explicit Resume in the UI. A job submitted after
startup runs at once. No job silently re-runs on a reload.

## Job types

`JobType` is stored as `VARCHAR`, so a new type needs no migration. Each
declares whether it mutates the library, which decides snapshot invalidation
([Actor and caches](actor-and-caches.md#snapshots)).

| Type | Handler module | Mutates library |
| -- | -- | -- |
| `scan` | `jobs/library` | yes |
| `check` | `jobs/library` | no (writes `track_check`) |
| `bulk_edit` | `jobs/edit` | yes |
| `relocate` | `jobs/edit` | yes |
| `trim` | `jobs/media` | yes |
| `replace` | `jobs/media` | yes |
| `download` | `jobs/media` | no (writes to inbox) |
| `artwork` | `jobs/media` | yes |
| `intake` | `jobs/media` | yes |
| `apple_sync` | `jobs/apple` | no (writes playlists) |
| `apple_stats` | `jobs/apple` | no (writes `apple_stat`) |

Adding a handler: add a `JobType`, write `handler(context) -> dict`, register it
in `app.py`, and set its mutation flag.

## The event stream

`GET /v1/events` is the only stream. It carries job frames and a status frame
(health, error counts, track counts, worker state). The shell opens it once and
never polls. `sse_response` supplies framing, a 15 s heartbeat, the retry hint
and a terminal `error` frame.

- Each 500 ms tick re-reads job state from `apollo.db` and emits what changed.
- On connect, every non-terminal job is emitted. Terminal jobs are seeded
  silently, so they set the baseline without a frame.
- There is no `Last-Event-ID` replay. A reconnect is told the current truth. The
  `id:` field is sent for ordering only.
- A tick costs one indexed query on `job`, plus a status read served from
  snapshots.

The client is ngkit's event stream, which keeps the browser's reconnect and
backs off only once the connection is `CLOSED`.

## Invalidation

A terminal job frame makes the client invalidate the resources that job type
affects, through ngkit's resource invalidation
([Frontend](frontend.md#state-ownership)). The mapping from job type to
resources lives in the client, in one table.

## Sequence: a bulk edit

1. The panel sends `POST /v1/tracks/bulk-edit` with `dry_run: true` and the
   operations list. The workflow resolves targets on the actor and returns
   each track's before, after, diff and any relocation, with source mtimes.
1. The user reviews the diff in the dry-run flow and confirms.
1. The panel sends the same request with `dry_run: false` and the reviewed
   mtimes. The route submits a `bulk_edit` job and returns 202 with `jobId`.
1. The worker claims the job. For each track the handler writes the audit entry
   first (one shared `batch_id`), then applies the tag write and any move on
   the actor ([ADR-0009](../adr/ADR-0009.md)). A track whose mtime changed
   since the dry run is refused. A failure on one track is recorded and the
   batch continues.
1. Progress frames arrive on `/v1/events` for each tick, and the job progress
   component shows them.
1. The job reaches `succeeded` or `failed`. The worker invalidates the
   snapshots, and the terminal frame makes the client refetch tracks, albums
   and facets.
1. Undo replays the batch newest first from History ([API](api.md#surface)).
