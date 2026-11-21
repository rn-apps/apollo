"""S1.3.2: paging shapes and app limits."""

from __future__ import annotations

from fastapi import Request
from fastapi.testclient import TestClient
from rn_forge.web import PROBLEM_MEDIA_TYPE

from apollo_api.app import create_app
from apollo_api.platform.paging import OffsetPage


def test_s1_3_2_1_offset_page() -> None:
    page = OffsetPage[int](items=[1, 2], offset=4, limit=1000, total=9)
    assert page.limit == 500
    assert page.model_dump() == {"items": [1, 2], "offset": 4, "limit": 500, "total": 9}
    assert OffsetPage[int](items=[], offset=0, limit=50, total=0).limit == 50

    application = create_app()

    @application.get("/page", response_model=OffsetPage[int])
    def _page() -> OffsetPage[int]:
        return OffsetPage[int](items=[1], offset=0, limit=10, total=1)

    response = TestClient(application).get("/page")
    assert response.status_code == 200
    assert response.json() == {"items": [1], "offset": 0, "limit": 10, "total": 1}


def test_s1_3_2_2_body_limit() -> None:
    application = create_app()

    @application.post("/echo")
    async def _echo(request: Request) -> dict[str, int]:
        return {"size": len(await request.body())}

    client = TestClient(application, raise_server_exceptions=False)
    ok = client.post("/echo", content=b"x" * (20 * 1024 * 1024))
    assert ok.status_code == 200
    assert ok.json() == {"size": 20 * 1024 * 1024}
    big = client.post("/echo", content=b"x" * (26 * 1024 * 1024))
    assert big.status_code == 413
    assert big.headers["content-type"].startswith(PROBLEM_MEDIA_TYPE)
    assert big.json()["status"] == 413


def test_s1_3_2_3_no_cors() -> None:
    client = TestClient(create_app())
    response = client.get("/livez", headers={"Origin": "http://example.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
    preflight = client.options(
        "/livez",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" not in preflight.headers
