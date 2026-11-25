# Actor and caches

Built by: E1

beets' `Library` and its SQLite index are not safe for concurrent use. apollo
serialises all access through one thread, and keeps reads that walk the whole
index off the request path ([ADR-0005](../adr/ADR-0005.md),
[ADR-0006](../adr/ADR-0006.md)).

## The actor

The library actor is a `ThreadActor[Library]` from commons, in `index/actor.py`.
apollo adds only the beets setup: the factory that builds the `Library` from the
generated configuration ([Data](data.md#beets-configuration)) and the custom
fields.

| Caller | Call | Waits on |
| -- | -- | -- |
| Async route or workflow | `await actor.run(fn)` | the event loop, not a thread |
| Job handler (sync code in a worker thread) | `actor.submit(fn)` | the returned `Future` |

Rules:

- Only code running inside `fn` touches a `Library`, `Item` or `Album`.
- No beets object leaves the actor. `fn` returns plain data or a DTO. Tests pin
  this for the actor's public calls.
- The actor is held only for beets work. A slow call delays every other read.
- Nothing blocks the event loop. File, tag, image and subprocess work in a
  request path goes through `asyncio.to_thread`.

## The three-phase pattern

An operation that needs files, a subprocess or the network splits into three
phases:

1. On the actor, read or write the beets index.
1. On the actor, project the result into plain data, for example
   `[(id, path, mtime)]`.
1. Off the actor, do the file or network work as a fan-out with
   `TaskPool.map_settled`. Results that must be stored go back to the actor in
   one hop.

The scan is the reference. Phase 1 reconciles the index with the files. Phase 2
projects `(id, path, mtime)` for every item and each path's expected destination
from `Item.destination()` ([ADR-0014](../adr/ADR-0014.md)). Phase 3 runs the tag
check and `ffprobe` per file, then writes `track_check` rows in batches of 500
and the scan-time attributes (`apollo_filesize`, `apollo_file_missing`,
`apollo_has_art`) back through the actor in chunks
([ADR-0013](../adr/ADR-0013.md)). `map_settled` returns a success or failure per
item, so one bad file does not stop the batch.

The track DTO is built on the actor in one code path (`index/dto.py`) and makes
no filesystem calls. A guard test patches `Path.stat`, `exists` and `open` to
raise and builds the DTO against them.

## Snapshots

A read that needs the whole index is built once, on the actor, and served from
memory until a mutation discards it.

| Snapshot | Serves | Module |
| -- | -- | -- |
| Albums | album summaries with their member index | `index/cache` |
| Facets | counted values for artists, genres, composers and the other facet fields | `index/facets` |
| Stats | library statistics for home and status | `index/stats` |

One generic snapshot type holds the value. A rebuild is lazy: the first reader
after invalidation triggers it, and readers that arrive during the rebuild share
it, so there is one rebuild per wave. A snapshot is never persisted and is never
a second source of truth.

Invalidation happens in two places: when a job whose type declares that it
mutates the library reaches a terminal state, and on the single-item paths that
write tags (edit, proposal accept, promotion). A job type that declares this
wrongly leaves stale data until the next mutation.

Numbers from the old app on the 12,335-track library:

| Read | Cold | Warm |
| -- | -- | -- |
| Album summaries | 1.85 s (2.45 s before the pure projection) | 1 ms |
| Whole-index walk (facets, stats) | about 2.6 s | served from memory |
| `list(lib.items())` in a request path | 793 ms at 12k tracks | not applicable |
| Track list page | 29 ms | not applicable |

## Paging into beets SQL

beets has no `LIMIT` or `OFFSET`. `index/paging.fetch_page` reuses beets' query
parser to build the `WHERE` clause and adds `ORDER BY`, `LIMIT` and `OFFSET`. It
returns the page and the total match count. A page costs about 18 ms, against
about 900 ms through beets' own iteration.

`fetch_page` declines, and returns nothing so the caller falls back to beets
iteration, in three cases:

- The query or sort touches a flexible attribute (`apollo_*`).
- The sort has no usable SQL column.
- The query needs an album join.

A test pins equivalence between `fetch_page` and `Library.items()` for the same
queries. The fallback path is correct but slower, and a snapshot or a stored
scan-time attribute is the way to avoid it for a hot query.

The tracks, albums and inbox lists carry the offset inside their page token
([API](api.md#paging)). A write between two requests can shift such a list by a
row, and the client refetches after a mutation.
