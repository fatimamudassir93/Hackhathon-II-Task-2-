# Operations Runbook

## Daily Operations

### Health Checks

**Morning Checklist:**
```bash
# 1. Check backend health
curl https://your-backend.railway.app/health

# Expected: {"status":"healthy","service":"Todo App API","version":"1.0.0","llm_provider":"groq"}

# 2. Check frontend
curl -I https://your-app.vercel.app

# Expected: HTTP/2 200

# 3. Check database
# Neon Console → Monitoring → Check connection count and query performance
```

### Monitoring Dashboards

**Railway (Backend):**
- URL: https://railway.app/dashboard
- Check: CPU, Memory, Network usage
- Alert threshold: CPU > 80%, Memory > 90%

**Vercel (Frontend):**
- URL: https://vercel.com/dashboard
- Check: Analytics, Web Vitals, Error rate
- Alert threshold: Error rate > 5%

**Neon (Database):**
- URL: https://console.neon.tech
- Check: Connection count, Storage usage
- Alert threshold: Connections > 80, Storage > 400MB (free tier)

## Common Operations

### Restart Services

**Backend (Railway):**
```bash
# Via Dashboard
1. Go to Railway Dashboard
2. Select your service
3. Click "Restart"

# Via CLI
railway restart --service backend
```

**Frontend (Vercel):**
```bash
# Redeploy current version
vercel --prod

# Or via dashboard
1. Go to Vercel Dashboard
2. Deployments → Latest → Redeploy
```

### Update Environment Variables

**Backend (Railway):**
```bash
# Via Dashboard
1. Railway Dashboard → Variables
2. Add/Edit variable
3. Service auto-restarts

# Via CLI
railway variables set KEY=value
```

**Frontend (Vercel):**
```bash
# Via Dashboard
1. Vercel Dashboard → Settings → Environment Variables
2. Add/Edit variable
3. Redeploy to apply changes

# Via CLI
vercel env add KEY production
```

### View Logs

**Backend Logs:**
```bash
# Via Railway Dashboard
Railway Dashboard → Logs → Filter by level

# Via CLI
railway logs --service backend

# Follow logs in real-time
railway logs --service backend --follow
```

**Frontend Logs:**
```bash
# Via Vercel Dashboard
Vercel Dashboard → Deployments → Click deployment → Logs

# Via CLI
vercel logs https://your-app.vercel.app
```

**Database Logs:**
```bash
# Via Neon Console
Neon Console → Monitoring → Query logs
```

### Deploy New Version

**Backend:**
```bash
# 1. Commit changes
git add .
git commit -m "Update backend"

# 2. Push to main (triggers CI/CD)
git push origin main

# 3. Monitor deployment
# GitHub Actions → Watch workflow
# Railway Dashboard → Watch deployment

# 4. Verify deployment
curl https://your-backend.railway.app/health
```

**Frontend:**
```bash
# 1. Commit changes
git add .
git commit -m "Update frontend"

# 2. Push to main (triggers auto-deploy)
git push origin main

# 3. Monitor deployment
# Vercel Dashboard → Deployments

# 4. Verify deployment
curl -I https://your-app.vercel.app
```

### Rollback Deployment

**Backend Rollback:**
```bash
# Via Railway Dashboard
1. Railway Dashboard → Deployments
2. Find previous working deployment
3. Click "Redeploy"

# Via Git
git revert HEAD
git push origin main
```

**Frontend Rollback:**
```bash
# Via Vercel Dashboard (Instant)
1. Vercel Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

# Via Git
git revert HEAD
git push origin main
```

## Incident Response

### Backend Down

**Symptoms:**
- Health check fails
- 502/503 errors
- Railway shows "Crashed"

**Response:**
```bash
# 1. Check Railway status
https://railway.app/status

# 2. Check logs
railway logs --service backend | tail -100

# 3. Check environment variables
railway variables list

# 4. Restart service
railway restart --service backend

# 5. If restart fails, rollback
# Railway Dashboard → Deployments → Redeploy previous

# 6. Check database connection
# Verify DATABASE_URL is correct
# Check Neon status
```

### Frontend Down

**Symptoms:**
- Site unreachable
- 404 errors
- Vercel shows "Failed"

**Response:**
```bash
# 1. Check Vercel status
https://vercel.com/status

# 2. Check deployment logs
vercel logs https://your-app.vercel.app

# 3. Check environment variables
# Vercel Dashboard → Settings → Environment Variables

# 4. Redeploy
vercel --prod

# 5. If redeploy fails, rollback
# Vercel Dashboard → Deployments → Promote previous
```

### Database Issues

**Symptoms:**
- Connection timeouts
- Slow queries
- High connection count

**Response:**
```bash
# 1. Check Neon status
https://neon.tech/status

# 2. Check connection count
# Neon Console → Monitoring → Connections

# 3. Check slow queries
# Neon Console → Monitoring → Query performance

# 4. If connections maxed out:
# - Restart backend to clear connections
# - Check for connection leaks in code

# 5. If storage full:
# - Clean up old data
# - Upgrade Neon plan
```

