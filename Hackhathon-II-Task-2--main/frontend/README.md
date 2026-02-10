# Next.js Frontend - Phase 2

## Overview

This is the Next.js frontend for the Phase 2 Todo application. It communicates with a separate FastAPI backend via REST API calls with JWT authentication.

## Architecture

```
┌─────────────┐      REST API      ┌──────────────┐      SQLModel     ┌──────────┐
│   Next.js   │ ───────────────▶   │   FastAPI    │ ────────────────▶ │   Neon   │
│  (UI Only)  │ ◀───────────────   │   Backend    │ ◀────────────────  │ Database │
└─────────────┘    JSON + JWT      └──────────────┘                    └──────────┘
```

**Key characteristics:**
- Frontend: React components, forms, displays only
- Backend: All business logic, JWT auth, database access
- Communication: REST API calls with JWT tokens
- Clear separation of concerns

## Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **API Communication**: Fetch API with custom client

## Local Development

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```

   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the FastAPI backend** (in separate terminal):
   ```bash
   cd ../backend
   uvicorn src.main:app --reload --port 8000
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

   Open http://localhost:3000

## Deploying to Vercel

### Step 1: Configure Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add this variable:
   - `NEXT_PUBLIC_API_URL`: Your deployed FastAPI backend URL
     - Example: `https://fatima7860-phase3-backend.hf.space`

### Step 2: Configure Build Settings

Vercel should auto-detect Next.js, but verify:

- **Framework Preset**: Next.js
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### Step 3: Deploy

```bash
# From project root
git add .
git commit -m "Configure Phase 2 deployment"
git push origin main
```

Vercel will automatically deploy when you push to main.

## Project Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── sign-in/         # Sign in page
│   │   └── sign-up/         # Sign up page
│   ├── dashboard/           # Main dashboard page
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Landing page
├── components/              # Reusable UI components
│   ├── AuthForm.tsx        # Authentication form
│   ├── Navbar.tsx          # Navigation bar
│   ├── TaskList.tsx        # Task list display
│   ├── TaskForm.tsx        # Task creation form
│   └── TaskItem.tsx        # Individual task card
├── lib/
│   └── api-client.ts       # FastAPI backend client
├── .env.local              # Local environment variables (not in git)
├── .env.example            # Environment variables template
└── package.json
```

## API Communication

All API calls go through the `apiClient` in `lib/api-client.ts`:

### Authentication
- `apiClient.signup(email, password, name)` - Register new user
- `apiClient.signin(email, password)` - Sign in user

### Tasks
- `apiClient.getTasks(userId)` - List all user's tasks
- `apiClient.createTask(userId, task)` - Create new task
- `apiClient.getTask(userId, taskId)` - Get specific task
- `apiClient.updateTask(userId, taskId, updates)` - Update task
- `apiClient.deleteTask(userId, taskId)` - Delete task
- `apiClient.toggleTaskComplete(userId, taskId)` - Toggle completion

## Authentication Flow

1. User signs up or signs in via the frontend
2. Frontend calls FastAPI `/api/signup` or `/api/signin`
3. Backend validates credentials and returns JWT token + user data
4. Frontend stores token in localStorage via `apiClient.setToken()`
5. Frontend includes JWT token in Authorization header for all subsequent requests
6. Backend validates token and processes requests

## Troubleshooting

### Backend Connection Issues

If you get network errors:
1. Verify backend is running and accessible
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Test backend health: `curl http://localhost:8000/health`
4. Check browser console for CORS errors

### Authentication Issues

If auth doesn't work:
1. Verify backend is returning JWT tokens
2. Check localStorage for `auth_token` and `user` data
3. Verify token is being sent in Authorization header
4. Check backend logs for authentication errors

### CORS Issues

If you see CORS errors in browser console:
1. Verify backend has CORS middleware configured
2. Check that frontend URL is in backend's allowed origins
3. Ensure credentials are being sent correctly

## Architecture Note

This is the **correct Phase 2 implementation**:

✅ **Phase 2 Architecture**:
- Next.js frontend (UI only)
- FastAPI backend (business logic)
- JWT authentication
- REST API communication
- Separated concerns

❌ **NOT Phase 2** (what was built before):
- Full-stack Next.js with API routes
- Better Auth library
- Drizzle ORM in frontend
- Monolithic architecture

## References

- **API Specification**: `../specs/api/rest-endpoints.md`
- **Database Schema**: `../specs/database/schema.md`
- **Authentication Spec**: `../specs/authentication/spec.md`
- **Task CRUD Spec**: `../specs/task-crud/spec.md`
- **Backend README**: `../backend/README.md`

