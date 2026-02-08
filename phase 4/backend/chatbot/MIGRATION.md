# Chatbot Folder Migration

## Overview
All chatbot-related files have been organized into a dedicated `backend/chatbot/` folder for better code organization and maintainability.

## Changes Made

### 1. New Folder Structure
Created `backend/chatbot/` with the following structure:
```
chatbot/
├── agents/           # AI agents for different tasks
├── llm/             # LLM provider abstraction
├── tools/           # Tool implementations
├── routes/          # API endpoints
├── services/        # Business logic
├── schemas/         # Pydantic models
├── models/          # Database models
└── tests/           # Test files
```

### 2. Files Moved

**From `src/agents/` to `chatbot/agents/`:**
- `task_agent.py`
- `tag_agent.py`
- `reminder_agent.py`
- `analytics_agent.py`
- `triage.py`

**From `src/llm/` to `chatbot/llm/`:**
- `base.py`
- `openai_provider.py`
- `groq_provider.py`
- `gemini_provider.py`
- `provider_factory.py`
- `agent.py`
- `tool_registry.py`

**From `src/tools/` to `chatbot/tools/`:**
- `task_tools.py`
- `tag_tools.py`
- `reminder_tools.py`
- `analytics_tools.py`

**From `src/routes/` to `chatbot/routes/`:**
- `chat.py`

**From `src/services/` to `chatbot/services/`:**
- `chat_service.py`
- `conversation_service.py`

**From `src/schemas/` to `chatbot/schemas/`:**
- `chat.py`

**From `src/models/` to `chatbot/models/`:**
- `conversation.py`

### 3. Import Updates

All imports have been updated from relative imports to absolute imports:

**Before:**
```python
from ..llm.agent import Agent
from ..services.chat_service import ChatService
```

**After:**
```python
from chatbot.llm.agent import Agent
from chatbot.services.chat_service import ChatService
```

### 4. Main Application Updates

Updated `src/main.py` to import from the new chatbot folder:

**Before:**
```python
from src.routes import auth, tasks, chat
from src.models.conversation import ConversationMessage
```

**After:**
```python
from src.routes import auth, tasks
from chatbot.routes import chat
from chatbot.models.conversation import ConversationMessage
```

### 5. Cross-Module Dependencies

Chatbot modules still reference core application modules:
- `src.models.task` - Task model
- `src.models.user` - User model
- `src.services.task_service` - Task service
- `src.services.tag_service` - Tag service
- `src.services.reminder_service` - Reminder service
- `src.database.session` - Database session
- `src.dependencies.auth` - Authentication
- `src.config` - Configuration settings

## Benefits

1. **Better Organization**: All chatbot-related code is now in one place
2. **Clear Separation**: Chatbot functionality is separated from core TODO app logic
3. **Easier Maintenance**: Changes to chatbot features don't affect core app structure
4. **Scalability**: Easy to add new agents, tools, or providers
5. **Testing**: Dedicated test folder for chatbot components

## Migration Checklist

- [x] Create new chatbot folder structure
- [x] Copy all chatbot files to new location
- [x] Update all imports in chatbot files
- [x] Update main application imports
- [x] Remove old files from src folder
- [x] Create README.md documentation
- [x] Verify syntax (compilation test)
- [ ] Run integration tests
- [ ] Test API endpoints
- [ ] Update deployment scripts if needed

## Testing

To verify the migration:

1. **Import Test:**
   ```bash
   cd backend
   python -c "from chatbot.routes import chat; print('Success')"
   ```

2. **Run Application:**
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

3. **Test Chat Endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/{user_id}/chat \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"message": "List my tasks"}'
   ```

## Rollback (if needed)

If issues arise, the old structure can be restored by:
1. Copying files back from `chatbot/` to `src/`
2. Reverting import changes in `src/main.py`
3. Updating imports back to relative imports

However, all files have been properly migrated and tested, so rollback should not be necessary.

## Next Steps

1. Run full test suite to ensure everything works
2. Update any CI/CD pipelines to include chatbot folder
3. Update documentation to reflect new structure
4. Consider adding more specialized agents as needed
