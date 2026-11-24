# Portfolio

A small FastAPI + Jinja2 portfolio site. Each project has a problem/solution write-up, a demo recording slot, live and code links, and its stack.

## Edit the content
- `app/profile.json`: name, tagline, about, GitHub/LinkedIn/email (empty links are hidden).
- `app/projects.json`: one entry per project. Set `links.live`, `links.code`, and `video` to `{"type": "embed", "src": "<YouTube/Loom embed URL>"}` or `{"type": "file", "src": "/static/media/demo.mp4"}`.

## Run
```sh
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload
.venv/bin/python -m pytest -q
```

JSON API: `/api/projects`, `/api/projects/{slug}`; docs at `/api/docs`; health at `/healthz`. Deploys to Render's free tier via `render.yaml`.
