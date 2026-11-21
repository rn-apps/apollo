# E15 — Acceptance and cutover

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F15.1 — Acceptance gates on a copy](F15.1-gates-on-a-copy.md) | New | — | — |
| [F15.2 — Gates on the real library](F15.2-gates-on-the-real-library.md) | New | — | — |
| [F15.3 — Daily use and retiring the old repo](F15.3-daily-use-and-retire.md) | New | — | — |

<!-- END derived features -->

Proving the rebuild before it touches the real library: the acceptance gates of
old apollo (12k tracks at 60 fps, path fidelity, `library_mutation` tests) run
against a copy, then against the real library, then daily use and the retirement
of the old repo. An installer (`lifecycle = true`) is out of scope here and
parked as an idea.

Builds on: [E1](../E1-backend-foundation/index.md),
[E2](../E2-frontend-foundation/index.md),
[E4](../E4-shared-domain-components/index.md), every epic from
[E5](../E5-library-browse/index.md) to
[E14](../E14-audit-and-maintenance/index.md),
[ADR-0001](../../../adr/ADR-0001.md), [ADR-0014](../../../adr/ADR-0014.md).
