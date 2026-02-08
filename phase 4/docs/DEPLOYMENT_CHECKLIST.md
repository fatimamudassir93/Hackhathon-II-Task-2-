# Deployment Checklist

## Pre-Deployment

### Code Preparation
- [ ] All changes committed to git
- [ ] Code reviewed and approved
- [ ] Tests passing locally
- [ ] No secrets in code
- [ ] Dependencies up to date
- [ ] Documentation updated

### Environment Setup
- [ ] Railway account created
- [ ] Vercel account created
- [ ] GitHub repository accessible
- [ ] Neon database accessible
- [ ] LLM API keys obtained

### Local Testing
- [ ] Backend starts successfully
- [ ] Frontend starts successfully
- [ ] Database connection works
- [ ] Authentication flow works
- [ ] Chat functionality works
- [ ] Docker builds successfully
- [ ] docker-compose up works

## Backend Deployment (Railway)

### Configuration
- [ ] Railway project created
- [ ] GitHub repository connected
- [ ] Root directory set to `backend`
- [ ] Dockerfile detected

### Environment Variables
- [ ] DATABASE_URL configured
- [ ] BETTER_AUTH_SECRET configured
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES set
- [ ] LLM_PROVIDER configured
- [ ] GROQ_API_KEY (or other LLM key) configured
- [ ] FRONTEND_URL configured
- [ ] All variables match .env.example

### Deployment
- [ ] Initial deployment triggered
- [ ] Build completed successfully
- [ ] Health check passing
- [ ] Backend URL obtained
- [ ] Backend URL saved for frontend config

### Verification
- [ ] Health endpoint accessible: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Database connection working
- [ ] Authentication endpoints working
- [ ] No errors in Railway logs

## Frontend Deployment (Vercel)

### Configuration
- [ ] Vercel project created
- [ ] GitHub repository imported
- [ ] Framework preset: Next.js
- [ ] Root directory set to `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `.next`

### Environment Variables
- [ ] BACKEND_URL configured (Railway URL)
- [ ] BETTER_AUTH_SECRET configured (matches backend)
- [ ] BETTER_AUTH_URL configured
- [ ] DATABASE_URL configured
- [ ] All variables match .env.example

### Deployment
- [ ] Initial deployment triggered
- [ ] Build completed successfully
- [ ] Frontend URL obtained
- [ ] Frontend URL saved

### Post-Deployment Updates
- [ ] Update Railway FRONTEND_URL with Vercel URL
- [ ] Redeploy Railway backend
- [ ] Update Vercel BETTER_AUTH_URL if needed
- [ ] Redeploy Vercel frontend if needed

### Verification
- [ ] Frontend accessible via Vercel URL
- [ ] Sign up works
- [ ] Sign in works
- [ ] Session persists
- [ ] Task CRUD operations work
- [ ] Chat interface works
- [ ] No CORS errors
- [ ] No errors in Vercel logs

## CI/CD Setup

### GitHub Secrets
- [ ] RAILWAY_TOKEN added to GitHub secrets
- [ ] Token has correct permissions

### Workflows
- [ ] .github/workflows/backend-test.yml exists
- [ ] .github/workflows/backend-deploy.yml exists
- [ ] Workflows enabled in GitHub

### Testing
- [ ] Push to test branch triggers tests
- [ ] Push to main triggers deployment
- [ ] Deployment succeeds
- [ ] Notifications working (if configured)

## Monitoring Setup

### Railway
- [ ] Metrics dashboard accessible
- [ ] Logs accessible
- [ ] Health checks configured
- [ ] Alerts configured (if available)

### Vercel
- [ ] Analytics enabled
- [ ] Web Vitals tracking enabled
- [ ] Error tracking enabled
- [ ] Logs accessible

### Neon
- [ ] Monitoring dashboard accessible
- [ ] Connection count visible
- [ ] Query performance visible
- [ ] Storage usage visible

## Documentation

### Created
- [ ] DEPLOYMENT.md complete
- [ ] ARCHITECTURE.md complete
- [ ] TROUBLESHOOTING.md complete
- [ ] RUNBOOK.md complete
- [ ] README.md updated

### Reviewed
- [ ] All documentation accurate
- [ ] URLs updated to production
- [ ] Screenshots current (if any)
- [ ] Contact information current

## Security

### Secrets Management
- [ ] No secrets in git history
- [ ] .env files in .gitignore
- [ ] .env.example files created
- [ ] All secrets documented

### Access Control
- [ ] Railway access limited
- [ ] Vercel access limited
- [ ] Neon access limited
- [ ] GitHub access limited

### Security Features
- [ ] HTTPS enforced
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Input validation working
- [ ] SQL injection prevention verified

## Post-Deployment

### Smoke Tests
- [ ] Sign up new user
- [ ] Sign in with new user
- [ ] Create task
- [ ] Update task
- [ ] Complete task
- [ ] Delete task
- [ ] Send chat message
- [ ] Verify chat response
- [ ] Test with different LLM provider

### Performance
- [ ] Response times acceptable (< 2s)
- [ ] No memory leaks
- [ ] No connection leaks
- [ ] Resource usage normal

### Monitoring
- [ ] Check logs for errors
- [ ] Verify metrics collecting
- [ ] Test alerting (if configured)

## Rollback Plan

### Preparation
- [ ] Previous deployment IDs noted
- [ ] Rollback procedure documented
- [ ] Team notified of deployment

### If Issues Occur
- [ ] Railway: Redeploy previous version
- [ ] Vercel: Promote previous deployment
- [ ] Database: Point-in-time recovery available
- [ ] Team notified of rollback

## Sign-Off

### Deployment Team
- [ ] Developer: _________________ Date: _______
- [ ] Reviewer: _________________ Date: _______
- [ ] Operations: _______________ Date: _______

### Production Readiness
- [ ] All checklist items completed
- [ ] No critical issues outstanding
- [ ] Monitoring confirmed working
- [ ] Documentation complete
- [ ] Team trained on operations

### Go-Live
- [ ] Deployment time scheduled
- [ ] Stakeholders notified
- [ ] Support team ready
- [ ] Rollback plan ready

---

## Quick Reference

### URLs
- **Backend**: https://your-backend.railway.app
- **Frontend**: https://your-app.vercel.app
- **API Docs**: https://your-backend.railway.app/docs
- **Railway Dashboard**: https://railway.app/dashboard
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Neon Console**: https://console.neon.tech

### Key Commands
```bash
# Check backend health
curl https://your-backend.railway.app/health

# Check frontend
curl -I https://your-app.vercel.app

# View Railway logs
railway logs --service backend

# View Vercel logs
vercel logs https://your-app.vercel.app

# Rollback Railway
# Dashboard → Deployments → Redeploy previous

# Rollback Vercel
# Dashboard → Deployments → Promote previous
```

### Emergency Contacts
- On-Call: [Contact]
- Team Lead: [Contact]
- Railway Support: support@railway.app
- Vercel Support: support@vercel.com
- Neon Support: support@neon.tech
