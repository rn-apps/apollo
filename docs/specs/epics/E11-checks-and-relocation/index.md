# E11 — Checks and relocation

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F11.1 — Track checks cache](F11.1-track-checks-cache.md) | New | — | — |
| [F11.2 — Errors page](F11.2-errors-page.md) | New | — | — |
| [F11.3 — Recheck](F11.3-recheck.md) | New | — | — |
| [F11.4 — Update tags from path](F11.4-update-tags-from-path.md) | New | — | — |
| [F11.5 — Relocate plan and apply](F11.5-relocate-plan-apply.md) | New | — | — |

<!-- END derived features -->

Finding library tracks whose tags or paths break the rules, and fixing them: the
track checks cache, the errors page, recheck, updating tags from the path and
relocating files to the templated path. At parity with old apollo. Relocation
follows the path and relocation rules of [ADR-0014](../../../adr/ADR-0014.md)
and is always planned, previewed and then applied.

Builds on: [E1](../E1-backend-foundation/index.md),
[E4](../E4-shared-domain-components/index.md),
[ADR-0007](../../../adr/ADR-0007.md), [ADR-0009](../../../adr/ADR-0009.md),
[ADR-0014](../../../adr/ADR-0014.md), [ADR-0017](../../../adr/ADR-0017.md),
[ADR-0020](../../../adr/ADR-0020.md).
