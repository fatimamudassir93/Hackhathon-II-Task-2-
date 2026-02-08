# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### Issue: Backend won't start locally

**Symptoms:**
- Error: `ModuleNotFoundError: No module named 'src'`
- Error: `uvicorn: command not found`

**Solutions:**
1. Ensure you're in the backend directory:
   ```bash
   cd backend
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run from correct directory:
   ```bash
   uvicorn src.main:app --reload
   ```

#### Issue: Database connection fails

**Symptoms:**
- Error: `could not connect to server`
- Error: `SSL connection has been closed unexpectedly`

**Solutions:**
1. Check DATABASE_URL format:
   ```env
   # Correct format for backend
   DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require
   ```

2. Verify Neon database is running:
   - Go to Neon Console
   - Check project status
   - Verify connection string

3. Check IP whitelist in Neon:
   - Neon Console → Settings → IP Allow
   - Add `0.0.0.0/0` for development (not recommended for production)

4. Test connection:
   ```bash
   python -c "from src.database.database import engine; print('Connected!')"
   ```

#### Issue: LLM API not working

**Symptoms:**
- Error: `Invalid API key`
- Error: `Rate limit exceeded`
- Chat returns generic errors

**Solutions:**
1. Verify API key is set:
   ```bash
   echo $GROQ_API_KEY  # or OPENAI_API_KEY, GEMINI_API_KEY
   ```

2. Check LLM_PROVIDER matches your key:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_...
   ```

3. Test API key directly:
   ```bash
   curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY"
   ```

4. Check rate limits:
   - Groq: 30 requests/minute (free tier)
   - OpenAI: Varies by plan
   - Gemini: 60 requests/minute (free tier)

#### Issue: CORS errors in production

**Symptoms:**
- Error: `Access to fetch blocked by CORS policy`
- Frontend can't reach backend API

**Solutions:**
1. Verify FRONTEND_URL in Railway:
   ```env
   FRONTEND_URL=https://your-app.vercel.app
   ```

2. Check CORS middleware in main.py:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[frontend_url],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. Ensure no trailing slash in URLs:
   - ✅ `https://your-app.vercel.app`
   - ❌ `https://your-app.vercel.app/`

4. Redeploy backend after changing FRONTEND_URL

### Frontend Issues

#### Issue: Frontend won't start locally

**Symptoms:**
- Error: `Cannot find module 'next'`
- Error: `npm: command not found`

**Solutions:**
1. Install Node.js (v18+):
   - Download from https://nodejs.org

2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Check for port conflicts:
   ```bash
   # Kill process on port 3000
   # Windows
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F

   # macOS/Linux
   lsof -ti:3000 | xargs kill -9
   ```

4. Clear Next.js cache:
   ```bash
   rm -rf .next
   npm run build
   npm run dev
   ```

#### Issue: Authentication not working

**Symptoms:**
- Can't sign up or sign in
- Session not persisting
- Redirected to login repeatedly

**Solutions:**
1. Verify BETTER_AUTH_SECRET matches between frontend and backend:
   ```bash
   # Check backend
   cd backend && grep BETTER_AUTH_SECRET .env

   # Check frontend
   cd frontend && grep BETTER_AUTH_SECRET .env
   ```

2. Check BETTER_AUTH_URL matches deployment:
   ```env
   # Local
   BETTER_AUTH_URL=http://localhost:3000

   # Production
   BETTER_AUTH_URL=https://your-app.vercel.app
   ```

3. Clear browser cookies and try again

4. Check database connection (Better Auth needs DB access)

#### Issue: Backend API calls failing

**Symptoms:**
- Error: `Failed to fetch`
- Error: `Network request failed`
- 404 errors on API calls

**Solutions:**
1. Verify BACKEND_URL is correct:
   ```env
   # Local
   BACKEND_URL=http://localhost:8000

   # Production
   BACKEND_URL=https://your-backend.railway.app
   ```

2. Check backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

3. Check for typos in API endpoints

4. Verify CORS is configured (see Backend CORS section)

### Docker Issues

#### Issue: Docker build fails

**Symptoms:**
- Error: `failed to solve with frontend dockerfile.v0`
- Error: `executor failed running`

**Solutions:**
1. Check Docker is running:
   ```bash
   docker --version
   docker ps
   ```

2. Clean Docker cache:
   ```bash
   docker system prune -a
   ```

3. Build with no cache:
   ```bash
   docker build --no-cache -t todo-backend ./backend
   ```

4. Check Dockerfile syntax:
   - Ensure COPY paths are correct
   - Verify base image exists

#### Issue: Container won't start

**Symptoms:**
- Container exits immediately
- Error: `standard_init_linux.go: exec user process caused: no such file or directory`

**Solutions:**
1. Check container logs:
   ```bash
   docker logs <container_id>
   ```

2. Verify environment variables:
   ```bash
   docker-compose config
   ```

3. Test container interactively:
   ```bash
   docker run -it todo-backend /bin/bash
   ```

4. Check port conflicts:
   ```bash
   docker ps  # See what's using ports
   ```

### Deployment Issues

#### Issue: Railway deployment fails

