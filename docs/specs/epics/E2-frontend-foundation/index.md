# E2 — Frontend foundation

|  |  |
| -- | -- |
| **State** | Active |
| **Start Date** | 2026-11-18 |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F2.1 — Web dependencies on current ngkit](F2.1-web-dependencies.md) | Closed | release-1 | 1 Closed |
| [F2.2 — Generated API client](F2.2-generated-client.md) | New | — | 2 New |
| [F2.3 — Live state: event stream, status store and invalidation](F2.3-live-state.md) | New | — | 2 New |
| [F2.4 — apollo theme over ngkit tokens](F2.4-theme.md) | Active | release-1 | 1 Active |
| [F2.5 — Shell, navigation, routes and URL state](F2.5-shell-and-routes.md) | New | — | 4 New |
| [F2.6 — Frontend layering lint](F2.6-frontend-guardrails.md) | New | — | 1 New |
| [F2.7 — Branded home with a live API check](F2.7-connected-home.md) | New | release-1 | 1 New |

<!-- END derived features -->

The Angular app every screen stands on: ngkit pinned at a current release, a
client generated from the API, live state from the one event stream, apollo's
theme over ngkit's tokens, the shell (navigation rail, bottom bar, breadcrumbs,
command palette), routes, URL state, and the layering lint. It is a rewrite, not
a port ([ADR-0002](../../../adr/ADR-0002.md)). The old SvelteKit shell and
`routes/` are its requirements.

The first checkpoint is the [connected home](F2.7-connected-home.md), using the
ngkit theme and the scaffold API. The
[foundation sequence](../../index.md#foundation-sequence) shows when the
generated client, live state and navigation shell follow.

When E2 closes, `task web:dev` shows the shell with the branded home and a
placeholder page for every other route. The bottom bar reflects job and status
frames from a running API, and `task validate` is green.

Decisions: [ADR-0003](../../../adr/ADR-0003.md) ngkit first,
[ADR-0004](../../../adr/ADR-0004.md) one component per concept,
[ADR-0008](../../../adr/ADR-0008.md) events,
[ADR-0019](../../../adr/ADR-0019.md) layering,
[ADR-0020](../../../adr/ADR-0020.md) API. Shape:
[frontend architecture](../../../architecture/frontend.md).

## Conventions for every E2 story

- Specs (Vitest) are written first, beside the code, named `<file>.spec.ts`,
  with test titles prefixed by the story ID (`S2.3.1: …`).
- A story that needs a primitive ngkit has not released stops, and the primitive
  is added to [E3](../E3-ngkit-primitives/index.md)
  ([ADR-0003](../../../adr/ADR-0003.md)).
- Components are standalone and `OnPush`, with signal inputs.
