# Implementation Plan: In-Memory Python Console Todo App

**Branch**: `001-console-todo` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a deterministic, in-memory console todo application with clean modular architecture. The application provides five core commands (add, delete, update, view, complete) with framed console UI, ANSI color support, and immediate feedback. Phase I focuses on single-session, ephemeral storage with no persistence, following constitution principles of continuity, transparency, and human-first UX.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: None (standard library only - per spec constraints)
**Storage**: In-memory (dict/list data structures) - no files or databases
**Testing**: pytest (unit and integration tests)
**Target Platform**: Any platform supporting Python 3.11+ (Linux, macOS, Windows, WSL)
**Project Type**: single (CLI application with modular source structure)
**Performance Goals**: Startup <1 second, view command output <100ms, command operations <1 second
**Constraints**: <100MB memory, no background threads, synchronous execution only
**Scale/Scope**: Single session, unlimited tasks within memory limits (no persistence)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Constitution Compliance - PASS

| Principle | Verification | Status | Notes |
|-----------|-------------|--------|--------|
| **Continuity** | Core commands must be valid across phases | PASS | Commands (add, delete, update, view, complete) designed for future extensibility to Phase II (persistence) without breaking semantics |
| **Transparency** | State transitions must be visible and explainable | PASS | Every command produces explicit confirmation or error messages showing what changed and why |
| **Determinism** | Same input produces same result within phase | PASS | No randomness in task ordering (sequential IDs, first-in-first-displayed), no async operations |
| **Human-First UX** | Console clarity before automation | PASS | CLI remains primary interface, framed UI with clear status markers `[ ]` and `[✔]` |
| **Progressive Enhancement** | Each phase adds capability, not complexity | PASS | Phase I (in-memory) designed to degrade gracefully when persistence is absent |

### Command Philosophy Compliance - PASS

| Requirement | Verification | Status |
|-------------|-------------|--------|
| Intent-expressing commands | Commands express "what" not "how" | PASS - `add <description>`, `delete <id>`, `update <id> <description>`, `complete <id>`, `view` |
| No hidden side effects | Every side effect must be explicit | PASS - Add/Delete/Update/Complete all show confirmation messages |
| Reversible or auditable | Commands reversible or fully auditable | PASS - Not reversible (no persistence), but operations display confirmation (auditable) |
| Explanatory errors | Errors explain cause and resolution | PASS - FR-009 and FR-010 require clear error messages |

### Task Invariants Compliance - PASS

| Invariant | Verification | Status |
|-----------|-------------|--------|
| Unique identity per task | Sequential IDs (1, 2, 3...) starting each session | PASS - FR-014 |
| Single phase-state at a time | Pending or completed status (no in_progress) | PASS - Status markers: `[ ]` pending, `[✔]` completed |
| Task history append-only | Historical state transitions preserved | PASS - Not applicable to Phase I (no persistence), but design allows future extension |
| Completed tasks immutable | Completed tasks cannot be modified | PASS - FR-013 (no delete/update on completed task - to be validated in implementation) |

### Phase I Standards Compliance - PASS

| Standard | Verification | Status |
|----------|-------------|--------|
| Startup instantaneous (<1 sec) | Application must start immediately | PASS - Technical context: synchronous, no async complexity |
| Exit clears all state | No persistence guarantees | PASS - FR-012: in-memory only, no files/DB |
| ANSI-based UI with fallback | Color support with graceful degradation | PASS - FR-011: ANSI with terminal detection |
| No background threads | Synchronous execution only | PASS - Technical context: synchronous CLI |

**GATE RESULT**: ✅ PASS - No constitution violations identified. Proceeding to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py              # Task entity with dataclass or similar
├── services/
│   ├── store.py             # In-memory task repository with CRUD operations
│   └── validator.py         # Input validation (non-empty descriptions, valid IDs)
├── commands/
│   ├── add.py              # Add task command handler
│   ├── delete.py           # Delete task command handler
│   ├── update.py           # Update task command handler
│   ├── complete.py          # Mark task complete command handler
│   └── view.py             # View tasks command handler (with optional filtering)
├── ui/
│   ├── renderer.py          # Console rendering with ANSI color and framing
│   └── formatter.py         # Task list formatting within frame boundaries
├── app.py                  # Entry point and command router
└── cli.py                  # Command-line argument parsing

tests/
├── unit/
│   ├── test_task.py        # Task entity tests
│   ├── test_store.py       # TaskStore CRUD tests
│   ├── test_validator.py   # Validation logic tests
│   └── test_renderer.py    # UI rendering tests
└── integration/
    └── test_app.py         # End-to-end command workflow tests
```

**Structure Decision**: Single project structure with modular separation of concerns. `models/` contains data entities, `services/` contains business logic, `commands/` contains command handlers, `ui/` contains presentation logic, and `app.py` orchestrates everything. This follows clean architecture principles and aligns with constitution requirements for modular, testable code.

## Complexity Tracking

> No constitution violations detected. This table is not required.

