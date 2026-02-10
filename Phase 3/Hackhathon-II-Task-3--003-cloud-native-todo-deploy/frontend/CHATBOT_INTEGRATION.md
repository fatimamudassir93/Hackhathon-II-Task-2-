# Frontend Integration with Chatbot

## Overview

The frontend is already fully integrated with the new chatbot structure. **No code changes are required** because the backend API endpoints remain unchanged - only the internal organization of the backend code has changed.

## Current Setup

### Frontend Structure

```
frontend/
├── app/
│   ├── api/
│   │   └── chat/
│   │       ├── route.ts           # POST /api/chat (proxy to backend)
│   │       └── history/
│   │           └── route.ts       # GET /api/chat/history (proxy)
│   └── chat/
│       └── page.tsx               # Chat page component
├── components/
│   ├── ChatInterface.tsx          # Main chat UI
│   ├── ChatMessage.tsx            # Message display
│   └── ToolCallDisplay.tsx        # Tool call visualization
└── lib/
    └── chat-api.ts                # API client functions
```

### API Flow

```
User Browser
    ↓
Frontend (Next.js)
    ↓ /api/chat
Next.js API Route (Proxy)
    ↓ POST http://localhost:8000/api/{user_id}/chat
Backend FastAPI (chatbot/routes/chat.py)
    ↓
Chatbot Service (chatbot/services/chat_service.py)
    ↓
Agent System (chatbot/agents/)
    ↓
LLM Provider (chatbot/llm/)
    ↓
Tools (chatbot/tools/)
```

## Configuration

### Backend URL

The frontend needs to know where the backend is running. This is configured in `.env`:

```env
BACKEND_URL=http://localhost:8000
```

**Default:** If not set, defaults to `http://localhost:8000`

### Current Configuration

The frontend `.env` currently has:
- ✅ `BETTER_AUTH_SECRET` - Set
- ✅ `BETTER_AUTH_URL` - Set to http://localhost:3000
- ✅ `DATABASE_URL` - Set (Neon PostgreSQL)
- ⚠️ `BACKEND_URL` - Not explicitly set (using default)

**Recommendation:** Add to frontend `.env`:
```env
BACKEND_URL=http://localhost:8000
```

## API Endpoints

### 1. Send Chat Message

**Frontend Route:** `POST /api/chat`

**Backend Endpoint:** `POST /api/{user_id}/chat`

**Request:**
```typescript
{
  message: string
}
```

**Response:**
```typescript
{
  reply: string,
  tool_calls: ToolCallInfo[]
}
```

**Example:**
```typescript
import { sendMessage } from '@/lib/chat-api';

const response = await sendMessage("Add a task to buy groceries");
console.log(response.reply); // "I've added the task 'Buy groceries' for you."
console.log(response.tool_calls); // [{ tool: "add_task", args: {...}, result: {...} }]
```

### 2. Get Chat History

**Frontend Route:** `GET /api/chat/history`

**Backend Endpoint:** `GET /api/{user_id}/chat/history`

**Query Parameters:**
- `limit` (optional, default: 50)
- `offset` (optional, default: 0)

**Response:**
```typescript
{
  messages: ChatMessage[],
  total: number
}
```

**Example:**
```typescript
import { getHistory } from '@/lib/chat-api';

const history = await getHistory(50, 0);
console.log(history.messages); // Array of messages
console.log(history.total); // Total message count
```

## Components

### ChatInterface

Main chat component with:
- Message list with auto-scroll
- Input field with Enter key support
- Loading indicator
- Error display
- Empty state with welcome message

**Usage:**
```tsx
import ChatInterface from '@/components/ChatInterface';

export default function ChatPage() {
  return <ChatInterface />;
}
```

### ChatMessage

Individual message display with:
- User/Assistant avatars
- Message bubbles
- Tool call display
- Timestamps

**Props:**
```typescript
{
  role: "user" | "assistant",
  content: string,
  toolCalls?: ToolCallInfo[],
  timestamp?: string,
  index: number
}
```

