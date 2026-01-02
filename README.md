# In-Memory Python Console Todo App

A deterministic, in-memory console todo application with clean modular architecture and spec-driven development.

## Features

- ✅ Add tasks with title and description
- ✅ Toggle tasks between complete/incomplete status
- ✅ Delete tasks
- ✅ Update task title and description
- ✅ View all tasks or filter by status (pending/completed)
- ✅ Framed console UI with ANSI color support
- ✅ ASCII fallback for terminals without Unicode support
- ✅ Clean, modular Python code (standard library only)

## Requirements

- Python 3.11+
- No external dependencies (standard library only)

## Installation

```bash
cd "C:\Users\shoai\Desktop\TODO app"
```

No additional installation required!

## Usage

### Interactive Menu Interface

The application provides an interactive menu-driven interface. Simply run:

```bash
python src/app.py
```

You'll be greeted with:

```
Welcome to TODO Application!

============================================================
                      TODO Application
============================================================
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit
============================================================
Enter your choice (1-7):
```

**Features:**
- **Option 1 - Add Task**: Enter title and description for a new task
- **Option 2 - View All Tasks**: Display all tasks with their status
- **Option 3 - Update Task**: Modify an existing task's title and description
- **Option 4 - Delete Task**: Remove a task by ID
- **Option 5 - Mark Task Complete**: Mark a pending task as completed
- **Option 6 - Mark Task Incomplete**: Mark a completed task back to pending
- **Option 7 - Exit**: Close the application

**Note**: Since this is Phase I (in-memory only), tasks are NOT persisted when you exit the application.

### Test Scripts

**Automated Integration Test:**
```bash
python test_todo.py
```
This demonstrates programmatic usage of all features:
- Adding multiple tasks with title and description
- Viewing all tasks
- Toggling task completion status
- Filtering by status (pending/completed)
- Updating task title and description
- Deleting tasks
- Error handling

**Interactive Demo Test:**
```bash
python test_interactive.py
```
This simulates user interaction with the menu system to demonstrate the interactive interface.

## Project Structure

```
src/
├── models/
│   ├── __init__.py
│   └── task.py              # Task entity with dataclass
├── services/
│   ├── __init__.py
│   ├── store.py             # In-memory task repository with CRUD operations
│   └── validator.py         # Input validation
├── commands/
│   ├── __init__.py
│   ├── add.py              # Add task command handler
│   ├── delete.py           # Delete task command handler
│   ├── update.py           # Update task command handler
│   ├── complete.py          # Mark task complete command handler
│   └── view.py             # View tasks command handler
├── ui/
│   ├── __init__.py
│   └── renderer.py          # Console rendering with ANSI color and framing
└── app.py                  # Entry point and command router

tests/
├── unit/                   # Unit tests
└── integration/            # Integration tests

test_todo.py                # Comprehensive test script
```

## Design Principles

This application follows constitution-based design:

- **Continuity**: Commands will remain valid across future phases (Phase II: Persistence, Phase III: AI, etc.)
- **Transparency**: All state transitions are visible with explicit confirmation messages
- **Determinism**: Same input produces same result within a session
- **Human-First UX**: CLI remains the primary interface with clear, framed output
- **Progressive Enhancement**: In-memory design will extend to persistence without breaking changes

## Task Invariants

1. Every task has a unique identity (sequential IDs starting at 1)
2. Every task exists in exactly one phase-state (pending or completed)
3. Task history is append-only (deferred to Phase II with persistence)
4. Completed tasks are immutable (cannot be updated)

## Success Criteria (Phase I)

- ✅ SC-001: Users can add their first task in under 1 second
- ✅ SC-002: View command outputs in under 100ms
- ✅ SC-003: Task completion happens in under 1 second
- ✅ SC-004: Task state visually distinguishable (`[ ]` vs `[X]`)
- ✅ SC-005: Simple, intuitive CLI commands
- ✅ SC-006: Readable output on all terminals (Unicode and ASCII fallback)
- ✅ SC-007: Instantaneous application startup
- ✅ SC-008: Clean termination with state cleared
- ✅ SC-009: Explanatory error messages

## Future Phases

- **Phase II**: Persistent storage with SQLModel, RESTful API via FastAPI, Web UI via Next.js
- **Phase III**: AI-powered todo agent with conversational task creation
- **Phase IV**: Local Kubernetes deployment
- **Phase V**: Advanced cloud deployment with Kafka and Dapr

## License

Educational project for learning spec-driven development.
