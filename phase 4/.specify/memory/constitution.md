<!-- SYNC IMPACT REPORT
Version change: 3.0.0 → 4.0.0
Bump rationale: MAJOR — complete project scope change from AI chatbot
to infrastructure automation agent. All principles redefined for
Docker/Kubernetes/Minikube deployment automation. Technology stack,
agent role, and quality gates entirely replaced.

Modified principles:
- "Technology Binding Adherence" → "Infrastructure Toolchain Binding" (redefined)
- "Agent Architecture Compliance" → removed (replaced by Automation Agent Role)
- "Authentication Architecture Compliance" → removed (not applicable)
- "MCP Tool Contract Enforcement" → removed (replaced by CLI Reproducibility)
- "Test-First (NON-NEGOTIABLE)" → removed (replaced by Reproducibility Gate)
- "Conversation & Statelessness Rules" → "Stateless Services Mandate" (redefined)
- "Feature Scope Lock" → "Deployment Scope Lock" (redefined)
- "Spec-Driven Execution Compliance" → "Spec-Driven Execution Compliance" (retained)

Added sections:
- Automation Agent Role (new principle)
- AI-First Artifact Generation (new principle)
- CLI Reproducibility Mandate (new principle)
- Kubernetes & Helm Best Practices (new principle)
- Local-Only Deployment Constraint (new principle)

Removed sections:
- Agent Architecture Compliance (multi-agent chatbot)
- Authentication Architecture Compliance (Better Auth)
- MCP Tool Contract Enforcement (MCP tools)
- Test-First (NON-NEGOTIABLE) (TDD cycle)
- Conversation & Statelessness Rules (chat persistence)
- Frontend Rules (ChatKit UI)
- Backend Rules (FastAPI + OpenAI Agents SDK)

Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending (Constitution Check gates need infra-specific refresh)
- .specify/templates/spec-template.md ✅ no structural changes needed (generic template)
- .specify/templates/tasks-template.md ⚠ pending (task categories need infra automation phases)

Follow-up TODOs: None
-->

# Phase IV – Infrastructure Automation Constitution

## Core Principles

### I. Automation Agent Role

The system operates as an infrastructure automation agent. The
agent MUST perform all containerization, orchestration, and
deployment tasks on behalf of the user. The user MUST NOT be
required to write code manually — all Dockerfiles, Helm charts,
Kubernetes manifests, and configuration files MUST be generated
by the agent or by AI-powered CLI tools. The agent is
responsible for producing complete, runnable infrastructure
artifacts from high-level user intent.

### II. Infrastructure Toolchain Binding

The following tools are the authoritative toolchain for this
project:

| Tool | Purpose |
|------|---------|
| Docker AI (Gordon) | Dockerfile generation and container image building |
| kubectl-ai | AI-assisted Kubernetes manifest generation and cluster operations |
| kagent | Kubernetes agent for Helm chart generation and management |
| Minikube | Local Kubernetes cluster for all deployments |
| Helm | Package management for Kubernetes applications |
| Docker CLI | Image build, tag, push, and container lifecycle |
| kubectl | Cluster inspection, apply, rollout, and debugging |

Tool responsibilities MUST NOT overlap — each tool has a fixed
role. The agent MUST prefer AI-powered tools (Gordon, kubectl-ai,
kagent) over manual artifact creation whenever the tool supports
the required operation.

### III. AI-First Artifact Generation

All infrastructure artifacts MUST be generated using AI-powered
tools as the primary method:

- **Dockerfiles**: MUST be generated using Docker AI (Gordon)
  where possible. Manual Dockerfile authoring is permitted only
  when Gordon cannot produce the required output.
- **Helm Charts**: MUST be generated using kagent or kubectl-ai.
  Manual chart authoring is a fallback only.
- **Kubernetes Manifests**: MUST be generated using kubectl-ai
  for deployments, services, ingress, and config resources.

All generated artifacts MUST be reviewed for correctness before
applying. The agent MUST store generated artifacts in the
repository for version control and reproducibility.

### IV. CLI Reproducibility Mandate

Every action the agent performs MUST be expressible as a
reproducible CLI command. The agent MUST output the exact
commands used so the user can re-execute them independently.
No action may depend on hidden state, GUI interaction, or
manual steps. The complete deployment pipeline MUST be
reproducible by running the documented commands in sequence
on a fresh Minikube cluster.

### V. Local-Only Deployment Constraint

All deployments MUST target a local Minikube cluster. Cloud
provider APIs (AWS, GCP, Azure), remote registries (unless
explicitly approved), and external cluster endpoints are
PROHIBITED. The Minikube cluster is the single deployment
target. Container images MUST be built and loaded into
Minikube's local Docker daemon or registry. No cloud-specific
constructs (LoadBalancer with external IP, cloud storage
classes, IAM roles) are permitted.

