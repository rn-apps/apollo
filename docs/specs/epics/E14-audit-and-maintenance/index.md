# E14 — Audit and maintenance

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F14.1 — Audit log](F14.1-audit-log.md) | New | — | — |
| [F14.2 — Batch undo](F14.2-batch-undo.md) | New | — | — |
| [F14.3 — History page](F14.3-history-page.md) | New | — | — |
| [F14.4 — Maintenance page](F14.4-maintenance-page.md) | New | — | — |
| [F14.5 — Prune and empty trash](F14.5-prune-and-empty-trash.md) | New | — | — |

<!-- END derived features -->

The record of what apollo changed and the means to take it back: the audit log,
batch undo, the history page, the maintenance page (logs, config, cache
rebuild), and pruning of the audit log and the trash with an empty-trash action.
Prune and empty trash are new work, specified in old apollo (ADR-0021) but never
built. Follows [ADR-0009](../../../adr/ADR-0009.md) for dry-run, audit, undo and
prune.

Builds on: [E1](../E1-backend-foundation/index.md),
[E4](../E4-shared-domain-components/index.md),
[ADR-0007](../../../adr/ADR-0007.md), [ADR-0009](../../../adr/ADR-0009.md),
[ADR-0020](../../../adr/ADR-0020.md).
