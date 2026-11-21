# Specs

What this repo is made of and what is left to build. **Start here:** the board
says what is next; the epic says how; its ADRs say why. The Releases and Backlog
sections below are derived from the epic, feature and release pages by
`task docs:generate`; never edit inside their fence.

## Foundation sequence

Build and validate one checkpoint at a time. At each checkpoint, run the
targeted checks, walk through the result with the owner on synthetic data where
needed, and review what the next checkpoint builds on before starting it. Only
the first checkpoint is assigned to a release.

| Checkpoint | Features in build order | What to verify before moving on |
| -- | -- | -- |
| 1. Connected home | [F2.1](epics/E2-frontend-foundation/F2.1-web-dependencies.md) → [F2.4](epics/E2-frontend-foundation/F2.4-theme.md) → [F2.7](epics/E2-frontend-foundation/F2.7-connected-home.md) | The branded home loads and Retry reconnects after an API restart. |
| 2. Backend runtime | [F1.1](epics/E1-backend-foundation/F1.1-dependencies-and-entry.md) → [F1.2](epics/E1-backend-foundation/F1.2-settings-and-runtime.md) → [F1.3](epics/E1-backend-foundation/F1.3-api-contract.md) → [F1.9](epics/E1-backend-foundation/F1.9-harness-and-guardrails.md) | Start the API against a temporary state directory and inspect its runtime tree, log and problem responses. |
| 3. Fixture library | [F1.4](epics/E1-backend-foundation/F1.4-apollo-db.md) → [F1.5](epics/E1-backend-foundation/F1.5-beets-actor.md) | Migrate an empty database and scan, query and page a generated library through the actor. |
| 4. Jobs and status | [F1.6](epics/E1-backend-foundation/F1.6-jobs-and-events.md) → [F1.7](epics/E1-backend-foundation/F1.7-status-and-capabilities.md) → [F2.2](epics/E2-frontend-foundation/F2.2-generated-client.md) → [F2.3](epics/E2-frontend-foundation/F2.3-live-state.md) | Run a fixture scan job, observe its events, and verify that Angular can read typed status and consume the stream. |
| 5. Reversible writes | [F1.8](epics/E1-backend-foundation/F1.8-audit-and-trash.md) | Audit and undo a tag write on a disposable fixture. |
| 6. Navigation shell | [F2.6](epics/E2-frontend-foundation/F2.6-frontend-guardrails.md) → [F2.5](epics/E2-frontend-foundation/F2.5-shell-and-routes.md), after its ngkit prerequisites | Open empty routes by URL and from navigation, and see the live connection and job state in the shell. |

<!-- BEGIN derived board -->

## Releases

| Release | Status | Features |
| -- | -- | -- |
| [Release 1 — Connected home and backend runtime](../releases/release-1/index.md) | in progress | 1 Active · 6 Closed |

## Backlog

Features with no Iteration, by State and epic.

### New

