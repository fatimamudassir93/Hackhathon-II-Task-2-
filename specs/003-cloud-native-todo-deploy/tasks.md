# Tasks: Cloud-Native TODO App Deployment

**Input**: Design documents from `/specs/003-cloud-native-todo-deploy/`
**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: No automated tests required for deployment tasks - validation through manual smoke testing

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each deployment phase.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase 4/backend/`
- **Frontend**: `phase 4/frontend/`
- **CI/CD**: `phase 4/.github/workflows/`
- **Docs**: `phase 4/docs/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare project structure and documentation for deployment

- [X] T001 Create docs/ directory for deployment documentation
- [X] T002 [P] Create .env.example in phase 4/backend/ with all required environment variables
- [X] T003 [P] Create .env.example in phase 4/frontend/ with all required environment variables
- [X] T004 [P] Update phase 4/backend/.gitignore to exclude deployment artifacts
- [X] T005 [P] Update phase 4/frontend/.gitignore to exclude deployment artifacts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify existing application works and prepare for containerization

**⚠️ CRITICAL**: No deployment work can begin until this phase is complete

- [ ] T006 Verify backend starts successfully with uvicorn src.main:app
- [ ] T007 Verify frontend starts successfully with npm run dev
- [ ] T008 Verify database connection to Neon PostgreSQL from backend
- [ ] T009 Verify authentication flow works end-to-end
- [ ] T010 Verify chat functionality works with LLM provider

**Checkpoint**: Foundation verified - containerization can now begin

---

## Phase 3: User Story 1 - Containerize Application (Priority: P1) 🎯 MVP

**Goal**: Create Docker containers for backend and frontend that run consistently across environments

**Independent Test**: Build and run containers locally with docker-compose, verify all functionality works

### Implementation for User Story 1

- [X] T011 [P] [US1] Create backend/.dockerignore with Python patterns (venv/, __pycache__/, *.pyc, .env, *.log)
- [X] T012 [P] [US1] Create frontend/.dockerignore with Node.js patterns (node_modules/, .next/, .env*, *.log)
- [X] T013 [US1] Create backend/Dockerfile with multi-stage build (builder + runtime stages)
- [X] T014 [US1] Create frontend/Dockerfile with Next.js standalone output optimization
- [X] T015 [US1] Update frontend/next.config.mjs to enable standalone output mode
- [X] T016 [US1] Create docker-compose.yml in phase 4/ for local development orchestration
- [X] T017 [US1] Create docker-compose.prod.yml in phase 4/ for production simulation
- [ ] T018 [US1] Test backend Docker build: docker build -t todo-backend ./backend
- [ ] T019 [US1] Test frontend Docker build: docker build -t todo-frontend ./frontend
- [ ] T020 [US1] Test docker-compose up and verify both services start successfully
- [ ] T021 [US1] Verify backend health endpoint accessible at http://localhost:8000/health
- [ ] T022 [US1] Verify frontend accessible at http://localhost:3000
- [ ] T023 [US1] Verify authentication works in containerized environment
- [ ] T024 [US1] Verify chat functionality works in containerized environment

**Checkpoint**: Containers built and tested locally - ready for cloud deployment

---

## Phase 4: User Story 2 - Deploy Backend to Cloud (Priority: P2)

**Goal**: Deploy FastAPI backend to Railway with proper configuration and environment variables

**Independent Test**: Access backend health endpoint via HTTPS, test API documentation at /docs

### Implementation for User Story 2

- [X] T025 [P] [US2] Create backend/railway.json with build and deploy configuration
- [X] T026 [P] [US2] Create backend/render.yaml as alternative deployment configuration
- [X] T027 [US2] Update backend/src/main.py to read PORT from environment variable
- [X] T028 [US2] Update backend CORS configuration to accept FRONTEND_URL from environment
- [ ] T029 [US2] Create Railway project and connect GitHub repository
- [ ] T030 [US2] Configure Railway environment variables (DATABASE_URL, BETTER_AUTH_SECRET, LLM_PROVIDER, GROQ_API_KEY)
- [ ] T031 [US2] Set Railway root directory to backend/
- [ ] T032 [US2] Deploy backend to Railway from main branch
- [ ] T033 [US2] Verify Railway deployment health check passes
- [ ] T034 [US2] Test backend health endpoint via Railway URL
- [ ] T035 [US2] Test API documentation accessible at Railway URL/docs
- [ ] T036 [US2] Test authentication endpoints (signup, signin) via Railway URL
- [ ] T037 [US2] Verify database connection from Railway to Neon PostgreSQL
- [ ] T038 [US2] Document Railway backend URL in docs/DEPLOYMENT.md

**Checkpoint**: Backend deployed and accessible via HTTPS - ready for frontend integration

---

## Phase 5: User Story 3 - Deploy Frontend to Vercel (Priority: P3)

