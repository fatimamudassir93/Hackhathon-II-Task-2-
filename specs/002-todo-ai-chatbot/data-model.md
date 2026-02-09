# Data Model: Todo AI Chatbot

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-02-08

## Existing Entities (No Changes)

### User (Better Auth managed)

| Field | Type | Constraints |
|-------|------|-------------|
| id | text | PK |
| name | text | NOT NULL |
| email | text | NOT NULL, UNIQUE |
| email_verified | boolean | NOT NULL, DEFAULT false |
| image | text | nullable |
| created_at | timestamp | NOT NULL, DEFAULT now() |
| updated_at | timestamp | NOT NULL, DEFAULT now() |

*Managed by Better Auth. Also exists in backend as SQLModel `User`
with `hashed_password` field for JWT auth.*

### Task (Existing)

| Field | Type | Constraints |
|-------|------|-------------|
| id | text | PK (UUID) |
| user_id | text | FK → user.id, NOT NULL, CASCADE |
| title | varchar(255) | NOT NULL |
| description | text | nullable |
| completed | boolean | NOT NULL, DEFAULT false |
| priority | varchar(20) | NOT NULL, DEFAULT 'medium' |
| due_date | timestamp | nullable |
| recurrence_pattern | varchar(20) | nullable |
| recurrence_end_date | timestamp | nullable |
| parent_task_id | text | nullable |
| reminder_enabled | boolean | NOT NULL, DEFAULT false |
| reminder_offset_minutes | integer | nullable |
| reminder_sent_at | timestamp | nullable |
| created_at | timestamp | NOT NULL, DEFAULT now() |
| updated_at | timestamp | NOT NULL, DEFAULT now() |

## New Entities

### Tag

| Field | Type | Constraints |
|-------|------|-------------|
| id | text | PK (UUID) |
| user_id | text | FK → user.id, NOT NULL, CASCADE |
| name | varchar(50) | NOT NULL |
| created_at | timestamp | NOT NULL, DEFAULT now() |

**Unique constraint**: (user_id, name) — a user cannot have
duplicate tag names.

### Task_Tag (Join Table)

| Field | Type | Constraints |
|-------|------|-------------|
| task_id | text | FK → task.id, NOT NULL, CASCADE |
| tag_id | text | FK → tag.id, NOT NULL, CASCADE |

**Primary key**: (task_id, tag_id)

### Reminder

| Field | Type | Constraints |
|-------|------|-------------|
| id | text | PK (UUID) |
| user_id | text | FK → user.id, NOT NULL, CASCADE |
| task_id | text | FK → task.id, NOT NULL, CASCADE |
| remind_at | timestamp | NOT NULL |
| status | varchar(20) | NOT NULL, DEFAULT 'active' |
| created_at | timestamp | NOT NULL, DEFAULT now() |

**Status values**: active, cancelled, sent

**Validation**: `remind_at` MUST be in the future at creation time.

### Conversation_Message

| Field | Type | Constraints |
|-------|------|-------------|
| id | text | PK (UUID) |
| user_id | text | FK → user.id, NOT NULL, CASCADE |
| role | varchar(20) | NOT NULL |
| content | text | NOT NULL |
| tool_calls | text | nullable (JSON string) |
| created_at | timestamp | NOT NULL, DEFAULT now() |

**Role values**: user, assistant
**tool_calls**: JSON-serialized array of tool invocations made during
this message (for display in chat UI). Nullable for user messages.

## Relationships

```
User (1) ──── (N) Task
User (1) ──── (N) Tag
User (1) ──── (N) Reminder
User (1) ──── (N) Conversation_Message
Task (N) ──── (N) Tag  (via Task_Tag)
Task (1) ──── (N) Reminder
```

## State Transitions

### Task.completed
```
false (pending) ──→ true (completed) via complete_task
true (completed) ──→ false (pending) via update_task
```

### Reminder.status
```
active ──→ cancelled  via cancel_reminder
active ──→ sent       via system (when remind_at is reached)
```

## Indexes

- `idx_task_user_id` on task(user_id)
- `idx_tag_user_id` on tag(user_id)
- `idx_task_tag_task_id` on task_tag(task_id)
- `idx_task_tag_tag_id` on task_tag(tag_id)
- `idx_reminder_user_id` on reminder(user_id)
- `idx_reminder_task_id` on reminder(task_id)
- `idx_reminder_status` on reminder(status) WHERE status = 'active'
- `idx_conversation_user_id` on conversation_message(user_id)
- `idx_conversation_created_at` on conversation_message(user_id, created_at)
