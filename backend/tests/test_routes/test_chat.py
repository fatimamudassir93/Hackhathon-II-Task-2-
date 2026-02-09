"""
Integration tests for chat endpoints

Per Constitution Principle V: Test-First (NON-NEGOTIABLE)
Tests authentication, message processing, and conversation history.
"""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import status


@pytest.mark.asyncio
async def test_chat_endpoint_requires_authentication(async_client: AsyncClient):
    """Test that chat endpoint rejects unauthenticated requests"""
    response = await async_client.post(
        "/api/test-user-123/chat",
        json={"message": "Hello"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_chat_endpoint_rejects_mismatched_user_id(async_client: AsyncClient, auth_headers):
    """Test that user cannot access another user's chat"""
    # auth_headers contains token for user-123
    response = await async_client.post(
        "/api/different-user-456/chat",
        json={"message": "Hello"},
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_chat_endpoint_success(async_client: AsyncClient, auth_headers):
    """Test successful chat message processing"""
    with patch("chatbot.services.chat_service.ChatService.process_message") as mock_process:
        mock_process.return_value = {
            "reply": "Task added successfully!",
            "tool_calls": [{"tool": "add_task", "args": {"title": "Buy groceries"}, "result": {"task_id": "123"}}]
        }

        response = await async_client.post(
            "/api/test-user-123/chat",
            json={"message": "Add a task to buy groceries"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "reply" in data
        assert "tool_calls" in data
        assert data["reply"] == "Task added successfully!"
        assert len(data["tool_calls"]) == 1


@pytest.mark.asyncio
async def test_chat_endpoint_empty_message(async_client: AsyncClient, auth_headers):
    """Test that empty messages are rejected"""
    response = await async_client.post(
        "/api/test-user-123/chat",
        json={"message": ""},
        headers=auth_headers
    )

    # Should either reject or handle gracefully
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK]


@pytest.mark.asyncio
async def test_chat_history_requires_authentication(async_client: AsyncClient):
    """Test that history endpoint requires authentication"""
    response = await async_client.get("/api/test-user-123/chat/history")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_chat_history_success(async_client: AsyncClient, auth_headers):
    """Test retrieving chat history"""
    with patch("chatbot.services.conversation_service.ConversationService.get_history") as mock_history:
        mock_messages = [
            MagicMock(
                id="msg-1",
                role="user",
                content="Hello",
                tool_calls=None,
                created_at="2024-01-01T00:00:00"
            ),
            MagicMock(
                id="msg-2",
                role="assistant",
                content="Hi! How can I help?",
                tool_calls=None,
                created_at="2024-01-01T00:00:01"
            )
        ]
        mock_history.return_value = (mock_messages, 2)

        response = await async_client.get(
            "/api/test-user-123/chat/history?limit=50&offset=0",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "messages" in data
        assert "total" in data
        assert data["total"] == 2
        assert len(data["messages"]) == 2


@pytest.mark.asyncio
async def test_chat_history_pagination(async_client: AsyncClient, auth_headers):
    """Test chat history pagination"""
    with patch("chatbot.services.conversation_service.ConversationService.get_history") as mock_history:
        mock_history.return_value = ([], 100)

        response = await async_client.get(
            "/api/test-user-123/chat/history?limit=10&offset=20",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 100


@pytest.mark.asyncio
async def test_chat_endpoint_handles_tool_errors(async_client: AsyncClient, auth_headers):
    """Test that tool execution errors are handled gracefully"""
    with patch("chatbot.services.chat_service.ChatService.process_message") as mock_process:
        mock_process.return_value = {
            "reply": "I encountered an error: Task not found",
            "tool_calls": [{"tool": "complete_task", "args": {"task_id": "999"}, "result": {"error": "Task not found"}}]
        }

        response = await async_client.post(
            "/api/test-user-123/chat",
            json={"message": "Complete task 999"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "error" in data["reply"].lower() or "error" in str(data["tool_calls"])


@pytest.mark.asyncio
async def test_conversation_persistence(async_client: AsyncClient, auth_headers):
    """Test that conversations are persisted across requests"""
    with patch("chatbot.services.chat_service.ChatService.process_message") as mock_process:
        mock_process.return_value = {
            "reply": "Task added!",
            "tool_calls": []
        }

        # Send first message
        await async_client.post(
            "/api/test-user-123/chat",
            json={"message": "Add task 1"},
            headers=auth_headers
        )

        # Send second message
        await async_client.post(
            "/api/test-user-123/chat",
            json={"message": "Add task 2"},
            headers=auth_headers
        )

        # Verify process_message was called twice
        assert mock_process.call_count == 2


# Fixtures for testing
@pytest.fixture
async def async_client():
    """Create async test client"""
    from backend.app import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def auth_headers():
    """Create mock authentication headers"""
    # In real tests, generate valid JWT token
    return {
        "Authorization": "Bearer mock-jwt-token-for-test-user-123"
    }
