# Decisions

Durable choices that constrain how apollo is built. Each record opens with the
decision, what follows from it, and what it influences; alternatives and history
are at the bottom. ADR-0010 to ADR-0018 restate decisions of the old apollo
(`rn_backup/apollo`, retired 2026-11-15) for this rebuild. Scope and work belong
in [specs](../specs/index.md).

| # | Decision | Scope |
| -- | -- | -- |
| [0001](ADR-0001.md) | apollo is a local-first, single-user music workstation over files apollo does not own | what apollo is, and the rules every feature must keep |
| [0002](ADR-0002.md) | Rebuilt fresh on kiln: backend ported onto current pykit, frontend rewritten in Angular | how the old apollo's code and contracts carry into this repository |
| [0003](ADR-0003.md) | Generic UI primitives are built and released in ngkit before apollo uses them | where apollo's frontend components live |
| [0004](ADR-0004.md) | One domain component per concept; screens differ by configuration, never by copy | apollo's frontend domain components and every screen that uses them |
| [0005](ADR-0005.md) | One actor thread owns beets; blocking work runs off the event loop and off the actor | every access to beets' `Library`, and where blocking work runs |
| [0006](ADR-0006.md) | Full-library reads are served from actor-built snapshots, discarded on mutation | any read that walks the whole beets index |
| [0007](ADR-0007.md) | Durable jobs run in-process from apollo.db, with no broker; leftover work waits for the user | every long-running operation |
| [0008](ADR-0008.md) | One server-sent event stream carries live state, re-derived from the database, with no replay | how the UI learns of job progress and app status |
| [0009](ADR-0009.md) | Every mutation is dry-run first, audited before it acts, reversible, and pruned only with its backups | every operation that changes a file, the index, a playlist or Music.app |
| [0010](ADR-0010.md) | Annotations hold only facts no audio frame can carry | what `apollo.db` may store about artists and albums, and how it is keyed |
| [0011](ADR-0011.md) | Artwork is served by endpoint and never inlined in lists | how cover art reaches the UI |
| [0012](ADR-0012.md) | Bulk edit keeps three states end to end and compiles to the operations list | bulk tag edit semantics in the UI and API |
| [0013](ADR-0013.md) | The track projection is pure and file facts are scan-time attributes | how the track DTO is built and where its file facts come from |
| [0014](ADR-0014.md) | Path agreement uses beets' own destination, and tag writes relocate in the same audited batch | path comparison, "update tag from path", and what a path-affecting tag edit does |
| [0015](ADR-0015.md) | Saved queries are transient: in the URL, or promoted to a playlist | where a query may be stored |
| [0016](ADR-0016.md) | Beets' plural tag vocabulary is the public vocabulary | field names in the API, the UI and URLs |
| [0017](ADR-0017.md) | Apple Music is a one-way XML import and a separate one-way export, and inbox promotion imports into Music.app | every exchange between apollo and Music.app |
| [0018](ADR-0018.md) | Inbox media is identified by path, not a fabricated id | how staged inbox files are referenced before promotion |
| [0019](ADR-0019.md) | Code is layered one way, back end and front end, and the layering is enforced by lint | imports inside `apps/api` and `apps/web` |
| [0020](ADR-0020.md) | The API is the rn-forge web standard at `/v1`, and the client is generated | the HTTP contract between `apps/api` and `apps/web` |
| [0021](ADR-0021.md) | apollo.db is async on rn-forge-sqlalchemy, from one fresh baseline migration | `apollo.db`: its engine, sessions, models and migrations |

<!-- BEGIN rn-forge kiln -->

## kiln's architecture baseline

kiln's canon decides part of this repository's product design, in
[kiln's architecture baseline](kiln/index.md). A decision here that departs from
one of those records names it, and says which part it supersedes.

<!-- END rn-forge kiln -->
