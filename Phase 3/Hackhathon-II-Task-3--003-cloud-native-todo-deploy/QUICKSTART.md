# Quick Start Guide - Phase 3 TODO AI Chatbot

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database (Neon recommended)
- API key for one of: Groq (free), Gemini (free), or OpenAI (paid)

## Step 1: Get API Keys

### Option A: Groq (Recommended for Development - Free & Fast)
1. Visit https://console.groq.com
2. Sign up for a free account
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### Option B: Google Gemini (Free Tier Available)
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy the key

### Option C: OpenAI (Paid)
1. Visit https://platform.openai.com/api-keys
2. Sign in or create account
3. Create new secret key
4. Copy the key (starts with `sk-`)

## Step 2: Backend Setup

```bash
# Navigate to backend directory
cd "Phase 3/backend"

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env file with your settings
# Required settings:
#   - DATABASE_URL (your Neon PostgreSQL connection string)
#   - BETTER_AUTH_SECRET (generate with: openssl rand -hex 32)
#   - LLM_PROVIDER (choose: groq, gemini, or openai)
#   - API key for your chosen provider
```

### Example .env Configuration (Groq)

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname
BETTER_AUTH_SECRET=your-secret-key-here
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

### Verify Setup

```bash
# Run verification script
python verify_setup.py

# Should show all checks passing
```

### Start Backend

```bash
# Start the FastAPI server
uvicorn src.main:app --reload

# Server will start on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

## Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd "../frontend"

# Install dependencies (if not already done)
npm install

# Create environment file
# Create .env.local with:
BACKEND_URL=http://localhost:8000

# Start development server
npm run dev

# Frontend will start on http://localhost:3000
```

## Step 4: Test the Application

1. **Open Browser**: Navigate to http://localhost:3000

2. **Sign Up**: Create a new account
   - Click "Sign Up"
   - Enter name, email, password
   - Submit

3. **Navigate to Chat**: Click "AI Chat" in the navbar

4. **Test Commands**:
   ```
   Add a task to buy groceries
   Show my tasks
   Add a task to finish the project report
   How many tasks do I have?
   Complete the first task
   Show my completed tasks
   ```

## Step 5: Verify Everything Works

### Backend Health Check
```bash
# In a new terminal
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### Test Chat API (with authentication)
```bash
# First, sign in via the web UI and get your session
# Then test the API directly (requires JWT token)
```

## Troubleshooting

### Backend Issues

**Error: "GROQ_API_KEY is required"**
- Solution: Make sure `.env` file exists and has the correct API key

**Error: "Module not found"**
- Solution: Run `pip install -r requirements.txt`

**Error: "Database connection failed"**
- Solution: Check DATABASE_URL in `.env`
- Verify Neon database is accessible

**Error: "Tool not found"**
- Solution: Make sure tool modules are imported in agent files
- Check that `@tool_registry.register()` decorators are present

### Frontend Issues

**Error: "Failed to fetch"**
- Solution: Verify backend is running on http://localhost:8000
- Check BACKEND_URL in `.env.local`

**Error: "Unauthorized"**
- Solution: Sign in first via the web UI
- Check that BETTER_AUTH_SECRET matches between frontend and backend

**Chat not responding**
- Solution: Check browser console for errors
- Verify API key is valid
- Check backend logs for errors

### Provider-Specific Issues

**Groq: Rate limit exceeded**
- Solution: Groq free tier has rate limits
- Wait a few minutes or upgrade to paid tier

**Gemini: API key invalid**
- Solution: Regenerate API key at https://aistudio.google.com
- Make sure key is copied correctly

**OpenAI: Insufficient quota**
- Solution: Add credits to your OpenAI account
- Check usage at https://platform.openai.com/usage

## Architecture Overview

```
User Browser
    ↓
Next.js Frontend (localhost:3000)
    ↓ (Better Auth session cookie)
Next.js API Routes (/api/chat)
    ↓ (JWT token minted)
FastAPI Backend (localhost:8000)
    ↓ (JWT validated)
ChatService
    ↓ (Routes to agent)
Agent (Task/Tag/Reminder/Analytics)
    ↓ (Calls LLM provider)
LLM Provider (Groq/Gemini/OpenAI)
    ↓ (Returns with tool calls)
MCP Tools
    ↓ (Database operations)
Neon PostgreSQL
```

## File Structure

```
Phase 3/
├── backend/
│   ├── src/
│   │   ├── llm/              # Multi-provider system
│   │   ├── agents/           # Specialist agents
│   │   ├── tools/            # MCP tools
│   │   ├── services/         # Business logic
│   │   ├── routes/           # API endpoints
│   │   └── models/           # Database models
│   ├── .env                  # Configuration (create from .env.example)
│   ├── requirements.txt      # Python dependencies
│   └── verify_setup.py       # Setup verification script
│
└── frontend/
    ├── app/
    │   ├── chat/             # Chat page
    │   └── api/chat/         # Chat API proxy routes
    ├── components/           # React components
    ├── lib/                  # Utilities
    └── .env.local            # Frontend config (create this)
```

## Next Steps

1. **Explore the Chat**: Try different commands and see how the AI responds
2. **Switch Providers**: Change `LLM_PROVIDER` in `.env` to test different models
3. **Add Features**: Implement remaining user stories (tags, reminders, analytics UI)
4. **Write Tests**: Add unit and integration tests (T019-T021)
5. **Deploy**: Deploy to production (Vercel for frontend, Railway/Render for backend)

## Useful Commands

```bash
# Backend
cd backend
python verify_setup.py          # Verify configuration
uvicorn src.main:app --reload   # Start server
pip install -r requirements.txt # Install dependencies

# Frontend
cd frontend
npm run dev                     # Start dev server
npm run build                   # Build for production
npm install                     # Install dependencies

# Database
npm run db:push                 # Push schema changes
npm run db:studio               # Open Drizzle Studio
```

## Support

- **Documentation**: See `LLM_PROVIDERS.md` for detailed provider info
- **Implementation**: See `IMPLEMENTATION_SUMMARY.md` for complete overview
- **Issues**: Check backend logs and browser console for errors

## Success Criteria

✅ Backend starts without errors
✅ Frontend loads and shows sign-in page
✅ Can create account and sign in
✅ Chat page loads with empty state
✅ Can send messages and receive responses
✅ Tasks are created via natural language
✅ Conversation history persists across page refreshes

Enjoy your AI-powered TODO app! 🎉