| Epic | Features |
| -- | -- |
| [E1 — Backend foundation](epics/E1-backend-foundation/index.md) | [F1.4](epics/E1-backend-foundation/F1.4-apollo-db.md), [F1.5](epics/E1-backend-foundation/F1.5-beets-actor.md), [F1.6](epics/E1-backend-foundation/F1.6-jobs-and-events.md), [F1.7](epics/E1-backend-foundation/F1.7-status-and-capabilities.md), [F1.8](epics/E1-backend-foundation/F1.8-audit-and-trash.md) |
| [E2 — Frontend foundation](epics/E2-frontend-foundation/index.md) | [F2.2](epics/E2-frontend-foundation/F2.2-generated-client.md), [F2.3](epics/E2-frontend-foundation/F2.3-live-state.md), [F2.5](epics/E2-frontend-foundation/F2.5-shell-and-routes.md), [F2.6](epics/E2-frontend-foundation/F2.6-frontend-guardrails.md) |
| [E3 — ngkit primitives apollo needs](epics/E3-ngkit-primitives/index.md) | [F3.1](epics/E3-ngkit-primitives/F3.1-overlays.md), [F3.2](epics/E3-ngkit-primitives/F3.2-form-controls.md), [F3.3](epics/E3-ngkit-primitives/F3.3-feedback.md), [F3.4](epics/E3-ngkit-primitives/F3.4-toolbar-and-selection.md), [F3.5](epics/E3-ngkit-primitives/F3.5-data-grid.md), [F3.6](epics/E3-ngkit-primitives/F3.6-command-palette.md), [F3.7](epics/E3-ngkit-primitives/F3.7-file-drop.md) |
| [E4 — Shared domain components](epics/E4-shared-domain-components/index.md) | [F4.1](epics/E4-shared-domain-components/F4.1-media-editor.md), [F4.2](epics/E4-shared-domain-components/F4.2-track-workspace.md), [F4.3](epics/E4-shared-domain-components/F4.3-dry-run-flow.md), [F4.4](epics/E4-shared-domain-components/F4.4-job-progress.md), [F4.5](epics/E4-shared-domain-components/F4.5-artwork-picker.md), [F4.6](epics/E4-shared-domain-components/F4.6-facet-view.md), [F4.7](epics/E4-shared-domain-components/F4.7-bulk-edit-panel.md), [F4.8](epics/E4-shared-domain-components/F4.8-formatting.md) |
| [E5 — Library browse](epics/E5-library-browse/index.md) | [F5.1](epics/E5-library-browse/F5.1-songs-grid.md), [F5.2](epics/E5-library-browse/F5.2-search-and-fields.md), [F5.3](epics/E5-library-browse/F5.3-albums.md), [F5.4](epics/E5-library-browse/F5.4-facet-drilldowns.md), [F5.5](epics/E5-library-browse/F5.5-column-manager.md), [F5.6](epics/E5-library-browse/F5.6-audio-preview.md) |
| [E6 — Tag editing](epics/E6-tag-editing/index.md) | [F6.1](epics/E6-tag-editing/F6.1-single-track-edit.md), [F6.2](epics/E6-tag-editing/F6.2-bulk-edit.md), [F6.3](epics/E6-tag-editing/F6.3-common-tags.md), [F6.4](epics/E6-tag-editing/F6.4-clean-tags.md), [F6.5](epics/E6-tag-editing/F6.5-identity-editor.md), [F6.6](epics/E6-tag-editing/F6.6-album-edit.md) |
| [E7 — Artwork and annotations](epics/E7-artwork-and-annotations/index.md) | [F7.1](epics/E7-artwork-and-annotations/F7.1-track-artwork.md), [F7.2](epics/E7-artwork-and-annotations/F7.2-album-artwork.md), [F7.3](epics/E7-artwork-and-annotations/F7.3-inbox-artwork.md), [F7.4](epics/E7-artwork-and-annotations/F7.4-artist-annotations.md), [F7.5](epics/E7-artwork-and-annotations/F7.5-album-annotations.md), [F7.6](epics/E7-artwork-and-annotations/F7.6-orphans-and-relink.md) |
| [E8 — Inbox and intake](epics/E8-inbox-and-intake/index.md) | [F8.1](epics/E8-inbox-and-intake/F8.1-inbox-listing.md), [F8.2](epics/E8-inbox-and-intake/F8.2-staged-edits.md), [F8.3](epics/E8-inbox-and-intake/F8.3-tag-check-gates.md), [F8.4](epics/E8-inbox-and-intake/F8.4-promotion.md), [F8.5](epics/E8-inbox-and-intake/F8.5-external-onboarding.md) |
| [E9 — Downloads and proposals](epics/E9-downloads-and-proposals/index.md) | [F9.1](epics/E9-downloads-and-proposals/F9.1-single-download.md), [F9.2](epics/E9-downloads-and-proposals/F9.2-playlist-download.md), [F9.3](epics/E9-downloads-and-proposals/F9.3-url-list-builder.md), [F9.4](epics/E9-downloads-and-proposals/F9.4-tag-proposals.md), [F9.5](epics/E9-downloads-and-proposals/F9.5-accept-proposals.md) |
| [E10 — Trim and replace](epics/E10-trim-and-replace/index.md) | [F10.1](epics/E10-trim-and-replace/F10.1-trim.md), [F10.2](epics/E10-trim-and-replace/F10.2-replace.md) |
| [E11 — Checks and relocation](epics/E11-checks-and-relocation/index.md) | [F11.1](epics/E11-checks-and-relocation/F11.1-track-checks-cache.md), [F11.2](epics/E11-checks-and-relocation/F11.2-errors-page.md), [F11.3](epics/E11-checks-and-relocation/F11.3-recheck.md), [F11.4](epics/E11-checks-and-relocation/F11.4-update-tags-from-path.md), [F11.5](epics/E11-checks-and-relocation/F11.5-relocate-plan-apply.md) |
| [E12 — Home, status and settings](epics/E12-home-status-settings/index.md) | [F12.1](epics/E12-home-status-settings/F12.1-home-dashboard.md), [F12.2](epics/E12-home-status-settings/F12.2-health-and-capabilities.md), [F12.3](epics/E12-home-status-settings/F12.3-settings-page.md) |
| [E13 — Playlists and Apple Music](epics/E13-playlists-and-apple-music/index.md) | [F13.1](epics/E13-playlists-and-apple-music/F13.1-static-playlists.md), [F13.2](epics/E13-playlists-and-apple-music/F13.2-smart-playlists.md), [F13.3](epics/E13-playlists-and-apple-music/F13.3-reorder.md), [F13.4](epics/E13-playlists-and-apple-music/F13.4-export.md), [F13.5](epics/E13-playlists-and-apple-music/F13.5-apple-stats-import.md), [F13.6](epics/E13-playlists-and-apple-music/F13.6-playlist-import-job.md), [F13.7](epics/E13-playlists-and-apple-music/F13.7-push-to-apple.md) |
| [E14 — Audit and maintenance](epics/E14-audit-and-maintenance/index.md) | [F14.1](epics/E14-audit-and-maintenance/F14.1-audit-log.md), [F14.2](epics/E14-audit-and-maintenance/F14.2-batch-undo.md), [F14.3](epics/E14-audit-and-maintenance/F14.3-history-page.md), [F14.4](epics/E14-audit-and-maintenance/F14.4-maintenance-page.md), [F14.5](epics/E14-audit-and-maintenance/F14.5-prune-and-empty-trash.md) |
| [E15 — Acceptance and cutover](epics/E15-acceptance-and-cutover/index.md) | [F15.1](epics/E15-acceptance-and-cutover/F15.1-gates-on-a-copy.md), [F15.2](epics/E15-acceptance-and-cutover/F15.2-gates-on-the-real-library.md), [F15.3](epics/E15-acceptance-and-cutover/F15.3-daily-use-and-retire.md) |

