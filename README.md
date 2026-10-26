# Nachiket Kulkarni: portfolio

Flask + Jinja portfolio. Plain CSS and JavaScript, no frontend build step.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# macOS/Linux:         source .venv/bin/activate
pip install -r requirements.txt
python app.py                      # http://127.0.0.1:5000  (FLASK_DEBUG=1 for debug mode)
# or the production-style server:
python -m gunicorn --bind 127.0.0.1:5000 app:app
python scripts/smoke_test.py       # renders every page and checks links and assets
```

## Routes

`/`, `/projects/<slug>` (six slugs, unchanged), `/healthz` (new, returns `{"status":"ok"}`), custom 404.

## Editing content

- Everything lives in `app.py`: `SITE`, `SKILLS`, `PROJECTS`, `EDUCATION`.
- Project screenshots go in `static/images/projects/`; list them under a project's `images`. Missing files are skipped automatically.
- Résumé: add `static/files/Nachiket_Kulkarni_Resume.pdf` and the résumé buttons appear on their own.
- `emotion-detection` is credited to its author. Delete that dict from `PROJECTS` if you don't want it listed (also fine: nothing else references it).

## Motion

- Headline words rise out of a mask on load; the pipeline line then draws across (CSS only).
- A rotating stamp (wide screens only), a scrolling ticker (pauses on hover), scroll reveals, a cursor glow and a pointer spotlight on project rows.
- `#bg-canvas` draws pipeline lanes with moving packets. Scrolling shifts the lanes at different depths and speeds the packets up; the pointer pulls nearby packets toward it. Plain JavaScript, no libraries. It pauses when the tab is hidden.
- `prefers-reduced-motion` turns all of it off: content is shown in its final state and the canvas draws one still frame.
- Copy for the ticker, bio and "What the projects taught me" lives in `TICKER`, `ABOUT` and `TAUGHT` in `app.py`. Extra project-page sections (who it's for, design targets, next steps) live in `PROJECT_EXTRAS`.

## Docker

`Dockerfile` (your original, minimally changed) and `.dockerignore` are included. See `DEPLOY.md`.
