# E7 — Artwork and annotations

|  |  |
| -- | -- |
| **State** | New |

<!-- BEGIN derived features -->

| Feature | State | Iteration | Stories |
| -- | -- | -- | -- |
| [F7.1 — Track artwork](F7.1-track-artwork.md) | New | — | — |
| [F7.2 — Album artwork](F7.2-album-artwork.md) | New | — | — |
| [F7.3 — Inbox artwork](F7.3-inbox-artwork.md) | New | — | — |
| [F7.4 — Artist annotations](F7.4-artist-annotations.md) | New | — | — |
| [F7.5 — Album annotations](F7.5-album-annotations.md) | New | — | — |
| [F7.6 — Orphans and relink](F7.6-orphans-and-relink.md) | New | — | — |

<!-- END derived features -->

Artwork for tracks, albums and inbox files, and the annotations that carry
artist and album facts the files cannot, with orphan listing and relink. At
parity with old apollo, plus album artwork, which had an endpoint but no UI.
Artwork is served through the one artwork endpoint and chosen through the one E4
artwork picker.

Builds on: [E1](../E1-backend-foundation/index.md),
[E4](../E4-shared-domain-components/index.md),
[ADR-0010](../../../adr/ADR-0010.md), [ADR-0011](../../../adr/ADR-0011.md),
[ADR-0020](../../../adr/ADR-0020.md).
