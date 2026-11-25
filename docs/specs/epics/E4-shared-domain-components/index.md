# E4 — Shared domain components

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F4.1 — Media editor side panel](F4.1-media-editor.md) | New | — | 4 New |
| [F4.2 — Track workspace](F4.2-track-workspace.md) | New | — | 2 New |
| [F4.3 — Dry-run flow](F4.3-dry-run-flow.md) | New | — | 2 New |
| [F4.4 — Job progress](F4.4-job-progress.md) | New | — | 1 New |
| [F4.5 — Artwork picker](F4.5-artwork-picker.md) | New | — | 1 New |
| [F4.6 — Facet view](F4.6-facet-view.md) | New | — | 1 New |
| [F4.7 — Bulk edit panel](F4.7-bulk-edit-panel.md) | New | — | 1 New |
| [F4.8 — Formatting](F4.8-formatting.md) | New | — | 1 New |

<!-- END derived features -->

apollo's one component per music concept ([ADR-0004](../../../adr/ADR-0004.md)):

- the media editor side panel;
- the track workspace;
- the dry-run flow;
- job progress;
- the artwork picker;
- the facet view;
- the bulk edit panel;
- shared formatting.

They are built before any screen. Each screen epic (E5–E14) only configures
them, and a screen story that finds one lacking extends it here; it never forks
it.

**How they are built without the screens' endpoints.** Each component talks to
the API only through an adapter interface, defined here. Its specs run against
an in-memory fake adapter (`domain/testing/`). The real adapters are written by
the epic that ships the endpoints. For example, the track media adapter is
[E6](../E6-tag-editing/index.md)'s, the inbox one
[E8](../E8-inbox-and-intake/index.md)'s. So E4 depends on E2 and E3 only.

Decisions: [ADR-0004](../../../adr/ADR-0004.md),
[ADR-0009](../../../adr/ADR-0009.md) dry run,
[ADR-0012](../../../adr/ADR-0012.md) bulk states,
[ADR-0018](../../../adr/ADR-0018.md) inbox targets. Shape:
[frontend architecture](../../../architecture/frontend.md).

## Conventions for every E4 story

- Code lives in `apps/web/src/app/domain/<component>/`. Specs are written first,
  titled with the story ID, and run against the fake adapter.
- Only E3 primitives are used for generic UI. No local stand-ins.
- Every operation a target lacks is rendered disabled, with the adapter's reason
  as a tooltip and an accessible description.

## Open questions

- **Inspector or editor.** The old app had both a persistent right inspector
  (read-only, on the workspace) and the editor drawer. The proposal is to keep
  only the media editor, opened by row activation and by `?item=` in the URL,
  with no separate inspector. That is one fewer surface, and it blocks F4.2.
