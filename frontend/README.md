# Next.js Frontend

## Overview

This is the Next.js frontend for the Phase II Todo application. It's a **full-stack Next.js application** with built-in API routes that handle authentication and task management.

## Architecture

- **Framework**: Next.js 14 (App Router)
- **Authentication**: Better Auth with email/password
- **Database**: Neon PostgreSQL (via Drizzle ORM)
- **Styling**: Tailwind CSS
- **API**: Next.js API Routes (not external FastAPI)

## Important Note

This frontend uses **Next.js API routes** (`/app/api/*`) for backend functionality, NOT the separate FastAPI backend. The API routes directly access the Neon database using Drizzle ORM.

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

   Edit `.env.local` with your values:
   - `BETTER_AUTH_SECRET`: Generate with `openssl rand -base64 32`
   - `BETTER_AUTH_URL`: `http://localhost:3000` for local dev
   - `DATABASE_URL_NEON`: Your Neon PostgreSQL connection string

3. **Push database schema**:
   ```bash
   npm run db:push
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
2. Add these variables:
   - `BETTER_AUTH_SECRET`: Your secret key (same as local)
   - `BETTER_AUTH_URL`: Your Vercel deployment URL (e.g., `https://your-app.vercel.app`)
   - `DATABASE_URL_NEON`: Your Neon PostgreSQL connection string

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
git commit -m "Configure Vercel deployment"
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
│   ├── api/
│   │   ├── auth/            # Better Auth API routes
│   │   └── tasks/           # Task CRUD API routes
│   ├── dashboard/           # Main dashboard page
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Landing page
├── components/              # Reusable UI components
├── hooks/                   # Custom React hooks
├── lib/
│   ├── auth.ts             # Better Auth configuration
│   ├── auth-client.ts      # Client-side auth utilities
│   ├── db.ts               # Database connection
│   └── schema.ts           # Drizzle ORM schema
├── .env.local              # Local environment variables (not in git)
├── .env.example            # Environment variables template
└── package.json
```

## API Routes

All API routes are Next.js API routes (not external API):

### Authentication
- `POST /api/auth/sign-up` - Register new user
- `POST /api/auth/sign-in` - Sign in user
- `GET /api/auth/session` - Get current session

### Tasks
- `GET /api/tasks` - List all user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/[id]` - Get specific task
- `PUT /api/tasks/[id]` - Update task
- `DELETE /api/tasks/[id]` - Delete task
- `PATCH /api/tasks/[id]/complete` - Toggle completion

## Database Schema

Managed by Drizzle ORM in `lib/schema.ts`:

- **users** - User accounts (managed by Better Auth)
- **sessions** - User sessions (managed by Better Auth)
- **tasks** - User tasks with CRUD operations

## Troubleshooting

### 404 Error on Vercel

If you get 404 errors:
1. Verify `vercel.json` exists in project root
2. Check that Root Directory is set to `frontend` in Vercel settings
3. Ensure environment variables are set in Vercel dashboard
4. Check build logs for errors

### Database Connection Issues

If database connection fails:
1. Verify `DATABASE_URL_NEON` is correct
2. Ensure your IP is whitelisted in Neon dashboard
3. Check that the connection string includes `?sslmode=require`

### Authentication Issues

If auth doesn't work:
1. Verify `BETTER_AUTH_SECRET` is set
2. Ensure `BETTER_AUTH_URL` matches your deployment URL
3. Check that database schema is pushed (`npm run db:push`)

## Architecture Note

This implementation differs from the original Phase 2 specs:

**Spec**: Next.js frontend + FastAPI backend
**Implementation**: Full-stack Next.js with API routes

The FastAPI backend exists but is not used by this frontend. If you need to use the FastAPI backend instead, you would need to:
1. Remove Next.js API routes
2. Create an API client to call FastAPI endpoints
3. Update authentication to use JWT tokens from FastAPI
