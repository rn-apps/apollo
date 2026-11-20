# Release 1 — Connected home and backend runtime

|  |  |
| -- | -- |
| **Status** | in progress |
| **Start Date** | 2026-11-18 |

Two local checkpoints: a themed Apollo home with a logo and a live connection to
the scaffold API, then the backend runtime (dependencies, settings, the API
contract and the test harness).

## Entry criteria

- The checkout has Angular and FastAPI dev tasks and the API liveness route.

## Scope

<!-- BEGIN derived scope -->

| Feature | Epic | State |
| -- | -- | -- |
| [F1.1 — Dependencies, entry point and CI tools](../../specs/epics/E1-backend-foundation/F1.1-dependencies-and-entry.md) | E1 | New |
| [F1.2 — Settings, runtime paths and logging](../../specs/epics/E1-backend-foundation/F1.2-settings-and-runtime.md) | E1 | New |
| [F1.3 — Errors, paging and the API contract](../../specs/epics/E1-backend-foundation/F1.3-api-contract.md) | E1 | New |
| [F1.9 — Test harness and layering guardrails](../../specs/epics/E1-backend-foundation/F1.9-harness-and-guardrails.md) | E1 | New |
| [F2.1 — Web dependencies on current ngkit](../../specs/epics/E2-frontend-foundation/F2.1-web-dependencies.md) | E2 | Closed |
| [F2.4 — apollo theme over ngkit tokens](../../specs/epics/E2-frontend-foundation/F2.4-theme.md) | E2 | Closed |
| [F2.7 — Branded home with a live API check](../../specs/epics/E2-frontend-foundation/F2.7-connected-home.md) | E2 | Closed |

<!-- END derived scope -->

## Decisions

None yet. The theme and health check follow [ADR-0003](../../adr/ADR-0003.md)
and [ADR-0020](../../adr/ADR-0020.md).

## Breaking changes

None.

## Progress

The connected home is closed: the owner walked through connection and recovery
in the browser on 2026-11-19, and the palette check moved to F2.5. The backend
runtime follows the
[foundation sequence](../../specs/index.md#foundation-sequence): F1.1, F1.2,
F1.3, then F1.9. Settle JSON field casing before F1.3.

## Commits

```sh
git log --oneline -E --grep='([FS]2\.(1|4|7)|[FS]1\.(1|2|3|9))(\.|[^0-9]|$)'
```

## Exit criteria

- All scoped stories meet their acceptance and `task validate` passes.
- The owner verifies the live API connection, the unavailable state and recovery
  through Retry.
- The owner starts the API against a temporary state directory and inspects its
  runtime tree, log and problem responses.