### ToolCallDisplay

Displays tool execution details:
- Tool name
- Arguments passed
- Results returned

**Props:**
```typescript
{
  toolCalls: ToolCallInfo[]
}
```

## Authentication

The frontend uses Better Auth for authentication. The API routes automatically:
1. Check for valid session
2. Extract user ID from session
3. Mint internal JWT token
4. Pass token to backend in Authorization header

**Flow:**
```
User → Sign In → Session Created → API Call → Token Minted → Backend Validates
```

## Testing the Integration

### 1. Start Backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:3000

### 3. Test Chat

1. Navigate to http://localhost:3000
2. Sign in or register
3. Go to http://localhost:3000/chat
4. Send a message: "Add a task to buy groceries"
5. Verify the response appears
6. Check tool calls are displayed

### 4. Verify Backend Connection

Check browser console for any errors:
- Network tab should show successful requests to `/api/chat`
- Backend logs should show incoming requests

## Troubleshooting

### "Failed to send message" Error

**Possible Causes:**
1. Backend not running
2. BACKEND_URL incorrect
3. LLM API key not configured
4. Authentication issue

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check BACKEND_URL in frontend `.env`
3. Configure LLM API key in backend `.env`
4. Check browser console for auth errors

### "Unauthorized" Error

**Cause:** Session expired or invalid

**Solution:**
1. Sign out and sign in again
2. Clear browser cookies
3. Check BETTER_AUTH_SECRET matches between frontend and backend

### Backend Connection Refused

**Cause:** Backend not running or wrong port

**Solution:**
1. Start backend: `uvicorn src.main:app --reload --port 8000`
2. Verify port 8000 is not in use
3. Check BACKEND_URL in frontend `.env`

### Tool Calls Not Displaying

**Cause:** ToolCallDisplay component issue

**Solution:**
1. Check browser console for errors
2. Verify tool_calls format in response
3. Check ToolCallDisplay.tsx exists

## Development

### Adding New Chat Features

1. **Backend:** Add new tools in `backend/chatbot/tools/`
2. **Frontend:** No changes needed - tools are automatically displayed
3. **Testing:** Test through chat interface

### Modifying Chat UI

1. **ChatInterface.tsx** - Main layout and logic
2. **ChatMessage.tsx** - Message display
3. **ToolCallDisplay.tsx** - Tool visualization
4. **globals.css** - Styling

### API Client

The `chat-api.ts` file provides typed functions:
- `sendMessage(message: string): Promise<ChatResponse>`
- `getHistory(limit?, offset?): Promise<ChatHistoryResponse>`

Add new functions here for additional endpoints.

## Environment Variables

### Frontend (.env)

```env
# Backend API
BACKEND_URL=http://localhost:8000

# Authentication
BETTER_AUTH_SECRET=your_secret_key
BETTER_AUTH_URL=http://localhost:3000

# Database (for Better Auth)
DATABASE_URL=postgresql://...
```

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://...

# Authentication
BETTER_AUTH_SECRET=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# LLM Provider
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key
```

**Important:** `BETTER_AUTH_SECRET` must match between frontend and backend!

## Production Deployment

### Frontend

1. Set `BACKEND_URL` to production backend URL
2. Build: `npm run build`
3. Deploy to Vercel/Netlify/etc.

### Backend

1. Configure production database
2. Set LLM API key
3. Deploy to Railway/Render/etc.
4. Update frontend `BACKEND_URL` to production URL

### CORS

If frontend and backend are on different domains, configure CORS in backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Summary

✅ **Frontend is already compatible** with the new chatbot structure
✅ **No code changes required** - API endpoints unchanged
✅ **Only configuration needed** - Set BACKEND_URL and LLM API key
✅ **Ready to use** - Start both servers and test

The chatbot reorganization was purely internal to the backend. The frontend continues to work exactly as before!
