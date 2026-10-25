# Nachiket Kulkarni — Editorial Portfolio

A light, editorial-style Flask portfolio with lime accents, expressive motion, and six dedicated project-detail pages.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Routes

- `/` — portfolio homepage
- `/projects/project-management-rag`
- `/projects/cloud-campus`
- `/projects/face-recognition-attendance`
- `/projects/voice-controlled-ai-agent`
- `/projects/emotion-detection`
- `/projects/milo-ai-study-partner`

## Before publishing

- Replace the placeholder email, GitHub, and LinkedIn links in `templates/base.html`.
- Review every project description and ensure it matches your actual implementation.
- Add verified technologies, screenshots, GitHub URLs, demo links, your contribution, and measured results where available.
- Keep secrets and environment files out of Git.
- Merge these files into your existing repository carefully. This package does not include or replace your existing CI/CD configuration, Dockerfile, Kubernetes manifests, or Jenkinsfile.
- If your current pipeline expects a different app entry point or port, adapt the deployment configuration rather than overwriting it blindly.


## Personal links

- Email: `nachikulkarni4115@gmail.com`
- GitHub: `https://github.com/nachikulkarni4115-cell`
- LinkedIn: `https://www.linkedin.com/in/nachiket-kulkarni-636498299/`

## Report images

The project image directory is `static/images/projects/`. To add accurate screenshots, diagrams, or result images from your reports, provide the PDFs for the six projects. Images should be extracted from the matching report and placed on the corresponding project detail page; no unrelated stock visuals are used as substitutes.
