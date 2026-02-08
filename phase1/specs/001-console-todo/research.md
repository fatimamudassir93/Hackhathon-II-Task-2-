# Research: In-Memory Python Console Todo App

**Purpose**: Document technical decisions for Phase I (In-Memory Console) implementation
**Date**: 2026-01-01
**Feature**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Decision 1: Python Version

**Decision**: Python 3.11
**Rationale**: Latest stable release at time of planning with strong type hints support (Python 3.10+) for clean, testable code. Aligns with constitution requirement for modular, standard library-only dependencies.
**Alternatives considered**:
- Python 3.9: Rejected - Lacks type hint improvements in 3.10+
- Python 3.12 (latest): Rejected - Not necessary for Phase I scope, 3.11 provides good balance of features and stability

## Decision 2: Storage Strategy

**Decision**: In-memory storage using Python `dict` and `list` data structures
**Rationale**: Per spec constraints (FR-012), Phase I requires no persistence. `dict` provides O(1) lookups by task ID for delete/update/complete operations. `list` maintains insertion order for view operations. Both are standard library types with zero external dependencies.
**Alternatives considered**:
- `sqlite3` (built-in): Rejected - Violates "no files or DB" constraint, adds persistence
- Custom classes for TaskStore: Rejected - Over-engineering, `dict` provides sufficient abstraction
- `collections.OrderedDict`: Rejected - Python 3.7+ `dict` maintains insertion order naturally

## Decision 3: Testing Framework

**Decision**: pytest
**Rationale**: Industry standard for Python testing with excellent fixtures, parameterized tests, and assertions. Supports both unit and integration testing patterns. Minimal learning curve for target audience (developers learning CLI design).
**Alternatives considered**:
- `unittest` (built-in): Rejected - More verbose, lacks modern features like fixtures
- `unittest.mock`: Rejected - Overkill for synchronous, in-memory operations

## Decision 4: Console UI and ANSI Color

**Decision**: ANSI color codes with terminal capability detection for graceful fallback
**Rationale**: Per spec (FR-011), system must support color with fallback for unsupported terminals. Use `colorama` or `sys.stdout.isatty()` detection. Frame task lists with ASCII box-drawing characters (Unicode box-drawing for better terminals, fallback to ASCII).
**Alternatives considered**:
- `curses` or `urwid`: Rejected - External library dependency (violates constraint), adds complexity for simple framed UI
- No color: Rejected - Fails FR-011 requirement for "minimal, meaningful color"

## Decision 5: Command Pattern

**Decision**: Simple verb-based commands: `add <description>`, `delete <id>`, `update <id> <description>`, `complete <id>`, `view` (with optional `--pending` or `--completed` flags)
**Rationale**: Aligns with constitution "intent-expressing commands" principle. Clear, intuitive for target audience. Maps directly to user stories (US1-US5).
**Alternatives considered**:
- Interactive menu-driven: Rejected - Fails "CLI clarity before automation" principle, reduces determinism
- Complex command syntax (e.g., `task add --desc "..."): Rejected - Adds unnecessary ceremony

## Decision 6: Error Handling Pattern

**Decision**: Explicit exceptions with user-friendly messages explaining cause and resolution
**Rationale**: Aligns with constitution "explanatory errors" requirement. Each command handler validates inputs and raises domain-specific exceptions that are caught at top level and rendered as user messages.
**Alternatives considered**:
- Silent failures: Rejected - Violates transparency principle
- Stack traces to user: Rejected - Not user-friendly, internal implementation detail leakage

## Decision 7: Module Organization

**Decision**: Separation of concerns: `models/`, `services/`, `commands/`, `ui/`, `app.py`
**Rationale**: Follows clean architecture principles. Each module has single responsibility. Testable in isolation. Satisfies spec assumption for "clean, modular Python code" organized by concern.
**Alternatives considered**:
- Monolithic single file: Rejected - Violates modular code requirement, harder to test
- Framework-based (e.g., `click` or `typer` CLI framework): Rejected - External dependency, adds abstraction layer not needed for Phase I

## Decision 8: Task Identifier Strategy

**Decision**: Sequential integers starting at 1 for each session
**Rationale**: Aligns with spec (FR-014) for deterministic ordering. Simple to understand (1, 2, 3...). Supports O(1) lookups in dict storage.
**Alternatives considered**:
- UUIDs: Rejected - Over-engineering, not user-friendly for CLI
- Time-based IDs: Rejected - Not sequential, harder to reference by user

## Decision 9: Text Overflow Handling

**Decision**: Word-wrap with frame width detection, truncate if necessary
**Rationale**: Per spec (FR-017), must handle descriptions exceeding console frame width. Use Python's `textwrap` module with configurable width (default 76 chars for 80-column terminal minus frame padding).
**Alternatives considered**:
- Hard truncation: Rejected - Cuts off critical information
- Horizontal scrolling: Rejected - Not feasible in CLI environment

## Decision 10: Execution Model

**Decision**: Synchronous, single-process execution with no background threads
**Rationale**: Aligns with Phase I standards (no background threads or async complexity). Deterministic behavior (constitution determinism principle). Simpler testing and debugging.
**Alternatives considered**:
- Async (`asyncio`): Rejected - Adds complexity not needed for in-memory operations, violates "no async complexity"
- Multi-threading: Rejected - Violates Phase I standards, introduces race conditions on mutable state

## Summary

All technical decisions made with rationale documented. No NEEDS CLARIFICATION items remaining. Architecture is ready for Phase 1 design (data-model, contracts, quickstart).

**Constitution Alignment**:
- ✅ Continuity: Commands designed for future extensibility
- ✅ Transparency: Every operation produces explicit feedback
- ✅ Determinism: No randomness, sequential IDs
- ✅ Human-First UX: Simple CLI commands, framed UI
- ✅ Progressive Enhancement: Modular design supports Phase II persistence without breaking changes