**Goal**: Deploy Next.js frontend to Vercel with proper backend integration

**Independent Test**: Access frontend via Vercel URL, test authentication and chat functionality

### Implementation for User Story 3

- [X] T039 [P] [US3] Create frontend/vercel.json with build and environment configuration
- [ ] T040 [US3] Update frontend environment to use BACKEND_URL for API calls
- [ ] T041 [US3] Import GitHub repository to Vercel
- [ ] T042 [US3] Set Vercel framework preset to Next.js
- [ ] T043 [US3] Set Vercel root directory to frontend/
- [ ] T044 [US3] Configure Vercel environment variables (BACKEND_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL)
- [ ] T045 [US3] Deploy frontend to Vercel from main branch
- [ ] T046 [US3] Verify Vercel deployment succeeds
- [ ] T047 [US3] Test frontend accessible via Vercel URL
- [ ] T048 [US3] Test authentication flow (signup, signin, session) on Vercel
- [ ] T049 [US3] Test task CRUD operations via Vercel frontend
- [ ] T050 [US3] Test chat interface functionality via Vercel frontend
- [ ] T051 [US3] Verify CORS working between Vercel frontend and Railway backend
- [ ] T052 [US3] Update Railway FRONTEND_URL environment variable with Vercel URL
- [ ] T053 [US3] Document Vercel frontend URL in docs/DEPLOYMENT.md

**Checkpoint**: Frontend deployed and fully functional - application accessible publicly

---

## Phase 6: User Story 4 - Configure CI/CD Pipeline (Priority: P4)

**Goal**: Automate deployment on git push with testing and notifications

**Independent Test**: Push code change, verify automated deployment succeeds

### Implementation for User Story 4

- [X] T054 [US4] Create .github/workflows/ directory in phase 4/
- [X] T055 [P] [US4] Create .github/workflows/backend-test.yml for backend testing
- [X] T056 [P] [US4] Create .github/workflows/backend-deploy.yml for Railway deployment
- [ ] T057 [US4] Configure GitHub secrets for RAILWAY_TOKEN
- [ ] T058 [US4] Test backend-test.yml workflow by pushing to test branch
- [ ] T059 [US4] Test backend-deploy.yml workflow by pushing to main branch
- [ ] T060 [US4] Verify Vercel auto-deployment configured for frontend
- [ ] T061 [US4] Test Vercel auto-deployment by pushing frontend change
- [ ] T062 [US4] Configure deployment notifications (optional)
- [ ] T063 [US4] Document CI/CD workflow in docs/DEPLOYMENT.md

**Checkpoint**: CI/CD pipeline functional - deployments automated

---

## Phase 7: User Story 5 - Add Monitoring and Logging (Priority: P5)

**Goal**: Configure monitoring, logging, and alerting for production application

**Independent Test**: Trigger error, verify it appears in logs and monitoring

### Implementation for User Story 5

- [ ] T064 [P] [US5] Configure structured logging in backend/src/main.py
- [ ] T065 [P] [US5] Add request/response logging middleware to backend
- [ ] T066 [US5] Configure Railway logging and metrics dashboard
- [ ] T067 [US5] Configure Vercel Analytics for frontend
- [ ] T068 [US5] Set up error tracking in backend (log errors with context)
- [ ] T069 [US5] Set up error tracking in frontend (log errors with context)
- [ ] T070 [US5] Configure uptime monitoring for backend health endpoint
- [ ] T071 [US5] Configure uptime monitoring for frontend
- [ ] T072 [US5] Test logging by triggering various operations
- [ ] T073 [US5] Test error tracking by triggering intentional errors
- [ ] T074 [US5] Document monitoring setup in docs/DEPLOYMENT.md

**Checkpoint**: Monitoring and logging active - production observability complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and final touches

- [X] T075 [P] Create docs/DEPLOYMENT.md with complete deployment guide
- [X] T076 [P] Create docs/ARCHITECTURE.md with architecture diagram and explanation
- [X] T077 [P] Create docs/TROUBLESHOOTING.md with common issues and solutions
- [X] T078 [P] Create docs/RUNBOOK.md with operational procedures
- [X] T079 Update phase 4/README.md with deployment information
- [X] T080 Create deployment checklist in docs/DEPLOYMENT_CHECKLIST.md
- [ ] T081 Perform end-to-end smoke test of production deployment
- [ ] T082 Verify all environment variables documented in .env.example files
- [ ] T083 Verify all secrets properly configured and not committed
- [ ] T084 Test rollback procedure for both backend and frontend
- [ ] T085 Document cost estimation and monitoring in docs/DEPLOYMENT.md
- [ ] T086 Create quick reference card for common deployment operations

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Containerization) must complete before US2 and US3
  - US2 (Backend Deploy) must complete before US3 (Frontend Deploy)
  - US3 (Frontend Deploy) must complete before US4 (CI/CD)
  - US4 (CI/CD) can run in parallel with US5 (Monitoring)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Containerization)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - Backend Deploy)**: Depends on US1 completion - Needs Docker images
