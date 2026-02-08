---
id: 3
title: Phase IV Infrastructure Automation Constitution
stage: constitution
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: 002-todo-ai-chatbot
user: shoai
command: /sp.constitution
labels: ["constitution", "phase4", "infrastructure", "docker", "kubernetes", "minikube"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

sp.constitution:

You are an infrastructure automation agent.

Rules:
- No manual coding by the user.
- Use Docker AI (Gordon) for containerization where possible.
- Use kubectl-ai and kagent for Kubernetes and Helm operations.
- Target environment is local Minikube only.
- Follow Kubernetes and Helm best practices.
- Prefer AI-generated Dockerfiles and Helm charts.
- Output must be reproducible using CLI commands.

Constraints:
- Local-only deployment (no cloud).
- Stateless services.
- Use separate frontend and backend services.

## Response snapshot

Amended constitution from v3.0.0 (Phase III - AI Chatbot) to v4.0.0 (Phase IV - Infrastructure Automation). MAJOR version bump due to complete project scope change. Defined 10 core principles: Automation Agent Role, Infrastructure Toolchain Binding, AI-First Artifact Generation, CLI Reproducibility Mandate, Local-Only Deployment Constraint, Stateless Services Mandate, Service Separation Requirement, Kubernetes & Helm Best Practices, Deployment Scope Lock, and Spec-Driven Execution Compliance. Added automation rules for Docker AI (Gordon), kubectl-ai/kagent, and Minikube operations. Replaced chatbot-specific quality gates with infrastructure deployment gates.

## Outcome

- ✅ Impact: Constitution fully rewritten for Phase IV infrastructure automation scope
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (overwritten)
- 🔁 Next prompts: /sp.specify to create feature spec for infrastructure deployment, update plan/tasks templates for infra phases
- 🧠 Reflection: Clean separation from Phase III. All 10 principles are declarative and testable. Toolchain table provides clear responsibility boundaries.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation PASS — no unresolved placeholders, version matches report, dates in ISO format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate templates (plan, tasks) alignment with new infra-specific phases
