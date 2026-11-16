# apollo

What this repository is, in a paragraph.

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
