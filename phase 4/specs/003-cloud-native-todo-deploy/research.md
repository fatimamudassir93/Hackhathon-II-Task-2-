# Research: Cloud-Native Todo Chatbot Deployment

**Feature**: 003-cloud-native-todo-deploy
**Date**: 2026-02-08
**Status**: Complete

## R1: Frontend Containerization (Next.js)

**Decision**: Multi-stage Docker build with standalone output mode.

**Rationale**: Next.js 14.x supports `output: "standalone"` in
`next.config.mjs`, which produces a minimal self-contained server
(~30MB) without `node_modules`. This enables small Docker images
using `node:20-alpine` as the runtime stage. The build stage uses
the full `node:20` image for `npm ci` and `next build`.

**Alternatives considered**:
- **Static export (`next export`)**: Not viable — the app uses API
  routes (`app/api/`) and server-side middleware, which require a
  Node.js runtime.
- **Full `node_modules` copy**: Produces images >500MB. Standalone
  mode reduces this to ~150MB.
- **Nginx serving static build**: Not possible due to server-side
  rendering and API proxy routes.

**Key findings**:
- Next.js standalone output copies only required `node_modules`
  files into `.next/standalone/`.
- Static assets from `.next/static` and `public/` must be copied
  separately into the standalone directory.
- The standalone server listens on port 3000 by default.
- Environment variables (BACKEND_URL, BETTER_AUTH_SECRET) must be
  injected at runtime, not build time, for container portability.
- For Kubernetes: `BACKEND_URL` should be set to the backend
  Service DNS (e.g., `http://todo-backend:8001`).

## R2: Backend Containerization (FastAPI/Python)

**Decision**: Multi-stage Docker build with `python:3.11-slim`
runtime.

**Rationale**: The backend uses FastAPI with asyncpg, which
requires Python 3.9+. Python 3.11 provides the best balance of
compatibility, performance, and image size. `slim` variant avoids
full Debian overhead while keeping essential C libraries for
`psycopg2-binary` and `asyncpg`.

**Alternatives considered**:
- **`python:3.11-alpine`**: Fails to build `psycopg2-binary` and
  `asyncpg` due to missing `libpq` and build tools. Would require
  installing `gcc`, `musl-dev`, `libpq-dev` — negating the size
  advantage.
- **`python:3.14`**: `psycopg2-binary` does not build on 3.14
  (known issue from project memory).
- **Single-stage build**: Includes pip cache and build artifacts
  in the final image. Multi-stage keeps the runtime image clean.

**Key findings**:
- `requirements.txt` contains all production dependencies.
- Entry point: `uvicorn src.main:app --host 0.0.0.0 --port 8001`.
- Virtual environment (`venv/`) and test files should be excluded
  via `.dockerignore`.
- LLM provider API keys (OPENAI_API_KEY, GROQ_API_KEY,
  GEMINI_API_KEY) are sensitive and MUST use Kubernetes Secrets,
  not ConfigMaps.
- Non-secret config (DATABASE_URL pattern, LLM_PROVIDER selection,
  rate limiting) can use ConfigMaps.
- Health check endpoint needed: FastAPI can expose `/health` for
  Kubernetes probes.

## R3: Helm Chart Architecture

**Decision**: Umbrella chart with two subcharts (frontend, backend).

**Rationale**: An umbrella chart pattern lets `helm install` deploy
the entire system while keeping each service's templates isolated.
Subcharts can be independently versioned and tested with
`helm lint`. This matches the constitution's Service Separation
Requirement (Principle VII).

**Alternatives considered**:
- **Single chart with all templates**: Simpler but mixes frontend
  and backend concerns. Harder to manage independently.
- **Two independent charts**: Requires two `helm install` commands,
  breaking the P1 user story (single-command deploy).
- **Kustomize overlays**: Not Helm-based; violates the constitution
  toolchain binding.

**Key findings**:
- Chart structure: `charts/todo-chatbot/` (umbrella) with
  `charts/todo-chatbot/charts/frontend/` and
  `charts/todo-chatbot/charts/backend/`.
- `values.yaml` at umbrella level overrides subchart defaults.
- Frontend subchart: Deployment (2 replicas), Service (NodePort),
  ConfigMap.
- Backend subchart: Deployment (1 replica), Service (ClusterIP),
  ConfigMap, Secret.
- Labels follow `app.kubernetes.io/*` convention per constitution.

## R4: Minikube Image Loading Strategy

**Decision**: Use `minikube image load` for local image access.

**Rationale**: `minikube image load` copies locally-built Docker
images directly into Minikube's container runtime. This avoids
needing a registry and works with all Minikube drivers (Docker,
Hyper-V, VirtualBox).

**Alternatives considered**:
- **`eval $(minikube docker-env)`**: Only works with the Docker
  driver. Builds images inside Minikube's Docker daemon. Less
  portable across drivers.
