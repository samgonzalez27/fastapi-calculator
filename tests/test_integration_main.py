from pathlib import Path
from fastapi.testclient import TestClient
from app import main


client = TestClient(main.app)


def test_root_serves_index():
    # When static/index.html exists, root should return the HTML file
    r = client.get("/")
    assert r.status_code == 200
    # content-type for FileResponse with html should include text/html
    assert "text/html" in r.headers.get("content-type", "")


def test_root_without_index(monkeypatch):
    # Temporarily point static_dir to a non-existent directory to hit the fallback
    original = main.static_dir
    try:
        main.static_dir = Path("/this/path/does/not/exist")
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
    finally:
        main.static_dir = original


def test_middleware_handles_exceptions():
    # Add a temporary route that raises to exercise the middleware exception path
    async def _boom():
        raise RuntimeError("boom")

    main.app.add_api_route("/boom", _boom)
    # Use a TestClient that does not re-raise server exceptions so we can assert
    # on the response status code instead of having pytest receive the exception.
    from fastapi.testclient import TestClient as _TC

    tc = _TC(main.app, raise_server_exceptions=False)
    r = tc.get("/boom")
    assert r.status_code == 500


def test_div_endpoint_nonzero():
    r = client.get("/div", params={"a": 10, "b": 2})
    assert r.status_code == 200
    assert r.json()["result"] == 5
