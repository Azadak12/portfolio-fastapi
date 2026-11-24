from fastapi.testclient import TestClient

from app.main import app, load_projects

client = TestClient(app)


def test_health():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_home_lists_every_project():
    html = client.get("/").text
    for p in load_projects():
        assert p["title"] in html


def test_every_project_page_renders_with_problem_solution_and_stack():
    for p in load_projects():
        r = client.get(f"/projects/{p['slug']}")
        assert r.status_code == 200
        for part in ("The problem", "The solution", "Stack", "Demo recording"):
            assert part in r.text


def test_live_link_shown_only_when_set():
    for p in load_projects():
        html = client.get(f"/projects/{p['slug']}").text
        assert ("Open live demo" in html) == bool(p["links"]["live"])


def test_unknown_project_404():
    assert client.get("/projects/nope").status_code == 404
    assert client.get("/api/projects/nope").status_code == 404


def test_api_projects():
    data = client.get("/api/projects").json()
    assert len(data) == len(load_projects())
