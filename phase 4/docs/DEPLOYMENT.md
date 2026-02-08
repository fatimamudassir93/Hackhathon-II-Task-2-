# Cloud-Native TODO App Deployment Guide

## Overview

This guide covers deploying the TODO application with AI chatbot to production cloud infrastructure using:
- **Backend**: Railway (FastAPI + Python)
- **Frontend**: Vercel (Next.js + TypeScript)
- **Database**: Neon PostgreSQL (existing)
- **CI/CD**: GitHub Actions + Vercel auto-deploy

## Prerequisites

Before deploying, ensure you have:

1. **Accounts**:
   - GitHub account with repository access
   - Railway account (https://railway.app)
   - Vercel account (https://vercel.com)
   - Neon PostgreSQL database (existing)

2. **API Keys**:
   - LLM provider API key (Groq/OpenAI/Gemini)
   - Better Auth secret key

3. **Tools** (for local testing):
   - Docker and Docker Compose
   - Git

## Architecture

```
User Browser
    ↓ HTTPS
Vercel (Frontend - Next.js)
    ↓ HTTPS API Calls
Railway (Backend - FastAPI)
    ↓ PostgreSQL Connection
Neon PostgreSQL (Database)
```

## Deployment Steps

### Step 1: Local Testing with Docker

Before deploying to cloud, test locally with Docker:

```bash
# Navigate to project root
cd "phase 4"

# Build and start containers
docker-compose up --build

# Verify services
# Backend: http://localhost:8000/health
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs

# Test authentication and chat functionality

# Stop containers
docker-compose down
```

### Step 2: Deploy Backend to Railway

#### 2.1 Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your TODO app repository
6. Choose "Deploy Now"

#### 2.2 Configure Railway Settings

1. **Set Root Directory**:
   - Go to Settings → Service Settings
   - Set Root Directory: `backend`

2. **Configure Environment Variables**:
   - Go to Variables tab
   - Add the following variables:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=https://your-app.vercel.app
```

3. **Deploy**:
   - Railway will automatically detect the Dockerfile
   - Deployment starts automatically
   - Wait for deployment to complete (2-3 minutes)

4. **Get Backend URL**:
   - Go to Settings → Domains
   - Copy the Railway-provided URL (e.g., `https://your-backend.railway.app`)
   - Save this URL for frontend configuration

#### 2.3 Verify Backend Deployment

```bash
# Test health endpoint
curl https://your-backend.railway.app/health

# Expected response:
# {"status":"healthy","service":"Todo App API","version":"1.0.0","llm_provider":"groq"}

# Test API documentation
# Open: https://your-backend.railway.app/docs
```

### Step 3: Deploy Frontend to Vercel

#### 3.1 Import Project to Vercel

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Vercel will auto-detect Next.js

#### 3.2 Configure Vercel Settings

1. **Set Root Directory**:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

2. **Configure Environment Variables**:
   - Go to Settings → Environment Variables
   - Add the following variables:

```env
BACKEND_URL=https://your-backend.railway.app
BETTER_AUTH_SECRET=your_secret_key_here
BETTER_AUTH_URL=https://your-app.vercel.app
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

**Important**:
- `BETTER_AUTH_SECRET` must match backend exactly
- `BACKEND_URL` is the Railway URL from Step 2.4
- `BETTER_AUTH_URL` will be your Vercel URL (update after first deploy)

3. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete (2-3 minutes)

4. **Get Frontend URL**:
   - Copy the Vercel-provided URL (e.g., `https://your-app.vercel.app`)

#### 3.3 Update Backend CORS Configuration

After getting the Vercel URL, update Railway backend:

1. Go to Railway → Your Backend Service → Variables
2. Update `FRONTEND_URL` to your Vercel URL
3. Redeploy backend (Railway will auto-redeploy)

#### 3.4 Update Frontend Auth URL

If needed, update Vercel environment variable:

1. Go to Vercel → Settings → Environment Variables
2. Update `BETTER_AUTH_URL` to match your actual Vercel URL
3. Redeploy frontend

#### 3.5 Verify Frontend Deployment

1. Open your Vercel URL in browser
2. Test sign up / sign in
3. Test task creation
4. Test chat functionality

### Step 4: Configure CI/CD Pipeline

#### 4.1 Set Up GitHub Secrets

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

```
RAILWAY_TOKEN=your_railway_token
```

To get Railway token:
1. Go to Railway → Account Settings → Tokens
2. Create new token
3. Copy and save in GitHub secrets

#### 4.2 Enable GitHub Actions

The workflows are already created in `.github/workflows/`:
- `backend-test.yml` - Runs tests on push
- `backend-deploy.yml` - Deploys to Railway on main branch

GitHub Actions will automatically:
1. Run tests on every push
2. Deploy backend to Railway when pushing to main
3. Vercel auto-deploys frontend on every push

#### 4.3 Test CI/CD

```bash
# Make a small change to backend
echo "# Test" >> backend/README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main

# Check GitHub Actions tab for workflow status
# Check Railway for automatic deployment
# Check Vercel for automatic deployment
```

### Step 5: Configure Monitoring

#### 5.1 Railway Monitoring

1. Go to Railway → Your Service → Metrics
2. View CPU, Memory, Network usage
3. Go to Logs tab to view application logs

#### 5.2 Vercel Monitoring

1. Go to Vercel → Your Project → Analytics
2. Enable Vercel Analytics (free tier)
3. View performance metrics and Web Vitals

#### 5.3 Neon Database Monitoring

1. Go to Neon Console → Your Project
2. View Monitoring tab for:
   - Connection count
   - Query performance
   - Storage usage

## Environment Variables Reference

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# LLM Provider
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key

# CORS
FRONTEND_URL=https://your-app.vercel.app

# Server (Railway provides this)
PORT=8000
```

### Frontend (.env)

```env
# Backend API
BACKEND_URL=https://your-backend.railway.app

# Authentication
BETTER_AUTH_SECRET=your_secret_key
BETTER_AUTH_URL=https://your-app.vercel.app

# Database
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues and solutions.

## Rollback Procedure

### Backend Rollback (Railway)

1. Go to Railway → Your Service → Deployments
2. Find the previous working deployment
3. Click "Redeploy"

### Frontend Rollback (Vercel)

1. Go to Vercel → Your Project → Deployments
2. Find the previous working deployment
3. Click "..." → "Promote to Production"

## Cost Estimation

- **Railway**: $5-10/month (free tier: $5 credit)
- **Vercel**: Free (Hobby tier)
- **Neon**: Free (existing database)
- **Total**: $0-10/month

## Security Checklist

- [ ] All environment variables configured securely
- [ ] No secrets committed to git
- [ ] HTTPS enforced on all endpoints
- [ ] CORS properly configured
- [ ] Database connection encrypted
- [ ] Rate limiting enabled
- [ ] API keys rotated regularly

## Next Steps

1. Set up custom domain (optional)
2. Configure error tracking (Sentry, etc.)
3. Set up uptime monitoring
4. Configure backup strategy
5. Document operational procedures

## Support

For issues or questions:
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Review Railway logs
- Review Vercel logs
- Check GitHub Actions workflow runs