- **User Story 3 (P3 - Frontend Deploy)**: Depends on US2 completion - Needs backend URL
- **User Story 4 (P4 - CI/CD)**: Depends on US2 and US3 completion - Needs deployment targets
- **User Story 5 (P5 - Monitoring)**: Can start after US2 and US3 - Independent of US4

### Within Each User Story

- Containerization (US1): .dockerignore files before Dockerfiles, Dockerfiles before docker-compose, testing after all files created
- Backend Deploy (US2): Configuration files before deployment, deployment before testing
- Frontend Deploy (US3): Configuration before deployment, backend URL update after deployment
- CI/CD (US4): Workflow files before secrets, testing after configuration
- Monitoring (US5): Logging before monitoring, testing after all setup

### Parallel Opportunities

- Phase 1: T002, T003, T004, T005 can run in parallel (different files)
- Phase 3 (US1): T011, T012 can run in parallel (different files)
- Phase 4 (US2): T025, T026 can run in parallel (different files)
- Phase 6 (US4): T055, T056 can run in parallel (different files)
- Phase 7 (US5): T064, T065 can run in parallel (different files)
- Phase 8: T075, T076, T077, T078 can run in parallel (different files)

---

## Parallel Example: User Story 1 (Containerization)

```bash
# Launch .dockerignore files together:
Task T011: "Create backend/.dockerignore with Python patterns"
Task T012: "Create frontend/.dockerignore with Node.js patterns"

# Then create Dockerfiles sequentially (after .dockerignore):
Task T013: "Create backend/Dockerfile with multi-stage build"
Task T014: "Create frontend/Dockerfile with Next.js standalone output"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - verify app works)
3. Complete Phase 3: User Story 1 (Containerization)
4. **STOP and VALIDATE**: Test containers locally with docker-compose
5. Verify all functionality works in containers before proceeding

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Containerization) → Test locally → Containers ready
3. Add User Story 2 (Backend Deploy) → Test independently → Backend live
4. Add User Story 3 (Frontend Deploy) → Test independently → Full app live
5. Add User Story 4 (CI/CD) → Test independently → Automation ready
6. Add User Story 5 (Monitoring) → Test independently → Observability complete
7. Each story adds value without breaking previous stories

### Sequential Deployment Strategy

Due to dependencies, deployment must be sequential:

1. Team completes Setup + Foundational together
2. Complete User Story 1 (Containerization) - Required for all deployments
3. Complete User Story 2 (Backend Deploy) - Required for frontend
4. Complete User Story 3 (Frontend Deploy) - Required for full app
5. Complete User Story 4 (CI/CD) and User Story 5 (Monitoring) in parallel
6. Complete Polish phase for documentation

---

## Validation Checkpoints

### After User Story 1 (Containerization)
- [ ] Backend container builds successfully
- [ ] Frontend container builds successfully
- [ ] docker-compose up starts both services
- [ ] Health endpoints accessible
- [ ] Authentication works in containers
- [ ] Chat functionality works in containers

### After User Story 2 (Backend Deploy)
- [ ] Backend accessible via HTTPS
- [ ] Health check passes
- [ ] API documentation accessible
- [ ] Database connection working
- [ ] Authentication endpoints working

### After User Story 3 (Frontend Deploy)
- [ ] Frontend accessible via HTTPS
- [ ] Authentication flow works
- [ ] Task CRUD operations work
- [ ] Chat interface functional
- [ ] CORS configured correctly

### After User Story 4 (CI/CD)
- [ ] Backend auto-deploys on push
- [ ] Frontend auto-deploys on push
- [ ] Tests run before deployment
- [ ] Deployment notifications working

### After User Story 5 (Monitoring)
- [ ] Logs accessible and structured
- [ ] Errors tracked and visible
- [ ] Performance metrics available
- [ ] Uptime monitoring active

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Test locally with Docker before deploying to cloud
- Verify environment variables before deployment
- Document all deployment URLs and credentials securely
- Use free tiers where possible to minimize costs

---

## Environment Variables Reference

### Backend (.env)
```
DATABASE_URL=postgresql+asyncpg://...
BETTER_AUTH_SECRET=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key
FRONTEND_URL=https://your-frontend.vercel.app
PORT=8000
```

### Frontend (.env)
```
BACKEND_URL=https://your-backend.railway.app
BETTER_AUTH_SECRET=your_secret_key
BETTER_AUTH_URL=https://your-frontend.vercel.app
DATABASE_URL=postgresql://...
```

**IMPORTANT**: Never commit .env files - use .env.example for templates
