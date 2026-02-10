"""
Unit tests for task MCP tools

Per Constitution Principle V: Test-First (NON-NEGOTIABLE)
These tests MUST pass before task tools are considered complete.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from chatbot.tools.task_tools import add_task, list_tasks, update_task, complete_task, delete_task
from chatbot.llm.agent import AgentContext


@pytest.fixture
def mock_context():
    """Create a mock context for tool execution"""
    ctx = MagicMock(spec=AgentContext)
    ctx.db_session = AsyncMock()
    ctx.user_id = "test-user-123"
    return ctx


@pytest.mark.asyncio
async def test_add_task_success(mock_context, monkeypatch):
    """Test adding a task successfully"""
    # Mock TaskService.create_task_for_user
    mock_task = MagicMock()
    mock_task.id = "task-123"
    mock_task.title = "Buy groceries"

    async def mock_create(task_data, user_id, db_session):
        return mock_task

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.create_task_for_user", mock_create)

    result = await add_task(mock_context, title="Buy groceries", description="Milk and eggs")

    assert result["task_id"] == "task-123"
    assert result["status"] == "created"
    assert result["title"] == "Buy groceries"


@pytest.mark.asyncio
async def test_add_task_empty_title(mock_context):
    """Test adding a task with empty title fails"""
    result = await add_task(mock_context, title="", description="Test")

    assert "error" in result
    assert result["error"] == "Title is required"


@pytest.mark.asyncio
async def test_list_tasks_all(mock_context, monkeypatch):
    """Test listing all tasks"""
    mock_tasks = [
        MagicMock(id="1", title="Task 1", completed=False, priority="high", due_date=None),
        MagicMock(id="2", title="Task 2", completed=True, priority="low", due_date=None),
    ]

    async def mock_get_tasks(user_id, db_session):
        return mock_tasks

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.get_tasks_by_user_id", mock_get_tasks)

    result = await list_tasks(mock_context)

    assert len(result["tasks"]) == 2
    assert result["tasks"][0]["id"] == "1"
    assert result["tasks"][1]["completed"] is True


@pytest.mark.asyncio
async def test_list_tasks_filter_pending(mock_context, monkeypatch):
    """Test listing only pending tasks"""
    mock_tasks = [
        MagicMock(id="1", title="Task 1", completed=False, priority="high", due_date=None),
        MagicMock(id="2", title="Task 2", completed=True, priority="low", due_date=None),
    ]

    async def mock_get_tasks(user_id, db_session):
        return mock_tasks

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.get_tasks_by_user_id", mock_get_tasks)

    result = await list_tasks(mock_context, status="pending")

    assert len(result["tasks"]) == 1
    assert result["tasks"][0]["completed"] is False


@pytest.mark.asyncio
async def test_update_task_success(mock_context, monkeypatch):
    """Test updating a task successfully"""
    mock_task = MagicMock()
    mock_task.id = "task-123"
    mock_task.title = "Updated title"

    async def mock_update(task_id, update_data, user_id, db_session):
        return mock_task

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.update_task_for_user", mock_update)

    result = await update_task(mock_context, task_id="task-123", title="Updated title")

    assert result["task_id"] == "task-123"
    assert result["status"] == "updated"


@pytest.mark.asyncio
async def test_update_task_not_found(mock_context, monkeypatch):
    """Test updating a non-existent task"""
    async def mock_update(task_id, update_data, user_id, db_session):
        return None

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.update_task_for_user", mock_update)

    result = await update_task(mock_context, task_id="nonexistent", title="New title")

    assert "error" in result
    assert result["error"] == "Task not found"


@pytest.mark.asyncio
async def test_complete_task_success(mock_context, monkeypatch):
    """Test completing a task successfully"""
    mock_task = MagicMock()
    mock_task.id = "task-123"
    mock_task.title = "Task to complete"

    async def mock_complete(task_id, completed, user_id, db_session):
        return mock_task

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.update_task_completion_for_user", mock_complete)

    result = await complete_task(mock_context, task_id="task-123")

    assert result["task_id"] == "task-123"
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_task_success(mock_context, monkeypatch):
    """Test deleting a task successfully"""
    async def mock_delete(task_id, user_id, db_session):
        return True

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.delete_task_for_user", mock_delete)

    result = await delete_task(mock_context, task_id="task-123")

    assert result["task_id"] == "task-123"
    assert result["status"] == "deleted"


@pytest.mark.asyncio
async def test_delete_task_not_found(mock_context, monkeypatch):
    """Test deleting a non-existent task"""
    async def mock_delete(task_id, user_id, db_session):
        return False

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.delete_task_for_user", mock_delete)

    result = await delete_task(mock_context, task_id="nonexistent")

    assert "error" in result
    assert result["error"] == "Task not found"


@pytest.mark.asyncio
async def test_user_isolation(mock_context, monkeypatch):
    """Test that all tools use the correct user_id from context"""
    calls_made = []

    async def mock_create(task_data, user_id, db_session):
        calls_made.append(("create", user_id))
        mock_task = MagicMock()
        mock_task.id = "task-123"
        mock_task.title = "Test"
        return mock_task

    monkeypatch.setattr("chatbot.tools.task_tools.TaskService.create_task_for_user", mock_create)

    await add_task(mock_context, title="Test task")

    assert len(calls_made) == 1
    assert calls_made[0][1] == "test-user-123"
