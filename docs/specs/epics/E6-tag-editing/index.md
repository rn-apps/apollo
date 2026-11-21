# E6 — Tag editing

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F6.1 — Single track edit](F6.1-single-track-edit.md) | New | — | — |
| [F6.2 — Bulk edit](F6.2-bulk-edit.md) | New | — | — |
| [F6.3 — Common tags](F6.3-common-tags.md) | New | — | — |
| [F6.4 — Clean tags](F6.4-clean-tags.md) | New | — | — |
| [F6.5 — Identity editor](F6.5-identity-editor.md) | New | — | — |
| [F6.6 — Album edit](F6.6-album-edit.md) | New | — | — |

<!-- END derived features -->

Editing tags on library tracks at parity with old apollo: single edit, bulk
edit, common tags, clean tags, the artist identity editor (main and featured)
and, new in the rebuild, album-level edit, which was only a stub in the old app.
Every edit goes through the one E4 media editor and bulk edit panel, writes tags
atomically and records an audit entry.

Builds on: [E1](../E1-backend-foundation/index.md),
[E4](../E4-shared-domain-components/index.md),
[ADR-0004](../../../adr/ADR-0004.md), [ADR-0009](../../../adr/ADR-0009.md),
[ADR-0010](../../../adr/ADR-0010.md), [ADR-0012](../../../adr/ADR-0012.md),
[ADR-0016](../../../adr/ADR-0016.md), [ADR-0020](../../../adr/ADR-0020.md).
