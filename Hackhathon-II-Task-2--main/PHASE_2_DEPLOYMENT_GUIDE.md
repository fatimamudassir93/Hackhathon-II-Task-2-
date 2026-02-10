# Phase 2 Deployment Guide

## ✅ What Was Fixed

Your TODO app now has the **correct Phase 2 architecture**:

```
┌─────────────┐      REST API      ┌──────────────┐      SQLModel     ┌──────────┐
│   Next.js   │ ───────────────▶   │   FastAPI    │ ────────────────▶ │   Neon   │
│  (UI Only)  │ ◀───────────────   │   Backend    │ ◀────────────────  │ Database │
└─────────────┘    JSON + JWT      └──────────────┘                    └──────────┘
```

### Changes Made

✅ **Frontend (Next.js)**
- Created API client (`lib/api-client.ts`) for FastAPI communication
- Updated all components to use `apiClient` instead of Next.js API routes
- Removed Better Auth and Drizzle ORM dependencies
- Removed Next.js API routes (`app/api/*`)
- JWT tokens stored in localStorage
- Build successful ✓

✅ **Backend (FastAPI)**
- Already deployed at: https://fatima7860-todo-phase2.hf.space
- Health check: ✓ Working
- All endpoints ready

✅ **Architecture**
- Proper separation of concerns
- Frontend only handles UI
- Backend handles all business logic
- JWT authentication working

---

## 🚀 Deploy to Vercel

### Step 1: Update Vercel Environment Variables

1. Go to your Vercel project: https://vercel.com/dashboard
2. Select your project (todo-app-phase3-frontend or create new)
3. Go to **Settings** → **Environment Variables**
4. **Remove old variables**:
   - `DATABASE_URL_NEON`
   - `BETTER_AUTH_SECRET`
   - `BETTER_AUTH_URL`
   - `NEXT_PUBLIC_BETTER_AUTH_URL`
   - `BACKEND_URL`

5. **Add new variable**:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://fatima7860-todo-phase2.hf.space`
   - **Environment**: Production, Preview, Development (select all)

### Step 2: Update Vercel Build Settings

1. In Vercel project settings, go to **General**
2. Verify these settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next` (leave default)
   - **Install Command**: `npm install`

### Step 3: Deploy

**Option A: Push to GitHub (Automatic)**
```bash
git push origin 003-cloud-native-todo-deploy
```
Vercel will automatically detect the push and deploy.

**Option B: Manual Deploy via Vercel CLI**
```bash
cd frontend
npx vercel --prod
```

### Step 4: Verify Deployment

Once deployed, test your application:

1. **Visit your Vercel URL**: https://your-app.vercel.app
2. **Test Sign Up**:
   - Click "Sign Up"
   - Enter name, email, password
   - Should redirect to dashboard
3. **Test Task Creation**:
   - Click "Add New Task"
   - Create a task
   - Verify it appears in the list
4. **Test Task Operations**:
   - Mark task as complete
   - Edit task
   - Delete task
5. **Test Sign Out**:
   - Click "Sign Out"
   - Should redirect to sign-in page

---

## 🔍 Troubleshooting

### Issue: "Network Error" when signing up/in

**Cause**: Frontend can't reach backend

**Solutions**:
1. Verify backend is running: https://fatima7860-todo-phase2.hf.space/health
2. Check `NEXT_PUBLIC_API_URL` in Vercel environment variables
3. Check browser console for CORS errors
4. Verify Hugging Face Space is not sleeping

### Issue: "401 Unauthorized" on dashboard

**Cause**: JWT token issue

**Solutions**:
1. Clear browser localStorage
2. Sign in again
3. Check that `BETTER_AUTH_SECRET` matches between frontend and backend
4. Verify token is being sent in Authorization header (check Network tab)

### Issue: Backend returns 404

**Cause**: Backend endpoint not found

**Solutions**:
1. Verify backend is deployed correctly
2. Check backend logs on Hugging Face
3. Test endpoints directly with curl:
   ```bash
   curl https://fatima7860-todo-phase2.hf.space/health
   ```

### Issue: CORS errors in browser

**Cause**: Backend not allowing frontend origin

**Solutions**:
1. Check backend CORS configuration in `backend/src/main.py`
2. Ensure your Vercel URL is in allowed origins
3. Verify backend is sending correct CORS headers

---

## 📊 Testing Checklist

After deployment, verify these features:

- [ ] Homepage redirects to sign-in
- [ ] Sign up creates new account
- [ ] Sign in authenticates user
- [ ] Dashboard displays user name
- [ ] Task list loads (empty or with tasks)
- [ ] Create new task works
- [ ] Task appears in list immediately
- [ ] Mark task as complete works
- [ ] Edit task works
- [ ] Delete task works
- [ ] Sign out clears session
- [ ] After sign out, can't access dashboard
- [ ] Can sign in again with same credentials

---

## 🔗 Important URLs

### Production
- **Frontend**: https://your-app.vercel.app (update after deployment)
- **Backend**: https://fatima7860-todo-phase2.hf.space
- **Backend Health**: https://fatima7860-todo-phase2.hf.space/health
- **Backend API Docs**: https://fatima7860-todo-phase2.hf.space/docs

### Repository
- **GitHub**: https://github.com/fatimamudassir93/Hackhathon-II-Task-2-
- **Branch**: 003-cloud-native-todo-deploy

---

## 📝 API Endpoints

Your FastAPI backend provides these endpoints:

### Authentication
- `POST /api/signup` - Register new user
- `POST /api/signin` - Sign in user

### Tasks (Requires JWT token)
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### System
- `GET /` - Root endpoint
- `GET /health` - Health check

---

## 🎯 Success Criteria

Your Phase 2 deployment is successful when:

✅ Frontend is deployed on Vercel
✅ Backend is running on Hugging Face
✅ Users can sign up and sign in
✅ JWT authentication works
✅ Users can create, read, update, delete tasks
✅ Users can only see their own tasks
✅ Sign out works correctly
✅ No console errors in browser
✅ All API calls go to FastAPI backend (not Next.js API routes)

---

## 🔄 Next Steps

After successful Phase 2 deployment:

1. **Test thoroughly** with multiple users
2. **Monitor backend logs** on Hugging Face
3. **Check Vercel analytics** for errors
4. **Document any issues** you encounter
5. **Consider Phase 3** (AI chatbot) if needed

---

## 📚 Documentation

- **Frontend README**: `frontend/README.md`
- **Backend README**: `backend/README.md`
- **Phase Confusion Analysis**: `PHASE_CONFUSION_ANALYSIS.md`
- **Phase 2 Fix Plan**: `PHASE_2_FIX_PLAN.md`
- **API Specs**: `specs/api/rest-endpoints.md`
- **Auth Specs**: `specs/authentication/spec.md`
- **Task Specs**: `specs/task-crud/spec.md`

---

**Status**: Ready to deploy ✅
**Date**: 2026-02-10
**Branch**: 003-cloud-native-todo-deploy
**Commit**: eb7d7b6
