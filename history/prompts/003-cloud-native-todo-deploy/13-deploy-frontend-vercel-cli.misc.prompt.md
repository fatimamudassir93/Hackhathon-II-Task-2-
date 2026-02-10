---
id: 13
title: Deploy Frontend to Vercel via CLI
stage: misc
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5
feature: 003-cloud-native-todo-deploy
branch: 003-cloud-native-todo-deploy
user: shoai
command: implement plan
labels: ["deployment", "vercel", "frontend", "cli", "environment-variables"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - C:\Users\shoai\Desktop\TODO-app\frontend\.vercel\project.json
 - C:\Users\shoai\Desktop\TODO-app\frontend\.vercel\README.txt
 - C:\Users\shoai\Desktop\TODO-app\frontend\.env.production
tests:
 - Verified backend health endpoint (https://fatima7860-phase3-backend.hf.space/health)
 - Verified backend API docs (https://fatima7860-phase3-backend.hf.space/docs)
 - Verified frontend homepage loads (https://frontend-snowy-gamma.vercel.app)
 - Verified database connection via /api/test-db endpoint
 - Verified sign-in and sign-up pages load correctly
---

## Prompt

Implement the following plan:

# Plan: Deploy Frontend to Vercel using CLI

The user has a Next.js 14 frontend application that needs to be deployed to Vercel using the Vercel CLI. The backend has already been deployed to Hugging Face Spaces at `https://fatima7860-phase3-backend.hf.space`. The frontend uses Better Auth for authentication, Drizzle ORM with Neon PostgreSQL database, and API routes that proxy requests to the backend.

Required environment variables:
1. DATABASE_URL_NEON - Neon database connection string
2. BETTER_AUTH_SECRET - Secret key for Better Auth
3. BETTER_AUTH_URL - Frontend URL (set after first deployment)
4. BACKEND_URL - Hugging Face backend URL

Implementation steps include: verify backend, install Vercel CLI, login, deploy, set environment variables, and verify functionality.

## Response snapshot

Successfully deployed the Next.js frontend to Vercel using CLI:

1. **Backend Verification**: Confirmed Hugging Face backend is healthy and responding at https://fatima7860-phase3-backend.hf.space

2. **Vercel CLI Setup**:
   - Installed Vercel CLI globally via npm
   - User completed manual login via browser authentication

3. **Directory Navigation**:
   - Initially attempted deployment from wrong directory (Phase 3/frontend was empty)
   - Located actual frontend code at C:\Users\shoai\Desktop\TODO-app\frontend

4. **Initial Deployment Attempt**:
   - First deployment failed due to missing DATABASE_URL_NEON environment variable
   - Build error: "No database connection string was provided to `neon()`"

5. **Environment Variables Configuration**:
   - Found DATABASE_URL_NEON, BETTER_AUTH_SECRET, and BETTER_AUTH_URL already configured from previous deployment
   - Added missing BACKEND_URL environment variable: https://fatima7860-phase3-backend.hf.space

6. **Production Deployment**:
   - Executed `vercel --prod` successfully
   - Build completed in 34 seconds
   - Generated production URLs:
     - Primary: https://frontend-kt5ct4f7w-fatima-mudassirs-projects.vercel.app
     - Alias: https://frontend-snowy-gamma.vercel.app

7. **Verification**:
   - Homepage loads correctly with TaskFlow branding
   - Database connection confirmed (9 tables detected)
   - Sign-in/sign-up pages accessible
   - Backend health check passing

Build warnings about dynamic server usage for /chat and /dashboard routes are expected since these pages use authentication headers and must be server-rendered.

## Outcome

- ✅ Impact: Frontend successfully deployed to Vercel production with all environment variables configured. Application is accessible at https://frontend-snowy-gamma.vercel.app
- 🧪 Tests: Backend health check passed, database connection verified, homepage and auth pages loading correctly
- 📁 Files: Created .vercel configuration directory, pulled production environment variables
- 🔁 Next prompts: Manual testing of authentication flow, task CRUD operations, and AI chat integration
- 🧠 Reflection: Initial confusion about directory structure (Phase 3 subdirectory vs root frontend) caused delay. Environment variables were mostly pre-configured from previous deployment attempt, only BACKEND_URL needed to be added.

## Evaluation notes (flywheel)

- Failure modes observed: Directory structure confusion (empty Phase 3/frontend vs actual frontend directory), initial build failure due to missing environment variable during build-time
- Graders run and results (PASS/FAIL): Backend health check PASS, Database connection PASS, Frontend deployment PASS, Homepage load PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify BETTER_AUTH_URL is correctly set to production URL, test complete authentication and task management flow in browser
