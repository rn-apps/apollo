# Release 1 — Connected home

|  |  |
| -- | -- |
| **Status** | in progress |
| **Start Date** | 2026-11-18 |

The first local checkpoint is a themed Apollo home with a logo and a live
connection to the scaffold API.

## Entry criteria

- The checkout has Angular and FastAPI dev tasks and the API liveness route.

## Scope

<!-- BEGIN derived scope -->

| Feature | Epic | State |
| -- | -- | -- |
| [F2.1 — Web dependencies on current ngkit](../../specs/epics/E2-frontend-foundation/F2.1-web-dependencies.md) | E2 | Closed |
| [F2.4 — apollo theme over ngkit tokens](../../specs/epics/E2-frontend-foundation/F2.4-theme.md) | E2 | Active |
| [F2.7 — Branded home with a live API check](../../specs/epics/E2-frontend-foundation/F2.7-connected-home.md) | E2 | Closed |

<!-- END derived scope -->

## Decisions

None yet. The theme and health check follow [ADR-0003](../../adr/ADR-0003.md)
and [ADR-0020](../../adr/ADR-0020.md).

## Breaking changes

None.

## Progress

The ngkit dependency and token smoke test is closed. Verify the theme next, then
walk through connection and recovery in the browser with the owner. The
[foundation sequence](../../specs/index.md#foundation-sequence) picks up the
backend runtime after this checkpoint.

## Commits

```sh
git log --oneline -E --grep='[FS]2\.(1|4|7)(\.|[^0-9]|$)'
```

## Exit criteria

- All scoped stories meet their acceptance and `task validate` passes.
- The owner reviews the rendered theme and verifies the live API connection, the
  unavailable state and recovery through Retry.
