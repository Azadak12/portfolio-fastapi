"""Portfolio site: FastAPI + Jinja2. Content lives in profile.json / projects.json."""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE = Path(__file__).parent
templates = Jinja2Templates(directory=BASE / "templates")

app = FastAPI(title="Portfolio", docs_url="/api/docs", redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


def load_profile() -> dict:
    return json.loads((BASE / "profile.json").read_text())


def load_projects() -> list[dict]:
    return json.loads((BASE / "projects.json").read_text())


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/api/projects")
def api_projects() -> list[dict]:
    return load_projects()


@app.get("/api/projects/{slug}")
def api_project(slug: str) -> dict:
    for project in load_projects():
        if project["slug"] == slug:
            return project
    raise HTTPException(status_code=404, detail="Project not found")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"profile": load_profile(), "projects": load_projects()},
    )


@app.get("/projects/{slug}", response_class=HTMLResponse)
def project_page(request: Request, slug: str):
    projects = load_projects()
    project = next((p for p in projects if p["slug"] == slug), None)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    others = [p for p in projects if p["slug"] != slug]
    return templates.TemplateResponse(
        request,
        "project.html",
        {"profile": load_profile(), "project": project, "others": others},
    )


@app.exception_handler(404)
def not_found(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return HTMLResponse('{"detail":"Not found"}', status_code=404, media_type="application/json")
    return templates.TemplateResponse(
        request, "404.html", {"profile": load_profile()}, status_code=404
    )
