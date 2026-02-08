# Tasks: Cloud-Native Todo Chatbot Deployment

**Input**: Design documents from `/specs/003-cloud-native-todo-deploy/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in the feature specification. No test tasks generated.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`
- **Helm charts**: `charts/todo-chatbot/`
- **Specs**: `specs/003-cloud-native-todo-deploy/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the project structure, source code modifications, and tooling prerequisites required before any containerization or deployment work begins.

- [ ] T001 Verify prerequisites are installed and accessible: Docker Desktop, Minikube, kubectl, Helm, Docker AI (Gordon), kubectl-ai, kagent — document versions
- [ ] T002 [P] Add `output: "standalone"` to Next.js config in frontend/next.config.mjs
- [ ] T003 [P] Add `/health` endpoint to FastAPI backend in backend/src/main.py returning `{"status": "ok"}`
- [ ] T004 [P] Create frontend/.dockerignore excluding node_modules, .next, .env, .env.*, *.md, .git, .gitignore
- [ ] T005 [P] Create backend/.dockerignore excluding venv, __pycache__, *.pyc, .env, .env.*, *.md, .git, .gitignore, tests, chatbot/tests, commands, app.py, start.bat, verify_setup.py
- [ ] T006 Create Helm chart directory structure: charts/todo-chatbot/ with charts/todo-chatbot/charts/frontend/ and charts/todo-chatbot/charts/backend/ subdirectories

**Checkpoint**: Project structure prepared. Source code has standalone output and health endpoint. Directory tree matches plan.md layout.

---

## Phase 2: Foundational — Containerize Services (US4 prerequisite, blocking)

**Purpose**: Generate Dockerfiles using Docker AI (Gordon) and build container images. This maps to User Story 4 (P4) but is a blocking prerequisite for all other stories — no Helm deploy (US1), service access (US2), or observability (US3) is possible without working container images.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Implementation

- [ ] T007 [US4] Generate frontend Dockerfile using Docker AI (Gordon): run `docker ai "Generate a multi-stage Dockerfile for a Next.js 14 app with standalone output. Use node:20 for build, node:20-alpine for runtime. Run as non-root user nextjs (UID 1001). Copy .next/standalone, .next/static, and public. Expose port 3000. CMD node server.js"` — save output to frontend/Dockerfile
- [ ] T008 [US4] Review and adjust generated frontend/Dockerfile: verify multi-stage build stages (deps, builder, runner), non-root user setup, standalone output copy, EXPOSE 3000, CMD per contracts/docker-build-contract.md
- [ ] T009 [US4] Build frontend Docker image: run `docker build -t todo-frontend:1.0.0 frontend/` — verify build succeeds and image size is under 200MB
- [ ] T010 [US4] Generate backend Dockerfile using Docker AI (Gordon): run `docker ai "Generate a multi-stage Dockerfile for a Python 3.11 FastAPI app. Use python:3.11-slim for both stages. Install from requirements.txt. Copy src/ and chatbot/ directories. Run as non-root user appuser (UID 1001). Expose port 8001. CMD uvicorn src.main:app --host 0.0.0.0 --port 8001"` — save output to backend/Dockerfile
- [ ] T011 [US4] Review and adjust generated backend/Dockerfile: verify multi-stage build, non-root user, pip install from requirements.txt, src/ and chatbot/ copy, EXPOSE 8001, CMD per contracts/docker-build-contract.md
- [ ] T012 [US4] Build backend Docker image: run `docker build -t todo-backend:1.0.0 backend/` — verify build succeeds and image size is under 300MB
- [ ] T013 [US4] Start Minikube cluster: run `minikube start --driver=docker --cpus=2 --memory=4096` — verify with `minikube status`
- [ ] T014 [US4] Load images into Minikube: run `minikube image load todo-frontend:1.0.0` and `minikube image load todo-backend:1.0.0` — verify with `minikube image ls | grep todo-`

**Checkpoint**: Both Docker images build successfully, are under size limits, and are loaded into Minikube. US4 acceptance scenarios satisfied.

---

## Phase 3: User Story 1 — Deploy Entire System with Single Helm Install (Priority: P1) 🎯 MVP

**Goal**: Create a Helm umbrella chart with frontend and backend subcharts that deploys the full system with one `helm install` command.

**Independent Test**: Run `helm install todo-chatbot ./charts/todo-chatbot` on Minikube. Both frontend and backend pods reach Running state within 120s. `helm uninstall` removes all resources cleanly.

### Implementation

- [ ] T015 [US1] Create umbrella chart metadata in charts/todo-chatbot/Chart.yaml: name=todo-chatbot, version=0.1.0, appVersion=1.0.0, type=application, with frontend and backend as dependencies
- [ ] T016 [P] [US1] Create frontend subchart Chart.yaml in charts/todo-chatbot/charts/frontend/Chart.yaml: name=frontend, version=0.1.0
- [ ] T017 [P] [US1] Create backend subchart Chart.yaml in charts/todo-chatbot/charts/backend/Chart.yaml: name=backend, version=0.1.0
- [ ] T018 [P] [US1] Create frontend subchart values.yaml in charts/todo-chatbot/charts/frontend/values.yaml per helm-values-contract.md (frontend section)
- [ ] T019 [P] [US1] Create backend subchart values.yaml in charts/todo-chatbot/charts/backend/values.yaml per helm-values-contract.md (backend section)
- [ ] T020 [US1] Create umbrella chart values.yaml in charts/todo-chatbot/values.yaml with frontend and backend overrides per helm-values-contract.md
- [ ] T021 [P] [US1] Create frontend _helpers.tpl in charts/todo-chatbot/charts/frontend/templates/_helpers.tpl with app.kubernetes.io/* label helpers and fullname helper
- [ ] T022 [P] [US1] Create backend _helpers.tpl in charts/todo-chatbot/charts/backend/templates/_helpers.tpl with app.kubernetes.io/* label helpers and fullname helper
- [ ] T023 [P] [US1] Create frontend ConfigMap template in charts/todo-chatbot/charts/frontend/templates/configmap.yaml: inject config values (BACKEND_URL, BETTER_AUTH_URL) from values.yaml
- [ ] T024 [P] [US1] Create backend ConfigMap template in charts/todo-chatbot/charts/backend/templates/configmap.yaml: inject config values (LLM_PROVIDER, RATE_LIMIT_DEFAULT, ACCESS_TOKEN_EXPIRE_MINUTES, BETTER_AUTH_URL) from values.yaml
- [ ] T025 [P] [US1] Create frontend Secret template in charts/todo-chatbot/charts/frontend/templates/secret.yaml: inject secrets (BETTER_AUTH_SECRET, DATABASE_URL, DATABASE_URL_NEON) from values.yaml with base64 encoding
- [ ] T026 [P] [US1] Create backend Secret template in charts/todo-chatbot/charts/backend/templates/secret.yaml: inject secrets (DATABASE_URL, DATABASE_URL_NEON, BETTER_AUTH_SECRET, OPENAI_API_KEY, GROQ_API_KEY, GEMINI_API_KEY) from values.yaml with base64 encoding
- [ ] T027 [US1] Create frontend Deployment template in charts/todo-chatbot/charts/frontend/templates/deployment.yaml: 2 replicas, image todo-frontend:1.0.0, imagePullPolicy Never, port 3000, resource requests/limits per data-model.md, liveness probe GET / delay 10s period 15s, readiness probe GET / delay 5s period 10s, envFrom ConfigMap and Secret references
- [ ] T028 [US1] Create backend Deployment template in charts/todo-chatbot/charts/backend/templates/deployment.yaml: 1 replica, image todo-backend:1.0.0, imagePullPolicy Never, port 8001, resource requests/limits per data-model.md, liveness probe GET /health delay 15s period 20s, readiness probe GET /health delay 10s period 10s, envFrom ConfigMap and Secret references
- [ ] T029 [P] [US1] Create frontend Service template in charts/todo-chatbot/charts/frontend/templates/service.yaml: type NodePort, port 80, targetPort 3000, selector matching deployment labels
- [ ] T030 [P] [US1] Create backend Service template in charts/todo-chatbot/charts/backend/templates/service.yaml: type ClusterIP, port 8001, targetPort 8001, selector matching deployment labels
- [ ] T031 [US1] Create NOTES.txt in charts/todo-chatbot/templates/NOTES.txt: post-install instructions showing how to access the frontend via `minikube service` and check pod status
- [ ] T032 [US1] Validate Helm chart: run `helm lint charts/todo-chatbot` — fix all warnings and errors until lint passes clean
- [ ] T033 [US1] Dry-run deployment: run `helm install todo-chatbot ./charts/todo-chatbot --dry-run --debug` — verify rendered manifests match data-model.md specifications
- [ ] T034 [US1] Deploy to Minikube: run `helm install todo-chatbot ./charts/todo-chatbot --set backend.secrets.GROQ_API_KEY=<key> --set backend.secrets.DATABASE_URL=<url> --set backend.secrets.BETTER_AUTH_SECRET=<secret>` — verify all pods reach Running state within 120s
- [ ] T035 [US1] Verify Helm uninstall: run `helm uninstall todo-chatbot` — verify all resources removed, run `kubectl get all` to confirm no orphaned objects
- [ ] T036 [US1] Re-deploy and verify values override: run `helm install todo-chatbot ./charts/todo-chatbot --set frontend.replicaCount=3` — verify 3 frontend pods are created, then uninstall

**Checkpoint**: US1 complete. Single `helm install` deploys the full system. Uninstall cleans up. Value overrides work. MVP achieved.

---

## Phase 4: User Story 2 — Access Services via Minikube (Priority: P2)

**Goal**: Verify and document that deployed services are reachable through Minikube networking — frontend externally, backend internally via Service DNS.

**Independent Test**: Run `minikube service todo-frontend --url`, open in browser. Confirm frontend loads and can communicate with backend.

### Implementation

- [ ] T037 [US2] Deploy the system with Helm (if not already deployed from Phase 3) using `helm install todo-chatbot ./charts/todo-chatbot` with required secrets
- [ ] T038 [US2] Access frontend via Minikube: run `minikube service todo-frontend --url` — open returned URL in browser, verify frontend loads
- [ ] T039 [US2] Verify frontend-to-backend communication: from the browser, trigger a backend API call (e.g., health check or task list) — verify the request routes through Kubernetes Service DNS (todo-backend:8001) and returns a valid response
- [ ] T040 [US2] Verify backend is internal-only: confirm backend Service type is ClusterIP, attempt direct external access without port-forward — verify it is NOT reachable from outside the cluster
- [ ] T041 [US2] Document access instructions: update quickstart.md in specs/003-cloud-native-todo-deploy/quickstart.md with verified access commands and any Minikube-specific notes discovered during testing

**Checkpoint**: US2 complete. Frontend accessible via browser through Minikube. Backend internal-only. Frontend-to-backend communication works over Service DNS.

---

## Phase 5: User Story 3 — Observe and Manage Pods (Priority: P3)

**Goal**: Verify pod observability — status, logs, and self-healing — using standard kubectl commands.

**Independent Test**: Run `kubectl get pods` to see all pods Running. Run `kubectl logs` to see application output. Delete a pod and verify Kubernetes recreates it.

### Implementation

- [ ] T042 [US3] Verify pod status: run `kubectl get pods` — confirm frontend shows 2/2 Running pods and backend shows 1/1 Running pod
- [ ] T043 [US3] Verify pod logs: run `kubectl logs -l app.kubernetes.io/name=frontend` and `kubectl logs -l app.kubernetes.io/name=backend` — confirm application startup messages are visible
- [ ] T044 [US3] Verify pod self-healing: run `kubectl delete pod -l app.kubernetes.io/name=frontend --wait=false` — watch with `kubectl get pods -w` and confirm replacement pod reaches Running state within 60 seconds
- [ ] T045 [US3] Verify pod details: run `kubectl describe pod -l app.kubernetes.io/name=backend` — confirm resource requests/limits, probe configuration, and environment variables match data-model.md specifications
- [ ] T046 [US3] Document observability commands: add verified kubectl commands to quickstart.md in specs/003-cloud-native-todo-deploy/quickstart.md under the "Verify Health" section

**Checkpoint**: US3 complete. All pods observable, logs accessible, self-healing verified. All 4 user stories satisfied.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and reproducibility verification.

- [ ] T047 Run full reproducibility test: `helm uninstall todo-chatbot`, `minikube delete`, `minikube start --driver=docker --cpus=2 --memory=4096`, rebuild images, reload into Minikube, `helm install` — verify entire pipeline works from scratch with zero manual steps
- [ ] T048 [P] Verify all infrastructure artifacts are committed: Dockerfiles, .dockerignore files, Helm chart directory, all templates — run `git status` and ensure nothing is untracked
- [ ] T049 [P] Validate quickstart.md end-to-end: follow specs/003-cloud-native-todo-deploy/quickstart.md step by step on a fresh Minikube — confirm all commands work as documented
- [ ] T050 Final Helm lint and dry-run: run `helm lint charts/todo-chatbot` and `helm install todo-chatbot ./charts/todo-chatbot --dry-run --debug` one final time to confirm clean state
- [ ] T051 Optimize resources using kagent: run kagent to analyze deployed workloads and suggest resource tuning (CPU/memory requests and limits) — apply recommendations to values.yaml if improvements found

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational / US4 (Phase 2)**: Depends on Setup (Phase 1) — BLOCKS all other user stories
- **US1 (Phase 3)**: Depends on Phase 2 (images must be built and loaded)
- **US2 (Phase 4)**: Depends on Phase 3 (system must be deployed via Helm)
- **US3 (Phase 5)**: Depends on Phase 3 (pods must be running to observe)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 4 (P4)** — Containerization: Foundational. No dependencies on other stories. BLOCKS US1, US2, US3.
- **User Story 1 (P1)** — Helm Deploy: Depends on US4 (images exist). BLOCKS US2, US3.
- **User Story 2 (P2)** — Service Access: Depends on US1 (system deployed). Can run in parallel with US3.
- **User Story 3 (P3)** — Pod Observability: Depends on US1 (pods running). Can run in parallel with US2.

### Within Each Phase

- Tasks marked [P] can run in parallel
- Sequential tasks depend on prior tasks in the same phase
- Commit after each task or logical group

### Parallel Opportunities

- Phase 1: T002, T003, T004, T005 can all run in parallel (different files)
- Phase 2: T007+T008+T009 (frontend) and T010+T011+T012 (backend) are sequential within each track but the two tracks can run in parallel
- Phase 3: T016+T017, T018+T019, T021+T022, T023+T024, T025+T026, T029+T030 are parallel pairs (frontend/backend variants)
- Phase 4 and Phase 5: US2 and US3 can run in parallel after US1 is complete

---

## Parallel Example: Phase 1

```bash
# Launch all source code prep tasks in parallel (different files):
Task: "Add output: standalone to frontend/next.config.mjs"
Task: "Add /health endpoint to backend/src/main.py"
Task: "Create frontend/.dockerignore"
Task: "Create backend/.dockerignore"
```

## Parallel Example: Phase 3 (US1)

```bash
# Launch frontend/backend subchart pairs in parallel:
Task: "Create frontend Chart.yaml"    Task: "Create backend Chart.yaml"
Task: "Create frontend values.yaml"   Task: "Create backend values.yaml"
Task: "Create frontend _helpers.tpl"  Task: "Create backend _helpers.tpl"
Task: "Create frontend configmap.yaml" Task: "Create backend configmap.yaml"
Task: "Create frontend secret.yaml"   Task: "Create backend secret.yaml"
Task: "Create frontend service.yaml"  Task: "Create backend service.yaml"
```

---

## Implementation Strategy

### MVP First (US4 + US1)

1. Complete Phase 1: Setup (source code prep)
2. Complete Phase 2: Containerize with Docker AI (US4)
3. Complete Phase 3: Helm chart + deploy (US1)
4. **STOP and VALIDATE**: `helm install` works, pods Running, `helm uninstall` clean
5. MVP achieved — system deploys with one command

### Incremental Delivery

1. Setup + US4 (containerization) → Images build and load
2. Add US1 (Helm deploy) → Single-command deploy works (MVP!)
3. Add US2 (service access) → Browser access verified
4. Add US3 (observability) → kubectl monitoring verified
5. Polish → Full reproducibility confirmed

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US4 is spec-priority P4 but execution-priority first (foundational dependency)
- AI tool commands (Gordon, kubectl-ai, kagent) are illustrative — actual commands may vary based on tool version
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