### VI. Stateless Services Mandate

All deployed services MUST be stateless. Application state
MUST NOT be stored in-container — containers MUST be
ephemeral and replaceable. If persistence is required, it
MUST be handled by external volumes or database services
declared explicitly in the spec. Session affinity and sticky
sessions are PROHIBITED unless explicitly approved. Services
MUST survive pod restarts and rescheduling without data loss
or user impact.

### VII. Service Separation Requirement

The application MUST be deployed as separate frontend and
backend services. Each service MUST have its own:

- Dockerfile (generated via Docker AI / Gordon)
- Helm chart or Kubernetes deployment manifest
- Kubernetes Service resource
- Independent scaling configuration

Frontend and backend MUST communicate over well-defined
network boundaries (Kubernetes Service DNS). Monolithic
single-container deployments combining frontend and backend
are PROHIBITED.

### VIII. Kubernetes & Helm Best Practices

All Kubernetes resources MUST follow established best
practices:

- Deployments MUST specify resource requests and limits
- Services MUST use ClusterIP type (NodePort only for
  Minikube external access)
- ConfigMaps and Secrets MUST be used for configuration —
  no hardcoded values in manifests
- Health checks (liveness and readiness probes) MUST be
  defined for all containers
- Labels and selectors MUST follow the
  `app.kubernetes.io/*` convention
- Helm charts MUST use `values.yaml` for all configurable
  parameters
- Namespace isolation SHOULD be used for environment
  separation

### IX. Deployment Scope Lock

Implementation is restricted to:

- Dockerfile generation for frontend and backend services
- Helm chart creation for packaging and deployment
- Kubernetes manifest generation (Deployment, Service,
  ConfigMap, Secret, Ingress)
- Minikube cluster setup and configuration
- Container image building and loading into Minikube
- Service-to-service networking within the cluster
- Health check and readiness probe configuration

Prohibited:

- Cloud provider deployments or integrations
- CI/CD pipeline configuration (Jenkins, GitHub Actions, etc.)
- Monitoring stack deployment (Prometheus, Grafana, etc.)
- Service mesh installation (Istio, Linkerd, etc.)
- Multi-cluster federation
- Custom operators or CRDs
- Persistent volume provisioning beyond Minikube defaults

No scope creep allowed without explicit spec update.

### X. Spec-Driven Execution Compliance

MUST read specs before implementation, reference specs
explicitly. If requirement is missing or unclear, STOP and
request spec update. Do NOT invent Kubernetes configurations,
Helm values, Docker build arguments, or service topologies.
Specs and this constitution are the single source of truth.
Infrastructure definitions in `/specs` are authoritative.

## Automation Rules

### Docker AI (Gordon) Usage

- Use Gordon to generate Dockerfiles for each service
- Review generated Dockerfiles for multi-stage build
  efficiency, security (non-root user), and minimal image
  size
- Tag images with version identifiers, not `latest` alone
- Build context MUST be scoped to the service directory

### kubectl-ai & kagent Usage

- Use kubectl-ai for generating Kubernetes manifests from
  natural language descriptions
- Use kagent for Helm chart scaffolding and management
- All generated manifests MUST be saved to the repository
  before applying
- `kubectl apply` MUST use declarative mode (`-f` with
  manifest files), not imperative commands

### Minikube Operations

- Start Minikube with documented driver and resource
  configuration
- Use `minikube image load` or `eval $(minikube docker-env)`
  for local image access
- Use `minikube service` or `minikube tunnel` for accessing
  services externally
- Document Minikube prerequisites (driver, CPU, memory) in
  the quickstart

## Quality Gates (Mandatory)

Before completion, verify:

- All CLI commands are documented and reproducible
- Dockerfiles build successfully without errors
- Container images load into Minikube's local registry
- Helm charts lint without warnings (`helm lint`)
- Kubernetes manifests validate (`kubectl apply --dry-run=client`)
- All pods reach Running state with healthy probes
- Frontend and backend services are independently accessible
- Frontend can reach backend over Kubernetes Service DNS
- No cloud-specific resources or external dependencies
- All secrets and config use ConfigMap/Secret resources
- Services restart cleanly (delete pod, verify recovery)

Failure at any gate invalidates the deployment and requires
spec refinement.

## Governance

This constitution supersedes all other practices for Phase IV.
All infrastructure artifacts MUST be AI-generated where tools
support it. All manifests MUST be version-controlled. Code
reviews MUST verify compliance with the toolchain binding and
reproducibility mandates. Complexity MUST be justified with
explicit reference to this constitution. Use Spec-Kit Plus
for runtime development guidance.

**Version**: 4.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
