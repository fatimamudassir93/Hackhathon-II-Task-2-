# Docker Build Contract

**Feature**: 003-cloud-native-todo-deploy
**Date**: 2026-02-08

## Frontend Image Build

### Input

| Parameter | Value |
|-----------|-------|
| Context | `frontend/` |
| Dockerfile | `frontend/Dockerfile` |
| Image name | `todo-frontend` |
| Tag | `1.0.0` |

### Build Command

```bash
docker build -t todo-frontend:1.0.0 frontend/
```

### Dockerfile Contract

```
Stage 1 (deps):     node:20 → npm ci (production deps only)
Stage 2 (builder):  node:20 → npm ci (all deps) → next build
Stage 3 (runner):   node:20-alpine → copy standalone + static
                    → USER nextjs (UID 1001)
                    → EXPOSE 3000
                    → CMD ["node", "server.js"]
```

### Required Files

- `frontend/package.json` — dependency manifest
- `frontend/package-lock.json` — lock file for deterministic builds
- `frontend/next.config.mjs` — MUST include `output: "standalone"`
- `frontend/.dockerignore` — excludes node_modules, .next, .env

### Output Verification

```bash
# Image exists
docker images todo-frontend:1.0.0

# Image size < 200MB
docker images todo-frontend:1.0.0 --format "{{.Size}}"

# Container starts and responds
docker run -d -p 3000:3000 --name test-frontend todo-frontend:1.0.0
curl http://localhost:3000
docker rm -f test-frontend
```

---

## Backend Image Build

### Input

| Parameter | Value |
|-----------|-------|
| Context | `backend/` |
| Dockerfile | `backend/Dockerfile` |
| Image name | `todo-backend` |
| Tag | `1.0.0` |

### Build Command

```bash
docker build -t todo-backend:1.0.0 backend/
```

### Dockerfile Contract

```
Stage 1 (builder):  python:3.11-slim → pip install -r requirements.txt
Stage 2 (runtime):  python:3.11-slim → copy installed packages + src
                    → USER appuser (UID 1001)
                    → EXPOSE 8001
                    → CMD ["uvicorn", "src.main:app",
                           "--host", "0.0.0.0", "--port", "8001"]
```

### Required Files

- `backend/requirements.txt` — Python dependency list
- `backend/src/` — Application source code
- `backend/chatbot/` — Chatbot module source code
- `backend/.dockerignore` — excludes venv, __pycache__, .env, tests

### Output Verification

```bash
# Image exists
docker images todo-backend:1.0.0

# Image size < 300MB
docker images todo-backend:1.0.0 --format "{{.Size}}"

# Container starts and responds on health endpoint
docker run -d -p 8001:8001 --name test-backend todo-backend:1.0.0
curl http://localhost:8001/health
docker rm -f test-backend
```

---

## Minikube Image Loading

```bash
# Load both images into Minikube
minikube image load todo-frontend:1.0.0
minikube image load todo-backend:1.0.0

# Verify images are available in Minikube
minikube image ls | grep todo-
```

## .dockerignore Files

### frontend/.dockerignore

```
node_modules
.next
.env
.env.*
*.md
.git
.gitignore
```

### backend/.dockerignore

```
venv
__pycache__
*.pyc
.env
.env.*
*.md
.git
.gitignore
tests
chatbot/tests
commands
app.py
start.bat
verify_setup.py
```
