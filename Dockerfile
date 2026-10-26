FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
# Build fails here if gunicorn (or Flask) cannot be installed or imported.
RUN pip install --no-cache-dir -r requirements.txt \
 && python -c "import flask, gunicorn" \
 && python -m gunicorn --version

COPY . .

# Build fails if the app or any template/static file the site needs is missing.
RUN python -m py_compile app.py \
 && test -f templates/index.html \
 && test -f templates/project_detail.html \
 && test -f templates/404.html \
 && test -f static/css/style.css \
 && test -f static/js/main.js

EXPOSE 5000

# python -m gunicorn does not depend on a `gunicorn` executable being on PATH.
CMD ["python", "-m", "gunicorn", "--workers", "1", "--timeout", "60", "--bind", "0.0.0.0:5000", "app:app"]