### LLM API Issues

**Symptoms:**
- Chat not responding
- API key errors
- Rate limit errors

**Response:**
```bash
# 1. Check API key
railway variables get GROQ_API_KEY

# 2. Test API key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"

# 3. Check rate limits
# Groq Console → Usage

# 4. Switch provider if needed
railway variables set LLM_PROVIDER=openai
railway variables set OPENAI_API_KEY=sk-...
railway restart
```

## Maintenance Tasks

### Weekly Tasks

**Every Monday:**
- [ ] Review error logs from past week
- [ ] Check resource usage trends
- [ ] Verify backups are working
- [ ] Review security alerts

**Commands:**
```bash
# Check error rate
railway logs --service backend | grep ERROR | wc -l

# Check resource usage
# Railway Dashboard → Metrics → Past 7 days

# Verify database backup
# Neon Console → Backups → Check latest
```

### Monthly Tasks

**First of Month:**
- [ ] Review and rotate API keys
- [ ] Check for dependency updates
- [ ] Review cost and usage
- [ ] Update documentation

**Commands:**
```bash
# Check for updates
cd backend && pip list --outdated
cd frontend && npm outdated

# Review costs
# Railway Dashboard → Usage
# Vercel Dashboard → Usage
# Neon Console → Billing
```

### Quarterly Tasks

**Every 3 Months:**
- [ ] Security audit
- [ ] Performance review
- [ ] Disaster recovery test
- [ ] Update runbook

## Performance Optimization

### Backend Optimization

**Check slow endpoints:**
```bash
# Review logs for slow requests
railway logs | grep "took" | sort -n

# Add indexes for slow queries
psql $DATABASE_URL -c "CREATE INDEX idx_tasks_user_id ON tasks(user_id);"
```

**Optimize database queries:**
```python
# Use select_related for joins
# Add pagination for large result sets
# Cache frequently accessed data
```

### Frontend Optimization

**Check Web Vitals:**
```bash
# Vercel Dashboard → Analytics → Web Vitals
# Target: LCP < 2.5s, FID < 100ms, CLS < 0.1
```

**Optimize bundle size:**
```bash
cd frontend
npm run build -- --analyze
```

## Security Operations

### Rotate Secrets

**Every 90 days:**
```bash
# 1. Generate new secret
openssl rand -base64 32

# 2. Update backend
railway variables set BETTER_AUTH_SECRET=new_secret

# 3. Update frontend
vercel env add BETTER_AUTH_SECRET production
# Enter new secret when prompted

# 4. Redeploy both services
```

### Review Access

**Monthly:**
- [ ] Review Railway team members
- [ ] Review Vercel team members
- [ ] Review Neon project access
- [ ] Review GitHub repository access

### Security Monitoring

**Check for vulnerabilities:**
```bash
# Backend
cd backend
pip-audit

# Frontend
cd frontend
npm audit
```

## Backup and Recovery

### Database Backup

**Manual backup:**
```bash
# Export database
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Compress
gzip backup_$(date +%Y%m%d).sql

# Store securely (S3, Google Drive, etc.)
```

**Restore from backup:**
```bash
# Decompress
gunzip backup_20260208.sql.gz

# Restore
psql $DATABASE_URL < backup_20260208.sql
```

**Point-in-time recovery (Neon):**
```bash
# Via Neon Console
1. Neon Console → Branches
2. Create branch from specific timestamp
3. Test on branch
4. Promote to main if successful
```

### Code Backup

**Git is the source of truth:**
```bash
# Ensure all changes are committed
git status

# Push to remote
git push origin main

# Tag releases
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0
```

## Scaling Operations

### Horizontal Scaling (Backend)

**When to scale:**
- CPU consistently > 80%
- Response time > 2s
- Request queue building up

**How to scale:**
```bash
# Railway Dashboard
1. Settings → Scaling
2. Increase replicas
3. Monitor performance
```

### Database Scaling

**When to scale:**
- Connection count > 80% of limit
- Storage > 80% of limit
- Query performance degrading

**How to scale:**
```bash
# Neon Console
1. Project Settings → Compute
2. Upgrade compute size
3. Enable autoscaling
```

## Contact Information

**On-Call Rotation:**
- Primary: [Name] - [Contact]
- Secondary: [Name] - [Contact]

**Escalation:**
- Level 1: Team Lead
- Level 2: Engineering Manager
- Level 3: CTO

**External Support:**
- Railway: support@railway.app
- Vercel: support@vercel.com
- Neon: support@neon.tech

## Useful Links

- **Railway Dashboard**: https://railway.app/dashboard
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Neon Console**: https://console.neon.tech
- **GitHub Repository**: [Your repo URL]
- **Documentation**: [Your docs URL]
- **Status Pages**:
  - Railway: https://railway.app/status
  - Vercel: https://vercel.com/status
  - Neon: https://neon.tech/status
