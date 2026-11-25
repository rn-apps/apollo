# Frontend

Built by: E2, E3, E4

The frontend is an Angular single-page app in `apps/web/src/app`, rewritten from
the old SvelteKit app ([ADR-0002](../adr/ADR-0002.md)). It is a dense,
dark-first workstation: Angular, Tailwind v4 utilities in features, and generic
primitives from ngkit.

## Layers

A layer imports only from the layers above it in the table. A feature never
imports another feature. Lint enforces it in `apps/web/eslint.config.mjs`
([ADR-0019](../adr/ADR-0019.md)).

| Layer | Folder | Holds |
| -- | -- | -- |
| core | `core/` | API client and generated types, problem handling, the status store, the event stream, invalidation table, formatters |
| shell | `shell/` | rail, bottom bar, command palette, breadcrumbs, page header, one navigation model |
| domain | `domain/` | the shared components below, media target adapters |
| features | `features/<screen>/` | one folder per route; composes domain components with configuration |

## From ngkit

Primitives are built and released in ngkit before apollo uses them, at a pinned
release ([ADR-0003](../adr/ADR-0003.md)). apollo's `apps/web` holds only domain
components and the shell.

| Source | Used for |
| -- | -- |
| `@rn-forge/ng` | `problemOf`, `problemMessage`, `hasProblemType`; `createEventStream`; `Invalidation` with `httpResource`; core config; local storage service |
| `@rn-forge/ng-tailwind` | button, modal and drawer, confirm dialog, toolbar, chips input, autocomplete, field control, state block, badge, tabs, toast, progress bar, data grid; the `--rnf-*` tokens |
| `@angular/cdk` | behaviour under the primitives, and `cdk/scrolling` for the virtual grid |

A story that finds a missing primitive adds it to ngkit and waits for the
release. It does not build a local stand-in.

## Shared domain components

Each concept has one component. Screens vary it through inputs: a target
adapter, a column set, a capability set or row actions
([ADR-0004](../adr/ADR-0004.md)).

| Component | Concept |
| -- | -- |
| Media editor side panel | one item's tags, artwork, trim, replace, clean-up and checks |
| Track workspace | grid and selection toolbar, opening the media editor, for tracks or staged media (inspector: open question on E4) |
| Dry-run flow | preview, diff, confirm, apply, for every mutation |
| Bulk edit panel | many items' tags, with three states per field ([ADR-0012](../adr/ADR-0012.md)) |
| Job progress | state and progress of a job |
| Artwork picker | file, URL or clear, for track, album and inbox |
| Facet view | counted values, as list or table |

The media editor addresses an item by a **media target**: `track:<id>` or
`inbox:<path>` ([ADR-0018](../adr/ADR-0018.md)). The target adapter says which
operations it supports. An operation a target lacks is shown disabled with its
reason. A capability the host lacks (see [API](api.md#status)) is disabled the
same way.

The track workspace takes a column set. The inbox column set is the same grid
with inbox columns and per-viewer column preferences. The bulk edit panel
compiles its form to the existing `operations` list, so it adds no mutation
path.

## State ownership

| State | Owner |
| -- | -- |
| Query, sort, selection detail, open item | the URL. A reload or Copy link reproduces it ([ADR-0015](../adr/ADR-0015.md)) |
| Health, error counts, active job, worker state | the status store, fed by `/v1/events` |
| Job frames | the event stream; terminal frames drive invalidation |
| Command palette actions, audio preview and queue | shell state |
| Server data | `httpResource`, invalidated on terminal job frames and after writes |

No screen polls. The shell opens the one stream. Breadcrumbs are a pure function
from URL to crumbs, and a crumb without an `href` is a grouping, never a link.

## Theming

One apollo theme file overrides the `--rnf-*` tokens for the dark workstation
palette. `src/styles.scss` declares
`@layer theme, base, rnf, components, utilities;`, then imports the ngkit tokens
and base, then the theme file. Features use Tailwind v4 utilities. No colour
literal appears outside the theme file. apollo never restyles a primitive's
internals.

The shell is responsive: a 208 px rail, a 66 px icon rail from 1100 to 820 px,
and a bottom tab bar below that.

## Routes

The Angular routes keep the paths of the old SvelteKit routes. Each is
lazy-loaded from `features/<screen>`.

| Path | Screen |
| -- | -- |
| `/` | Home: vitals, needs attention, recently added, distribution, activity |
| `/library` | Songs, with facet list |
| `/library/artists`, `/library/genres`, `/library/composers` | facet tables |
| `/library/artists/:name`, `/library/genres/:name`, `/library/composers/:name` | track workspace for one value |
| `/albums`, `/albums/:id` | album list and album tracks |
| `/albums/:id/edit` | album edit |
| `/searches` | search: a query box over the track workspace |
| `/playlists`, `/playlists/:id` | playlists, playlist detail |
| `/errors` | check findings with the media editor and relocate |
| `/inbox` | staged media, parse, promote and proposal review |
| `/jobs`, `/jobs/:id` | job list and detail |
| `/history` | audit batches and undo |
| `/apple` | Apple Music import, export and statistics |
| `/maintenance` | caches, logs, trash, prune |
| `/settings`, `/settings/annotations` | settings, orphan relink |

The old `/searches` stored-search CRUD is not ported; the route stays as a
search surface.

## Performance gate

The track grid renders fixed-height virtual rows with `cdk/scrolling`. The gate
is 12,000 rows at 60 fps, and acceptance measures it against a 12k-track
fixture. Row height is constant. The grid shows `totalSize` as the result count
and loads the next page by `nextPageToken` as the user nears the last loaded row
([API](api.md#paging)). It does not seek to a row that is not loaded. Artwork in
a row is a thumbnail request, never inline data.
