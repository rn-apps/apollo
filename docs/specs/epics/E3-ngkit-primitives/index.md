# E3 — ngkit primitives apollo needs

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F3.1 — Overlays: modal, side panel and confirm](F3.1-overlays.md) | New | — | 1 New |
| [F3.2 — Form controls](F3.2-form-controls.md) | New | — | 1 New |
| [F3.3 — Feedback: states, badges, toast and progress](F3.3-feedback.md) | New | — | 1 New |
| [F3.4 — Toolbar, selection chip and tabs](F3.4-toolbar-and-selection.md) | New | — | 1 New |
| [F3.5 — Virtual data grid](F3.5-data-grid.md) | New | — | 1 New |
| [F3.6 — Command palette](F3.6-command-palette.md) | New | — | 1 New |
| [F3.7 — File drop zone](F3.7-file-drop.md) | New | — | 1 New |

<!-- END derived features -->

What apollo needs from `@rn-forge/ng-tailwind` (and `@rn-forge/ng`), by
primitive, before its domain components and screens can be built
([ADR-0003](../../../adr/ADR-0003.md)). **The building happens in ngkit**, under
ngkit's own epics, briefs and releases. This epic is apollo's requirements list,
and the record of which ngkit release apollo adopted each primitive at.

Each feature here has one story: apollo adopts the primitive at an ngkit
release. It closes when that release is pinned (F2.1) and an apollo spec renders
the primitive under apollo's theme. Each feature's requirements section is the
input to ngkit's spec for that primitive. ngkit decides the API, and apollo
records what it adopted.

## Status at 2026-11-15

- **ngkit v0.4.0 ships:** `RnfButton`, ng-tailwind's `tokens.css`, `base.css`
  and `tailwind.css`, and in `@rn-forge/ng` the problem helpers (E14), the
  event stream (E15) and resource invalidation (E16).

- **ngkit E9 (presentation primitives) is New and deferred.** It plans
  StatusBadge, EmptyState, StateBlock, PageSkeleton, ThemeToggle, Modal (with
  a drawer size and a dirty guard), ConfirmDialog, Toolbar, SelectionChip,
  ChipsInput, AutocompleteInput and FieldControl.

- **Not planned in ngkit:**

    - the virtual data grid and column manager;
    - tabs, toast, progress bar, the command palette UI, the tri-state field and
      the file drop zone.

    ngkit E12 holds only the headless parts: client-side sort state (F12.4) and
    the command registry (F12.8), both deferred.

## Order apollo needs them

| Order | Feature | Unblocks |
| -- | -- | -- |
| 1 | [F3.1](F3.1-overlays.md) overlays | shell (F2.5), media editor (F4.1), dry-run flow (F4.3) |
| 2 | [F3.3](F3.3-feedback.md) feedback | every screen's empty, loading and error states; job progress (F4.4) |
| 3 | [F3.2](F3.2-form-controls.md) form controls | media editor (F4.1), bulk edit panel (F4.7) |
| 4 | [F3.4](F3.4-toolbar-and-selection.md) toolbar and selection | track workspace (F4.2) |
| 5 | [F3.5](F3.5-data-grid.md) data grid | track workspace (F4.2), every list screen |
| 6 | [F3.6](F3.6-command-palette.md) command palette | shell palette (S2.5.3) |
| 7 | [F3.7](F3.7-file-drop.md) file drop | artwork picker (F4.5) |

## Open questions

- **For the ngkit owner: where does the unplanned work go?** The grid, tabs,
  toast, progress bar, palette UI, tri-state field and drop zone could join
  E9, or go into new ngkit epics. The recommendation: schedule E9 now, in the
  order above. Add the grid as its own ngkit epic, because it is the largest
  piece and has a performance gate. Put the rest into E9 as features.
