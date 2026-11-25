# apollo

apollo is a local-first music-library workstation for macOS. Audio files are the
source of truth; beets is the tag and index layer, a FastAPI service exposes
safe, dry-run-first, reversible use cases, and an Angular app is the
keyboard-first management UI ([ADR-0001](docs/adr/ADR-0001.md)). This repository
is a rebuild of the old apollo on kiln, pykit and ngkit
([ADR-0002](docs/adr/ADR-0002.md)); status and what is next are on
[the spec board](docs/specs/index.md).

## Working here

- Run everything through `task`. `task validate` is the gate.
- A file whose first line says it was generated is owned by kiln: edit
  `.rn-forge/kiln/config.toml` and run `task kiln:apply`, never the file. The
  standard is [.rn-forge/kiln/standard.md](.rn-forge/kiln/standard.md).

## Running the API

`task api:dev` serves `apps/api/src/apollo_api/app.py`, which defines the ASGI
application as `app`. `kiln new` seeded it with a small router and a test; the
application and its tests are repo-owned from then on.

The smallest such module uses `rn-forge-fastapi`'s standard application:

```python
from rn_forge.fastapi import AppConfig, FastApiApp

app = FastApiApp(AppConfig())
```

## Conventions

- Python 3.14, `src/` layout, pyright strict, ruff for lint and format.
