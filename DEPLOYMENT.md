# Deployment Guide - AI Chart Mentor

## Production Deployment

### Frontend (Vercel) ✅ LIVE

**Status:** Deployed to production  
**URL:** https://frontend-dd6zzb65j-obcoin1990s-projects.vercel.app  
**Alternate:** https://frontend-black-two-69.vercel.app

### Backend (Railway) - Setup Instructions

The backend is ready for deployment to Railway. Follow these steps:

## Prerequisites

1. **Railway Account** - Create one at https://railway.app
2. **GitHub Repository** - Already set up: https://github.com/obcoin1990/AI-Fx-mentor
3. **Claude API Key** - Get from https://console.anthropic.com
4. **Railway CLI** (optional) - For local deployments

## Quick Setup (via Railway Dashboard)

1. **Create New Project**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose `obcoin1990/AI-Fx-mentor` repository
   - Select the `main` branch

2. **Add Services**

   **PostgreSQL Database:**
   - Click "Add Service" → "Database" → PostgreSQL
   - Railway will auto-generate `DATABASE_URL`

   **Redis Cache:**
   - Click "Add Service" → "Redis"
   - Railway will auto-generate `REDIS_URL`

   **Backend (FastAPI):**
   - Click "Add Service" → GitHub Repo
   - Link to your forked repo
   - Root directory: `.` (root)
   - Dockerfile: `./Dockerfile`

3. **Environment Variables**

   In the Backend service settings, add:

   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   BACKEND_CORS_ORIGINS=https://frontend-dd6zzb65j-obcoin1990s-projects.vercel.app,https://frontend-black-two-69.vercel.app
   DEBUG=false
   PYTHON_VERSION=3.11
   PYTHONUNBUFFERED=1
   ```

   Database and Redis URLs are auto-populated by Railway.

4. **Deploy**
   - Railway auto-deploys from GitHub on push
   - Or manually deploy via "Deploy" button
   - Check build logs for errors

5. **Verify Deployment**
   - Visit `https://<your-backend-url>/health` (should return 200)
   - Visit `https://<your-backend-url>/docs` (Swagger UI)
   - Check logs in Railway dashboard

## Environment Variables Reference

| Variable | Example | Source |
|----------|---------|--------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Anthropic Console |
| `DATABASE_URL` | Auto-generated | Railway PostgreSQL |
| `REDIS_URL` | Auto-generated | Railway Redis |
| `BACKEND_CORS_ORIGINS` | Frontend URLs | Vercel deployment |
| `DEBUG` | `false` | Keep false in production |
| `PYTHONUNBUFFERED` | `1` | For streaming logs |

## Connect Frontend to Backend

Once backend is deployed:

1. **Get Backend URL** from Railway dashboard
   - Format: `https://your-project-backend-xxxx.up.railway.app`

2. **Update Frontend Environment**
   - Vercel Dashboard → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL=https://your-backend-url`
   - Redeploy frontend

3. **Test Connection**
   - Open frontend in browser
   - Upload a test chart
   - Check browser console for API calls
   - Should see Vision API response

## Troubleshooting

### Build Fails
- Check Python version (3.11 required)
- Verify Dockerfile syntax
- Check `pyproject.toml` or `requirements.txt`

### Health Check Fails
- Verify `HEALTHCHECK` in Dockerfile
- Check if port 8000 is exposed
- Review startup logs in Railway

### CORS Errors
- Update `BACKEND_CORS_ORIGINS` with frontend URL
- Restart backend service

### API Connection Fails
- Verify `NEXT_PUBLIC_API_URL` in frontend
- Check that backend service is running
- Test with `curl https://backend-url/health`

## Scaling

After MVP validation:

1. **Increase resource limits** in Railway dashboard
2. **Monitor performance** via Sentry integration
3. **Optimize database queries** based on logs
4. **Increase Redis memory** if cache misses increase

## Monitoring & Logs

### Railway Logs
- Check "Logs" tab in service settings
- Real-time streaming of stdout/stderr
- Search by keyword (errors, warnings)

### Sentry Integration (Optional)
1. Create Sentry account at https://sentry.io
2. Add `SENTRY_DSN` to environment variables
3. Errors automatically reported with context

## Cost Estimation (Monthly)

- **PostgreSQL:** $10-20 (small database)
- **Redis:** $5-10 (caching)
- **Backend:** $10-20 (compute)
- **Total:** ~$25-50/month for MVP load

## CI/CD Pipeline

Push to `main` branch on GitHub:
1. GitHub Actions runs tests (optional)
2. Railway auto-deploys frontend + backend
3. Health checks verify services
4. Logs visible in Railway dashboard

## Manual Deployment (CLI)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to project
railway link

# Deploy
railway deploy

# Check status
railway status

# View logs
railway logs
```

## Rollback

If deployment breaks:

1. Go to Railway dashboard
2. Select service → "Deployments" tab
3. Click previous successful deployment
4. Click "Redeploy"

## Next Steps

After successful deployment:

1. **User Testing** - Beta test with 5-10 traders
2. **Performance Validation** - Verify <5s response time
3. **Accuracy Validation** - Test Vision/Reasoning quality
4. **Monitor for Issues** - Check logs daily
5. **Iterate** - Fix bugs, optimize prompts

---

**Phase 1 Backend Deployment Ready** ✅

All infrastructure, code, and configuration is in place.
Ready for production deployment to Railway.
