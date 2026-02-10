# API Contract: Chat Endpoint

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-02-08

## Chat Endpoint

### POST /api/{user_id}/chat

Send a natural language message to the AI chatbot. The backend routes
the message to the appropriate agent and returns the response.

**Authentication**: Bearer JWT token required
**Authorization**: JWT user_id MUST match path user_id

**Request**:
```json
{
  "message": "Add a task to buy groceries"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | yes | Natural language user input |

**Response (200 OK)**:
```json
{
  "reply": "Task created: 'Buy groceries' (ID: abc-123)",
  "tool_calls": [
    {
      "tool": "add_task",
      "args": {"user_id": "usr-1", "title": "Buy groceries", "description": null},
      "result": {"task_id": "abc-123", "status": "created"}
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| reply | string | Human-readable assistant response |
| tool_calls | array | MCP tools invoked (may be empty) |
| tool_calls[].tool | string | Tool name |
| tool_calls[].args | object | Arguments passed to tool |
| tool_calls[].result | object | Tool execution result |

**Error Responses**:

| Status | Condition |
|--------|-----------|
| 400 | Empty or invalid message |
| 401 | Missing or invalid JWT |
| 403 | JWT user_id does not match path user_id |
| 500 | Agent processing failure |

### GET /api/{user_id}/chat/history

Retrieve conversation history for the authenticated user.

**Authentication**: Bearer JWT token required
**Authorization**: JWT user_id MUST match path user_id

**Query Parameters**:

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| limit | integer | 50 | Max messages to return |
| offset | integer | 0 | Pagination offset |

**Response (200 OK)**:
```json
{
  "messages": [
    {
      "id": "msg-1",
      "role": "user",
      "content": "Add a task to buy groceries",
      "tool_calls": null,
      "created_at": "2026-02-08T10:00:00Z"
    },
    {
      "id": "msg-2",
      "role": "assistant",
      "content": "Task created: 'Buy groceries' (ID: abc-123)",
      "tool_calls": [{"tool": "add_task", "result": {"task_id": "abc-123"}}],
      "created_at": "2026-02-08T10:00:01Z"
    }
  ],
  "total": 42
}
```
