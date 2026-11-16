# E13 — Playlists and Apple Music

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F13.1 — Static playlists](F13.1-static-playlists.md) | New | — | — |
| [F13.2 — Smart playlists](F13.2-smart-playlists.md) | New | — | — |
| [F13.3 — Reorder](F13.3-reorder.md) | New | — | — |
| [F13.4 — Export](F13.4-export.md) | New | — | — |
| [F13.5 — Apple stats import](F13.5-apple-stats-import.md) | New | — | — |
| [F13.6 — Playlist import job](F13.6-playlist-import-job.md) | New | — | — |
| [F13.7 — Push to Music.app](F13.7-push-to-apple.md) | New | — | — |

<!-- END derived features -->

Static and smart playlists, reordering, export, and the Apple Music side: stats
import, playlist import as a job and push to Music.app. At parity with old
apollo. Apple sync is one-way into apollo, with promotion into Music.app as the
only write the other way ([ADR-0017](../../../adr/ADR-0017.md)); playlist views
use the E4 track workspace with an inspector, which old apollo's playlist detail
lacked.

Builds on: [E1](../E1-backend-foundation/index.md),
[E4](../E4-shared-domain-components/index.md),
[ADR-0007](../../../adr/ADR-0007.md), [ADR-0015](../../../adr/ADR-0015.md),
[ADR-0017](../../../adr/ADR-0017.md), [ADR-0020](../../../adr/ADR-0020.md).