**Symptoms:**
- Build fails in Railway
- Deployment crashes on startup
- Health check fails

**Solutions:**
1. Check Railway logs:
   - Railway Dashboard → Your Service → Logs
   - Look for error messages

2. Verify environment variables are set:
   - Railway Dashboard → Variables
   - Ensure all required vars are present

3. Check Dockerfile builds locally:
   ```bash
   cd backend
   docker build -t test .
   docker run -p 8000:8000 test
   ```

4. Verify root directory is set to `backend`

5. Check health endpoint:
   ```bash
   curl https://your-backend.railway.app/health
   ```

#### Issue: Vercel deployment fails

**Symptoms:**
- Build fails in Vercel
- 404 on deployment
- Environment variables not working

**Solutions:**
1. Check Vercel build logs:
   - Vercel Dashboard → Deployments → Click deployment
   - Review build output

2. Verify root directory is set to `frontend`

3. Check environment variables:
   - Vercel Dashboard → Settings → Environment Variables
   - Ensure all vars are set for Production

4. Test build locally:
   ```bash
   cd frontend
   npm run build
   ```

5. Check vercel.json configuration

#### Issue: Database connection from Railway/Vercel fails

**Symptoms:**
- Error: `connection refused`
- Error: `SSL required`

**Solutions:**
1. Verify DATABASE_URL includes `?sslmode=require`:
   ```env
   DATABASE_URL=postgresql+asyncpg://...?sslmode=require
   ```

2. Check Neon IP allowlist:
   - Neon Console → Settings → IP Allow
   - Add Railway/Vercel IP ranges or use `0.0.0.0/0`

3. Test connection from Railway/Vercel:
   - Use Railway/Vercel shell to test connection
   - Check Neon connection pooler settings

### CI/CD Issues

#### Issue: GitHub Actions workflow fails

**Symptoms:**
- Workflow shows red X
- Tests fail
- Deployment step fails

**Solutions:**
1. Check workflow logs:
   - GitHub → Actions → Click workflow run
   - Review each step's output

2. Verify GitHub secrets are set:
   - GitHub → Settings → Secrets and variables → Actions
   - Ensure RAILWAY_TOKEN is set

3. Test locally before pushing:
   ```bash
   # Run tests
   cd backend
   pytest tests/
   ```

4. Check workflow file syntax:
   - Ensure YAML is valid
   - Verify job dependencies

#### Issue: Railway auto-deploy not working

**Symptoms:**
- Push to main doesn't trigger deployment
- GitHub Actions succeeds but Railway doesn't update

**Solutions:**
1. Check Railway GitHub integration:
   - Railway Dashboard → Settings → GitHub
   - Reconnect if needed

2. Verify Railway CLI token:
   - Generate new token if expired
   - Update GitHub secret

3. Manual deploy as fallback:
   ```bash
   npm install -g @railway/cli
   railway login
   cd backend
   railway up
   ```

### Performance Issues

#### Issue: Slow API responses

**Symptoms:**
- Requests take > 5 seconds
- Timeouts in production

**Solutions:**
1. Check database query performance:
   - Neon Console → Monitoring
   - Look for slow queries

2. Add database indexes:
   ```sql
   CREATE INDEX idx_tasks_user_id ON tasks(user_id);
   ```

3. Enable connection pooling

4. Check Railway instance size:
   - Upgrade if needed

#### Issue: High memory usage

**Symptoms:**
- Container crashes
- Out of memory errors

**Solutions:**
1. Check Railway metrics:
   - Railway Dashboard → Metrics
   - Monitor memory usage

2. Optimize Python memory:
   - Reduce worker count
   - Add memory limits to Docker

3. Check for memory leaks:
   - Review code for unclosed connections
   - Monitor over time

## Getting Help

If issues persist:

1. **Check logs**:
   - Railway: Dashboard → Logs
   - Vercel: Dashboard → Deployments → Logs
   - Local: Terminal output

2. **Review documentation**:
   - [DEPLOYMENT.md](./DEPLOYMENT.md)
   - [ARCHITECTURE.md](./ARCHITECTURE.md)
   - [RUNBOOK.md](./RUNBOOK.md)

3. **Test components individually**:
   - Backend health: `/health`
   - Frontend: Check browser console
   - Database: Test connection directly

4. **Common debugging commands**:
   ```bash
   # Backend
   cd backend
   python -c "from src.main import app; print(app.routes)"

   # Frontend
   cd frontend
   npm run build -- --debug

   # Docker
   docker-compose logs -f

   # Database
   psql $DATABASE_URL -c "SELECT 1"
   ```

## Emergency Procedures

### Complete System Down

1. Check status pages:
   - Railway: https://railway.app/status
   - Vercel: https://vercel.com/status
   - Neon: https://neon.tech/status

2. Rollback to last working version:
   - Railway: Redeploy previous deployment
   - Vercel: Promote previous deployment

3. Check all environment variables

4. Verify database is accessible

### Data Loss Prevention

1. Neon automatic backups (point-in-time recovery)
2. Export data regularly:
   ```bash
   pg_dump $DATABASE_URL > backup.sql
   ```

3. Keep git history clean for code rollback