<!-- END derived board -->

Ideas not yet agreed as work are parked in the [ideas list](ideas/index.md).

Every epic, by number, is on [the epic list](epics/index.md).

## Conventions

- **Taxonomy.** Epic `E<n>` → feature `F<n>.<m>` → story `S<n>.<m>.<k>`. The
  prefix chain locates a bare ID without a lookup. IDs are permanent once a
  commit names them or work starts; a `New` item no commit names takes its new
  parent's next ID when it moves. Gaps are fine.
- **Every piece of work is an epic**, closed work included. There is no build
  log.
- **State lives on the work.** Epics and features carry `State` in a metadata
  table, stories on a `**State:**` line: `New`, `Active`, `Closed` or
  `Removed`. The board above is derived from them, never a second copy.
- **A feature's `Iteration` is its release.** A release page's Scope table is
  derived from it, so moving a feature edits only the feature.
- **A story is closed when its acceptance holds.** Each story carries an
  `**Acceptance:**` list of observable results, and the tests that prove it
  belong in that list.
- **A feature states its predecessors and its acceptance**: a `Predecessors`
  row, and, when it has several stories, a `## Acceptance` block that
  exercises every story and fails loudly.
- **Ideas are a parking lot.** An idea not yet agreed as work is a row in
  `ideas/index.md`, with no ID and no state, and a page beside it when the row
  is not enough. Agreed work that is not ready is tagged `deferred`, with
  entry criteria.
- **Design lives with the work** — a `## Design` section on the feature, or the
  epic's `design.md`. Current behaviour belongs in
  [architecture](../architecture/index.md).
- **Decisions are ADRs**, one file per topic, revised in place with a dated line
  under `## Background` when they change — see [the log](../adr/index.md).
- **Open questions live on the feature or epic they block.** Answered, a
  question becomes an ADR or a rejected option recorded on the feature, and
  leaves the page.
