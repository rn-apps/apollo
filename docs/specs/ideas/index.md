# Ideas

Ideas not yet agreed as this repository's work. An entry takes no ID and no
state, and does not authorize starting anything. An idea that needs more than
its row has a page in this folder, named after the row and linked from its
**Idea** cell. Promoting one moves its page, or its row's summary, into a new
epic or feature and deletes both; a dropped idea's row and page are deleted too.

[Back to the specs](../index.md)

| Idea | Summary | Source |
| -- | -- | -- |
| Installer | Install apollo as a tool (`lifecycle = true`): `apollo self install` puts a built, served copy under `~/.rn-forge`, with the API serving the SPA. Out of v1 ([ADR-0001](../../adr/ADR-0001.md)). | owner, 2026-11-15 |
| Network metadata | MusicBrainz or AcoustID lookup and LLM tag suggestions as proposal sources. Deferred in the old app too. | old apollo README |
| `track_read` table | Mirror the index in `apollo.db` for list, sort and filter reads off the actor, only if acceptance measures a need ([ADR-0006](../../adr/ADR-0006.md)). | old ADR-0009 |
