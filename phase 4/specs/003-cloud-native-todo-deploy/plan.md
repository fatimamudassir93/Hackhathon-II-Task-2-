# Implementation Plan: Cloud-Native Todo Chatbot Deployment

**Branch**: `003-cloud-native-todo-deploy` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-cloud-native-todo-deploy/spec.md`

## Summary

Containerize the existing Phase III Todo Chatbot (Next.js frontend +
FastAPI backend) into Docker images, package them as a Helm umbrella
chart with two subcharts, and deploy the complete system to a local
Minikube cluster with a single `helm install` command. All
infrastructure artifacts (Dockerfiles, Helm charts, Kubernetes
manifests) are generated using AI-powered tools (Docker AI Gordon,
kubectl-ai, kagent) and documented as reproducible CLI commands.

## Technical Context

**Language/Version**: Node.js 20 (frontend), Python 3.11 (backend)
**Primary Dependencies**: Docker, Helm 3, Minikube, kubectl,
Docker AI (Gordon), kubectl-ai, kagent
**Storage**: N/A (stateless services; database is external Neon
PostgreSQL, not deployed in-cluster)
**Testing**: `helm lint`, `kubectl apply --dry-run=client`,
`docker build` verification, pod health checks
**Target Platform**: Local Minikube cluster (Docker driver, Windows)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: All pods Running within 120s of `helm install`,
frontend accessible within 30s of pods ready
**Constraints**: Local-only (no cloud), stateless services,
Minikube resource budget (2 CPU, 4GB memory)
**Scale/Scope**: 2 frontend replicas, 1 backend replica, single
Minikube cluster

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Status | Notes |
|---|-----------|--------|-------|
| I | Automation Agent Role | PASS | Agent generates all Dockerfiles, Helm charts, manifests |
| II | Infrastructure Toolchain Binding | PASS | Using Gordon, kubectl-ai, kagent, Minikube, Helm, kubectl |
| III | AI-First Artifact Generation | PASS | Dockerfiles via Gordon, manifests via kubectl-ai, charts via kagent |
| IV | CLI Reproducibility Mandate | PASS | All steps documented as CLI commands in quickstart.md |
| V | Local-Only Deployment Constraint | PASS | Minikube only, no cloud, imagePullPolicy: Never |
| VI | Stateless Services Mandate | PASS | No in-container state, external DB only |
| VII | Service Separation Requirement | PASS | Separate frontend/backend Dockerfiles, Deployments, Services |
| VIII | Kubernetes & Helm Best Practices | PASS | Resource limits, probes, labels, ConfigMaps, values.yaml |
| IX | Deployment Scope Lock | PASS | Only Dockerfiles, Helm charts, K8s manifests, Minikube config |
| X | Spec-Driven Execution Compliance | PASS | All decisions reference spec and constitution |

**Gate result**: ALL PASS — proceed to implementation.

## Project Structure

### Documentation (this feature)

```text
specs/003-cloud-native-todo-deploy/
├── plan.md                  # This file
├── research.md              # Phase 0: technology decisions
├── data-model.md            # Phase 1: infrastructure entities
├── quickstart.md            # Phase 1: deployment runbook
├── contracts/
│   ├── helm-values-contract.md    # Helm values.yaml schema
│   └── docker-build-contract.md   # Dockerfile specifications
└── tasks.md                 # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
frontend/                    # Existing Next.js application
├── Dockerfile               # NEW — generated via Docker AI (Gordon)
├── .dockerignore            # NEW — excludes node_modules, .next, .env
├── next.config.mjs          # MODIFIED — add output: "standalone"
└── (existing source...)

backend/                     # Existing FastAPI application
├── Dockerfile               # NEW — generated via Docker AI (Gordon)
├── .dockerignore            # NEW — excludes venv, __pycache__, .env
├── src/
│   └── main.py              # MODIFIED — add /health endpoint
└── (existing source...)

charts/                      # NEW — Helm chart directory
└── todo-chatbot/            # Umbrella chart
    ├── Chart.yaml
    ├── values.yaml           # Configurable parameters
    ├── charts/
    │   ├── frontend/         # Frontend subchart
    │   │   ├── Chart.yaml
    │   │   ├── values.yaml
    │   │   └── templates/
    │   │       ├── deployment.yaml
    │   │       ├── service.yaml
    │   │       ├── configmap.yaml
    │   │       ├── secret.yaml
    │   │       └── _helpers.tpl
    │   └── backend/          # Backend subchart
    │       ├── Chart.yaml
    │       ├── values.yaml
    │       └── templates/
    │           ├── deployment.yaml
    │           ├── service.yaml
    │           ├── configmap.yaml
    │           ├── secret.yaml
    │           └── _helpers.tpl
    └── templates/
        └── NOTES.txt          # Post-install instructions
```

**Structure Decision**: Umbrella chart with subcharts pattern.
Chosen because it enables single-command deployment (P1 user story)
while maintaining service separation (constitution Principle VII).
Each subchart owns its own Deployment, Service, ConfigMap, and
Secret templates.

## Implementation Phases

### Phase 0: Research (COMPLETE)

All technology decisions documented in [research.md](./research.md).
Key decisions:

1. **Frontend**: Multi-stage build with Next.js standalone output
2. **Backend**: Multi-stage build with python:3.11-slim
3. **Helm**: Umbrella chart + 2 subcharts
4. **Images**: `minikube image load` for local access
5. **Networking**: Frontend NodePort, Backend ClusterIP, Service DNS
6. **Health**: HTTP probes on `/` (frontend) and `/health` (backend)
7. **Config**: ConfigMap for non-secret, Secret for credentials
8. **Gordon**: AI-first Dockerfile generation with manual review
9. **kubectl-ai/kagent**: AI-first manifest/chart generation

### Phase 1: Design (COMPLETE)

Artifacts produced:

- **[data-model.md](./data-model.md)**: Infrastructure entity
  specifications (images, deployments, services, configmaps, secrets)
- **[contracts/helm-values-contract.md](./contracts/helm-values-contract.md)**:
  Complete `values.yaml` schema with override examples
- **[contracts/docker-build-contract.md](./contracts/docker-build-contract.md)**:
  Dockerfile specifications and build verification commands
- **[quickstart.md](./quickstart.md)**: Step-by-step deployment
  runbook with all CLI commands

### Phase 2: Implementation (pending /sp.tasks)

High-level implementation sequence from user input:

1. Analyze existing Phase III frontend and backend source
2. Generate Dockerfiles using Docker AI (Gordon)
3. Build and tag Docker images locally
4. Create Helm chart structure (kagent)
5. Generate Kubernetes manifests via kubectl-ai
6. Package frontend and backend as Helm subcharts
7. Deploy to Minikube using Helm
8. Verify pod health and services
9. Optimize resources using kagent

Detailed task breakdown will be generated by `/sp.tasks`.

## Complexity Tracking

> No constitution violations. No complexity justifications needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | — | — |
