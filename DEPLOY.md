# Validate and deploy

Nothing here pushes, publishes or deploys by itself. Do each step by hand, in order.

## 1. Local checks (any machine)
```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/smoke_test.py
python -m gunicorn --bind 127.0.0.1:5000 app:app       # open http://127.0.0.1:5000, check phone width too
```

## 2. Copy to the EC2 project
```bash
# on your laptop, from the folder containing this project
scp -r -i <key.pem> ./portfolio-redesign ec2-user@<ec2-ip>:~/portfolio-redesign
# on EC2: back up first
cd ~/<your-existing-project> && git status && git checkout -b redesign
cp -r . ../portfolio-backup
```
Copy these over your project, keeping your own Jenkinsfile and k8s files: `app.py`, `requirements.txt`, `Dockerfile`, `.dockerignore` (merge if you already have one), `.gitignore`, `README.md`, `DEPLOY.md`, `templates/`, `static/`, `scripts/`.
Delete `static/images/projects/README.txt` if it exists.

## 3. Dockerfile (already adapted to yours)
The included `Dockerfile` is your original with three changes: `python -m gunicorn` instead of the bare `gunicorn` executable, a build-time check that gunicorn imports, and a build-time check that the templates and static files exist. Workers, timeout, port and `COPY . .` are unchanged. `.dockerignore` now keeps `.venv`, `.git` and `__pycache__` out of the build.

## 4. Build and test the image on EC2 (no push)
```bash
docker build -t portfolio-test .
docker run --rm -d --name portfolio-test -p 5001:5000 portfolio-test
sleep 3
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/static/css/style.css
curl -s http://localhost:5001/healthz
docker exec portfolio-test python -m gunicorn --version
docker logs portfolio-test | tail
docker rm -f portfolio-test
```
Expect 200, 200, `{"status":"ok"}`. If any step fails, stop.

## 5. Commit, then trigger Jenkins
Your Jenkinsfile checks out branch `main` of `serverless-hub`, so Jenkins only deploys what is on `main`.
```bash
git add -A && git commit -m "Redesign portfolio; add gunicorn to requirements"
git push origin redesign
# after step 4 passed: merge redesign into main (PR or git merge), push main
```
Then run the Jenkins job. It builds `nachiket1/my-cicd-app:<BUILD_NUMBER>`, pushes it, and runs `kubectl set image deployment/my-cicd-app`. Check with `kubectl rollout status deployment/my-cicd-app`. To roll back: `kubectl rollout undo deployment/my-cicd-app`.

## Likely cause of the gunicorn error
The uploaded `requirements.txt` contained only Flask. If your Dockerfile installs from it and starts `gunicorn ...`, you get exactly `exec: "gunicorn": executable file not found in $PATH`. Your Dockerfile confirms the start command: it uses the bare `gunicorn` executable in exec form. Check that the `requirements.txt` already on `main` lacks gunicorn; this version adds it.
