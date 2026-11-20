# E1 — Backend foundation

|  |  |
| -- | -- |
| **State** | Active |
| **Start Date** | 2026-11-19 |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F1.1 — Dependencies, entry point and CI tools](F1.1-dependencies-and-entry.md) | Active | release-1 | 1 Active · 2 New · 1 Closed |
| [F1.2 — Settings, runtime paths and logging](F1.2-settings-and-runtime.md) | New | release-1 | 2 New |
| [F1.3 — Errors, paging and the API contract](F1.3-api-contract.md) | New | release-1 | 2 New |
| [F1.4 — apollo.db](F1.4-apollo-db.md) | New | — | 2 New |
| [F1.5 — The beets actor, projections, paging and snapshots](F1.5-beets-actor.md) | New | — | 4 New |
| [F1.6 — Job runtime and event stream](F1.6-jobs-and-events.md) | New | — | 4 New |
| [F1.7 — Status, tools and capabilities](F1.7-status-and-capabilities.md) | New | — | 2 New |
| [F1.8 — Audit, trash and undo core](F1.8-audit-and-trash.md) | New | — | 2 New |
| [F1.9 — Test harness and layering guardrails](F1.9-harness-and-guardrails.md) | New | release-1 | 2 New |

<!-- END derived features -->

The platform every backend feature stands on: dependencies on the current pykit
releases, settings and runtime paths, the problem-based API contract,
`apollo.db` on the async engine, the beets actor and its snapshots, the job
runtime and the event stream, status and capabilities, the audit and trash core,
and the test harness and layering guardrails. It ports the old apollo's generic
infrastructure onto pykit ([ADR-0002](../../../adr/ADR-0002.md)) and holds no
screen.

Start F1.1 after the
[connected home](../E2-frontend-foundation/F2.7-connected-home.md) has been
reviewed. The [foundation sequence](../../index.md#foundation-sequence) breaks
E1 into checkpoints for runtime, fixture data, jobs and reversible writes.

When E1 closes, `task validate` is green, `task api:dev` serves `/v1/status` and
`/v1/events`, a scan job of a generated fixture library runs end to end, and an
audited tag write can be undone. These are what every feature epic (E5–E14)
needs.

Decisions: [ADR-0005](../../../adr/ADR-0005.md) actor,
[ADR-0006](../../../adr/ADR-0006.md) snapshots,
[ADR-0007](../../../adr/ADR-0007.md) jobs, [ADR-0008](../../../adr/ADR-0008.md)
events, [ADR-0009](../../../adr/ADR-0009.md) audit,
[ADR-0019](../../../adr/ADR-0019.md) layering,
[ADR-0020](../../../adr/ADR-0020.md) API, [ADR-0021](../../../adr/ADR-0021.md)
database. Shape: [backend architecture](../../../architecture/backend.md).

## Conventions for every E1 story

- Tests are written first. They live in `apps/api/tests/` and are named
  `test_s<epic>_<feature>_<story>_<n>_<slug>`, as in
  `test_s1_4_1_1_engine_uses_wal`.
- Each story names the old module it ports from, under
  `rn_backup/apollo/apps/api/src/apollo/`. It ports behaviour, not file
  layout.
- `task validate` passes when the story closes.
- No file kiln generated is edited. Config changes go through
  `.rn-forge/kiln/config.toml` and `task kiln:apply`.

## Open questions

- **JSON field casing.** Should response bodies use snake_case, matching beets
  field names (`albumartist`, `mb_artistid`), or camelCase, matching the kit's
  query parameters (`pageSize`, `pageToken`)? The recommendation is snake_case
  for bodies and the kit's names for paging parameters. It blocks F1.3.