- **Local registry (e.g., `localhost:5000`)**: Adds complexity
  (running a registry container). Overkill for local development.
- **`minikube cache add`**: Deprecated in favor of
  `minikube image load`.

**Key findings**:
- Build images locally with `docker build`.
- Load into Minikube with `minikube image load <image:tag>`.
- Set `imagePullPolicy: Never` in Kubernetes manifests to prevent
  Kubernetes from trying to pull from a remote registry.
- Tag images with a version (e.g., `todo-frontend:1.0.0`), not
  `latest`, to avoid caching issues.

## R5: Service Networking in Minikube

**Decision**: Frontend exposed via NodePort, backend via ClusterIP
with Kubernetes Service DNS for inter-service communication.

**Rationale**: NodePort is the simplest way to expose services
externally on Minikube without needing `minikube tunnel` or an
Ingress controller. ClusterIP for the backend keeps it internal-
only, matching the spec requirement (FR-007).

**Alternatives considered**:
- **LoadBalancer type**: Requires `minikube tunnel` running
  continuously. More complex for local development.
- **Ingress controller**: Adds an Ingress resource and controller
  deployment. Overkill when only two services need exposure (and
  only one externally).
- **Port forwarding (`kubectl port-forward`)**: Not declarative;
  cannot be captured in Helm charts. Violates reproducibility.

**Key findings**:
- Frontend Service: `type: NodePort`, `targetPort: 3000`.
- Backend Service: `type: ClusterIP`, `targetPort: 8001`.
- Frontend connects to backend via
  `http://todo-backend.default.svc.cluster.local:8001`.
- This URL is injected via ConfigMap as `BACKEND_URL`.
- Access frontend: `minikube service todo-frontend --url`.

## R6: Health Check Strategy

**Decision**: HTTP liveness and readiness probes for both services.

**Rationale**: HTTP probes are the most reliable for web services.
Liveness probes detect hung processes; readiness probes prevent
traffic routing before the service is ready.

**Key findings**:
- **Frontend**: Readiness probe on `GET /` (Next.js serves the
  page). Liveness probe on the same endpoint.
  `initialDelaySeconds: 10`, `periodSeconds: 15`.
- **Backend**: Add a `/health` endpoint to FastAPI that returns
  `{"status": "ok"}`. Readiness probe on `GET /health`.
  Liveness probe on `GET /health`.
  `initialDelaySeconds: 15`, `periodSeconds: 20`.
- Backend readiness should optionally check database connectivity,
  but for MVP (stateless per constitution), a simple 200 response
  suffices.

## R7: ConfigMap vs Secret Separation

**Decision**: Non-secret config in ConfigMap, credentials in
Kubernetes Secret.

**Key findings**:

| Variable | Resource | Rationale |
|----------|----------|-----------|
| BACKEND_URL | ConfigMap | Service URL, not sensitive |
| BETTER_AUTH_URL | ConfigMap | Public URL, not sensitive |
| LLM_PROVIDER | ConfigMap | Provider name, not sensitive |
| RATE_LIMIT_DEFAULT | ConfigMap | Config, not sensitive |
| ACCESS_TOKEN_EXPIRE_MINUTES | ConfigMap | Config value |
| DATABASE_URL | Secret | Contains credentials |
| BETTER_AUTH_SECRET | Secret | Signing key |
| OPENAI_API_KEY | Secret | API credential |
| GROQ_API_KEY | Secret | API credential |
| GEMINI_API_KEY | Secret | API credential |
| DATABASE_URL_NEON | Secret | Contains credentials |

## R8: Docker AI (Gordon) Capability Assessment

**Decision**: Use Gordon for initial Dockerfile generation,
then review and adjust for production readiness.

**Rationale**: Docker AI (Gordon) can generate Dockerfiles from
natural language prompts describing the application. However,
generated output may need adjustments for multi-stage builds,
non-root user setup, and Next.js standalone mode specifics.

**Key findings**:
- Gordon command: `docker ai "Generate a Dockerfile for..."`.
- Gordon produces reasonable Dockerfiles but may not know
  Next.js standalone output mode nuances.
- Agent should use Gordon first, validate output, then patch
  if needed (per constitution Principle III — AI-first with
  manual fallback).

## R9: kubectl-ai and kagent for Manifest Generation

**Decision**: Use kubectl-ai for individual manifest generation,
kagent for Helm chart scaffolding.

**Key findings**:
- `kubectl-ai` generates Kubernetes YAML from natural language
  descriptions. Good for individual Deployments and Services.
- `kagent` can scaffold Helm chart directory structures.
- Generated manifests must be saved to repository before applying
  (constitution Principle IV).
- All generated output requires review for label conventions,
  resource limits, and probe configuration.
