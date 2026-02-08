# Helm Values Contract: todo-chatbot

**Feature**: 003-cloud-native-todo-deploy
**Date**: 2026-02-08

## Overview

This document defines the authoritative contract for
`charts/todo-chatbot/values.yaml` — the single configuration
surface for the entire deployment.

## values.yaml Schema

```yaml
# ============================================================
# Umbrella Chart: todo-chatbot
# ============================================================

# -- Frontend subchart overrides
frontend:
  # -- Number of frontend replicas
  replicaCount: 2

  image:
    # -- Frontend Docker image repository (local)
    repository: todo-frontend
    # -- Frontend image tag
    tag: "1.0.0"
    # -- Image pull policy (Never for local Minikube images)
    pullPolicy: Never

  service:
    # -- Service type for external access on Minikube
    type: NodePort
    # -- Service port
    port: 80
    # -- Container target port
    targetPort: 3000

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi

  probes:
    liveness:
      path: /
      port: 3000
      initialDelaySeconds: 10
      periodSeconds: 15
    readiness:
      path: /
      port: 3000
      initialDelaySeconds: 5
      periodSeconds: 10

  config:
    # -- Backend URL for frontend-to-backend communication
    BACKEND_URL: "http://todo-backend:8001"
    # -- Better Auth public URL
    BETTER_AUTH_URL: "http://localhost:3000"

  secrets:
    # -- JWT signing secret (base64 encoded in Secret resource)
    BETTER_AUTH_SECRET: ""
    # -- Frontend database URL
    DATABASE_URL: ""
    DATABASE_URL_NEON: ""

# -- Backend subchart overrides
backend:
  # -- Number of backend replicas
  replicaCount: 1

  image:
    # -- Backend Docker image repository (local)
    repository: todo-backend
    # -- Backend image tag
    tag: "1.0.0"
    # -- Image pull policy (Never for local Minikube images)
    pullPolicy: Never

  service:
    # -- Service type (internal only)
    type: ClusterIP
    # -- Service port
    port: 8001
    # -- Container target port
    targetPort: 8001

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi

  probes:
    liveness:
      path: /health
      port: 8001
      initialDelaySeconds: 15
      periodSeconds: 20
    readiness:
      path: /health
      port: 8001
      initialDelaySeconds: 10
      periodSeconds: 10

  config:
    # -- LLM provider selection
    LLM_PROVIDER: "groq"
    # -- Rate limiting configuration
    RATE_LIMIT_DEFAULT: "5/minute"
    # -- Token expiry
    ACCESS_TOKEN_EXPIRE_MINUTES: "1440"
    # -- Better Auth URL
    BETTER_AUTH_URL: "http://localhost:3000"

  secrets:
    # -- Database connection strings (base64 encoded)
    DATABASE_URL: ""
    DATABASE_URL_NEON: ""
    # -- Authentication secret
    BETTER_AUTH_SECRET: ""
    # -- LLM API keys (populate the one matching LLM_PROVIDER)
    OPENAI_API_KEY: ""
    GROQ_API_KEY: ""
    GEMINI_API_KEY: ""
```

## Override Examples

### Increase frontend replicas

```bash
helm install todo-chatbot ./charts/todo-chatbot \
  --set frontend.replicaCount=3
```

### Use a different image tag

```bash
helm install todo-chatbot ./charts/todo-chatbot \
  --set frontend.image.tag="2.0.0" \
  --set backend.image.tag="2.0.0"
```

### Set secrets at install time

```bash
helm install todo-chatbot ./charts/todo-chatbot \
  --set backend.secrets.GROQ_API_KEY="gsk_xxx" \
  --set backend.secrets.DATABASE_URL="postgresql+asyncpg://..." \
  --set backend.secrets.BETTER_AUTH_SECRET="eDpBF53..."
```

### Use custom values file

```bash
helm install todo-chatbot ./charts/todo-chatbot \
  -f my-values.yaml
```

## Validation Rules

- `frontend.image.pullPolicy` MUST be `Never` for local Minikube.
- `backend.image.pullPolicy` MUST be `Never` for local Minikube.
- `frontend.service.type` MUST be `NodePort` for Minikube access.
- `backend.service.type` MUST be `ClusterIP` (internal only).
- `secrets.*` values MUST NOT be committed to version control
  with real credentials — use `--set` or a gitignored values file.
- All `config.*` values MUST be non-sensitive configuration only.
