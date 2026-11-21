"""S1.3.1: every `ApolloError` answers as an RFC 9457 problem."""

from collections.abc import Awaitable, Callable, Iterator
from pathlib import Path

from fastapi.testclient import TestClient
from rn_forge.web import PROBLEM_MEDIA_TYPE, WireModel

from apollo_api.app import create_app
from apollo_api.platform.errors import ApolloError, NotFoundError, WriteFailedError

EXPECTED: dict[str, int] = {
    "not-found": 404,
    "conflict": 409,
    "file-missing": 409,
    "write-failed": 500,
    "validation": 422,
    "artwork-fetch": 502,
    "artwork-invalid-image": 422,
    "job-failed": 500,
    "icloud-sync-active": 409,
    "invalid-source": 422,
    "inbox-preview-stale": 409,
    "trim-range": 422,
    "trim-result-too-short": 422,
    "capability-unavailable": 409,
    "invalid-query": 422,
    "plan-stale": 409,
}


def _subclasses(base: type[ApolloError]) -> Iterator[type[ApolloError]]:
    for sub in base.__subclasses__():
        yield sub
        yield from _subclasses(sub)


def _raiser(error: type[ApolloError]) -> Callable[[], Awaitable[None]]:
    async def raise_it() -> None:
        raise error("failed")

    return raise_it


def test_s1_3_1_1_every_error_registered() -> None:
    application = create_app()
    subclasses = list(_subclasses(ApolloError))
    for cls in subclasses:
        application.add_api_route(f"/raise/{cls.code}", _raiser(cls))
    application.add_api_route("/raise/base", _raiser(ApolloError))
    assert {cls.code: cls.status_code for cls in subclasses} == EXPECTED
    client = TestClient(application, raise_server_exceptions=False)
    for cls in subclasses:
        response = client.get(f"/raise/{cls.code}")
        body = response.json()
        assert response.status_code == cls.status_code
        assert response.headers["content-type"].startswith(PROBLEM_MEDIA_TYPE)
        assert body["type"] == f"/problems/{cls.code}"
        assert body["status"] == cls.status_code
    base = client.get("/raise/base")
    assert base.status_code == 500
    assert base.json()["type"] == "/problems/internal-error"


def test_s1_3_1_2_extensions() -> None:
    application = create_app()

    async def missing() -> None:
        raise NotFoundError("track {} not found", 7, track_id=7, reason_code="gone")

    async def full() -> None:
        raise WriteFailedError("disk full", path="/a")

    application.add_api_route("/missing", missing)
    application.add_api_route("/full", full)
    client = TestClient(application, raise_server_exceptions=False)
    body = client.get("/missing").json()
    assert body["trackId"] == 7
    assert body["reasonCode"] == "gone"
    assert body["detail"] == "track 7 not found"
    assert "code" not in body
    response = client.get("/full")
    assert response.status_code == 500
    assert "path" not in response.json()
    assert "pathName" not in response.json()


def test_s1_3_1_3_validation_422() -> None:
    application = create_app()

    class Payload(WireModel):
        display_name: str

    @application.post("/validate")
    async def validate(body: Payload) -> None:
        return None

    response = TestClient(application, raise_server_exceptions=False).post(
        "/validate", json={}
    )
    body = response.json()
    assert response.status_code == 422
    assert response.headers["content-type"].startswith(PROBLEM_MEDIA_TYPE)
    assert body["type"] == "/problems/validation-error"
    assert body["errors"] == [
        {"pointer": "/displayName", "detail": "This field is required."}
    ]


def test_s1_3_1_4_unhandled_500(configured_env: dict[str, Path]) -> None:
    application = create_app()

    async def boom() -> None:
        raise RuntimeError("secret internals")

    application.add_api_route("/boom", boom)
    with TestClient(application, raise_server_exceptions=False) as client:
        response = client.get("/boom")
    body = response.json()
    assert response.status_code == 500
    assert body["type"] == "/problems/internal-error"
    assert body["detail"] == "An unexpected error occurred."
    assert "secret internals" not in response.text
    logs = (configured_env["state"] / "logs").glob("apollo*")
    text = "".join(path.read_text() for path in logs)
    assert "RuntimeError: secret internals" in text
