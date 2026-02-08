# Data Model: Cloud-Native Todo Chatbot Deployment

**Feature**: 003-cloud-native-todo-deploy
**Date**: 2026-02-08

## Overview

This feature does not introduce application-level data entities.
It defines infrastructure entities — the Kubernetes resources and
Docker artifacts that compose the deployment topology.

## Infrastructure Entities

### Docker Image: todo-frontend

| Attribute | Value |
|-----------|-------|
| Base image (build) | node:20 |
| Base image (runtime) | node:20-alpine |
| Source directory | frontend/ |
| Build output | .next/standalone + .next/static + public/ |
| Exposed port | 3000 |
| Run user | nextjs (non-root, UID 1001) |
| Tag format | todo-frontend:<version> |
| Max image size | 200MB |

### Docker Image: todo-backend

| Attribute | Value |
|-----------|-------|
| Base image (build) | python:3.11-slim |
| Base image (runtime) | python:3.11-slim |
| Source directory | backend/ |
| Entry point | uvicorn src.main:app --host 0.0.0.0 --port 8001 |
| Exposed port | 8001 |
| Run user | appuser (non-root, UID 1001) |
| Tag format | todo-backend:<version> |
| Max image size | 300MB |

### Helm Chart: todo-chatbot (umbrella)

| Attribute | Value |
|-----------|-------|
| Chart name | todo-chatbot |
| Chart version | 0.1.0 |
| App version | 1.0.0 |
| Location | charts/todo-chatbot/ |
| Subcharts | frontend, backend |
| Install command | helm install todo-chatbot ./charts/todo-chatbot |

### Kubernetes Deployment: frontend

| Attribute | Value |
|-----------|-------|
| Replicas | 2 |
| Image | todo-frontend:1.0.0 |
| Container port | 3000 |
| Resource requests | cpu: 100m, memory: 128Mi |
| Resource limits | cpu: 250m, memory: 256Mi |
| Liveness probe | GET / :3000, delay 10s, period 15s |
| Readiness probe | GET / :3000, delay 5s, period 10s |
| Image pull policy | Never (local Minikube images) |

### Kubernetes Deployment: backend

| Attribute | Value |
|-----------|-------|
| Replicas | 1 |
| Image | todo-backend:1.0.0 |
| Container port | 8001 |
| Resource requests | cpu: 100m, memory: 128Mi |
| Resource limits | cpu: 500m, memory: 512Mi |
| Liveness probe | GET /health :8001, delay 15s, period 20s |
| Readiness probe | GET /health :8001, delay 10s, period 10s |
| Image pull policy | Never (local Minikube images) |

### Kubernetes Service: todo-frontend

| Attribute | Value |
|-----------|-------|
| Type | NodePort |
| Port | 80 |
| Target port | 3000 |
| Selector | app.kubernetes.io/name: frontend |
| External access | minikube service todo-frontend --url |

### Kubernetes Service: todo-backend

| Attribute | Value |
|-----------|-------|
| Type | ClusterIP |
| Port | 8001 |
| Target port | 8001 |
| Selector | app.kubernetes.io/name: backend |
| DNS | todo-backend.default.svc.cluster.local |

### Kubernetes ConfigMap: todo-backend-config

| Key | Value |
|-----|-------|
| BACKEND_URL | http://todo-backend:8001 |
| BETTER_AUTH_URL | (set via values.yaml) |
| LLM_PROVIDER | groq |
| RATE_LIMIT_DEFAULT | 5/minute |
| ACCESS_TOKEN_EXPIRE_MINUTES | 1440 |

### Kubernetes ConfigMap: todo-frontend-config

| Key | Value |
|-----|-------|
| BACKEND_URL | http://todo-backend:8001 |
| BETTER_AUTH_URL | (set via values.yaml) |

### Kubernetes Secret: todo-backend-secrets

| Key | Description |
|-----|-------------|
| DATABASE_URL | PostgreSQL connection string (asyncpg) |
| DATABASE_URL_NEON | PostgreSQL connection string (standard) |
| BETTER_AUTH_SECRET | JWT signing secret (32+ bytes) |
| OPENAI_API_KEY | OpenAI API key (if using OpenAI provider) |
| GROQ_API_KEY | Groq API key (if using Groq provider) |
| GEMINI_API_KEY | Gemini API key (if using Gemini provider) |

### Kubernetes Secret: todo-frontend-secrets

| Key | Description |
|-----|-------------|
| BETTER_AUTH_SECRET | JWT signing secret (shared with backend) |
| DATABASE_URL | Frontend database connection (Neon) |
| DATABASE_URL_NEON | Frontend database connection (standard) |

## Entity Relationships

```text
Helm Chart (todo-chatbot)
├── Subchart: frontend
│   ├── Deployment (2 replicas) → Image: todo-frontend:1.0.0
│   ├── Service (NodePort:80 → 3000)
│   ├── ConfigMap (todo-frontend-config)
│   └── Secret (todo-frontend-secrets)
└── Subchart: backend
    ├── Deployment (1 replica) → Image: todo-backend:1.0.0
    ├── Service (ClusterIP:8001 → 8001)
    ├── ConfigMap (todo-backend-config)
    └── Secret (todo-backend-secrets)

Network Flow:
  Browser → NodePort → frontend:3000 → ClusterIP → backend:8001
```

## Validation Rules

- Image tags MUST NOT be `latest` — use semantic version tags.
- `imagePullPolicy` MUST be `Never` for locally-loaded images.
- Resource requests MUST be set to enable Kubernetes scheduling.
- Resource limits MUST be set to prevent runaway containers.
- Secrets MUST be base64-encoded in Kubernetes Secret manifests.
- ConfigMap values MUST NOT contain credentials or API keys.
