# Vercel + Supabase Deployment Guide

## Architecture Overview

```
Frontend + Backend (Vercel)
├── Next.js 16 App
├── API Routes (Vercel Serverless)
│   ├── POST /api/analyze-chart (Vision API)
│   └── POST /api/reason (Reasoning API)
└── Supabase Client (for logging)
        ↓
Database & Auth (Supabase)
├── PostgreSQL (audit_logs table)
└── Authentication (Phase 2)
```

## Quick Setup (10 minutes)

### 1. Create Supabase Project

1. Go to https://supabase.com
2. Sign up with GitHub
3. Click "New Project"
4. **Name:** `ai-chart-mentor`
5. **Password:** Save this!
6. **Region:** Pick closest to you
7. Click "Create new project"
8. Wait 2-3 minutes for provisioning...

### 2. Set Up Database Schema

Once Supabase is ready:

1. Go to **SQL Editor**
2. Click **"New Query"**
3. Copy-paste this SQL:

```sql
CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  timestamp TIMESTAMP DEFAULT NOW(),
  pair VARCHAR(20) NOT NULL,
  timeframe VARCHAR(10),
  trend VARCHAR(50),
  confidence FLOAT,
  support_zones JSONB,
  resistance_zones JSONB,
  trade_scenarios JSONB,
  analysis_output JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_pair ON audit_logs(pair);
```

4. Click **"Run"**
5. Confirm success

### 3. Get Supabase Credentials

1. Go to **Settings** → **API**
2. Copy these values:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`

3. Go to **Settings** → **Database**
4. Copy the PostgreSQL connection string:
   - Format: `postgresql://postgres:[PASSWORD]@db.[REGION].supabase.co:5432/postgres`
   - This is for backup/exports (not needed for MVP)

### 4. Set Up Redis (Upstash)

For image hash caching (optional for MVP):

1. Go to https://upstash.com
2. Sign up with GitHub
3. Create Redis database
4. Copy connection string → `REDIS_URL`

**Or skip Redis for now** - use Supabase only.

### 5. Get Claude API Key

1. Go to https://console.anthropic.com
2. Create API key
3. Copy → `ANTHROPIC_API_KEY`

### 6. Update Frontend Code (Already Done ✅)

Files already created:
- ✅ `frontend/app/api/analyze-chart/route.ts` (Vision API)
- ✅ `frontend/app/api/reason/route.ts` (Reasoning API)
- ✅ `frontend/lib/supabase.ts` (Supabase client)
- ✅ `frontend/lib/api.ts` (Updated for Vercel)
- ✅ `frontend/package.json` (Supabase + Anthropic deps added)

### 7. Deploy to Vercel

1. Go to https://vercel.com
2. Log in with GitHub
3. Click **"Add New"** → **"Project"**
4. Select **`obcoin1990/AI-Fx-mentor`**
5. Click **"Import"**
6. Configure settings:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend` (if needed)
7. Click **"Environment Variables"**
8. Add these:

```
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT_ID].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[ANON_KEY]
ANTHROPIC_API_KEY=sk-ant-[YOUR_KEY]
```

9. Click **"Deploy"**
10. Wait 3-5 minutes for build

### 8. Verify Deployment

Once Vercel shows "✅ Ready":

1. Go to deployment URL (provided by Vercel)
2. Try uploading a test chart
3. Should see analysis results
4. Check browser console for any errors

---

## Environment Variables Reference

### Frontend (.env.local or Vercel)

```
# Supabase (public - safe to expose)
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT_ID].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[ANON_KEY]

# Claude API (secret - Vercel serverless only)
ANTHROPIC_API_KEY=sk-ant-[YOUR_KEY]

# Optional: Redis for caching
REDIS_URL=redis://[USER]:[PASS]@[HOST]:[PORT]
```

### Supabase Project Settings

Location: **Settings** → **API**
- Copy **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
- Copy **anon key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Copy **service_role key** (keep secret, not needed for MVP)

---

## How It Works

### Request Flow

```
1. User uploads chart in browser
   ↓
2. Frontend calls POST /api/analyze-chart
   ↓
3. Vercel serverless function receives image
   ↓
4. Function calls Claude Vision API
   ↓
5. Claude analyzes chart, returns structured JSON
   ↓
6. Function logs result to Supabase
   ↓
7. Function returns analysis to frontend
   ↓
8. Frontend calls POST /api/reason with analysis
   ↓
9. Vercel serverless function receives analysis
   ↓
10. Function calls Claude Reasoning API
   ↓
11. Claude generates trade scenarios
   ↓
12. Function returns scenarios to frontend
   ↓
13. Frontend displays results
```

### Data Storage

- **Charts:** NOT stored (deleted after Vision API call)
- **Analysis JSON:** Stored in Supabase `audit_logs` table
- **Retention:** 30 days (auto-delete via trigger)
- **Privacy:** No PII, no images, only analysis output

---

## Deployment Checklist

- [ ] Supabase project created
- [ ] Database schema initialized
- [ ] Supabase credentials copied
- [ ] Claude API key obtained
- [ ] Frontend code updated (already done ✅)
- [ ] Vercel project created
- [ ] Environment variables added to Vercel
- [ ] Deployment triggered
- [ ] Build successful
- [ ] Health check passed (upload test chart)
- [ ] Analysis results displayed correctly

---

## Troubleshooting

### Build Fails in Vercel

**Error:** "Cannot find module '@supabase/supabase-js'"

**Solution:**
1. Go to Vercel dashboard
2. Settings → Environment Variables
3. Make sure all vars are set
4. Redeploy

**Error:** "ANTHROPIC_API_KEY is not set"

**Solution:**
1. Vercel dashboard → Settings → Environment Variables
2. Add: `ANTHROPIC_API_KEY=sk-ant-xxxxx`
3. Redeploy

### Chart Upload Fails

**Error:** "Failed to connect to analysis server"

**Solution:**
1. Check browser console (F12)
2. Verify Vercel deployment is "Ready"
3. Try reloading the page
4. Check if Claude API key is valid

### Analysis Doesn't Log to Database

**Error:** Nothing shows in Supabase `audit_logs` table

**Solution:**
1. Check Vercel function logs
2. Verify Supabase credentials in environment
3. Confirm database schema was created
4. Check Supabase audit logs for SQL errors

---

## Monitoring

### Vercel Logs

1. Vercel dashboard → Select project
2. Click **"Logs"** tab
3. Search for errors
4. Monitor request count and latency

### Supabase Logs

1. Supabase dashboard → Select project
2. Click **"Logs"** in left menu
3. Filter by table: `audit_logs`
4. Check for INSERT operations

### Cost Estimation (Monthly)

- **Vercel:** $20 (Pro plan, or free for hobby)
- **Supabase:** $0 (free tier includes 500MB DB)
- **Claude API:** $0-50 (depends on usage)
- **Upstash Redis:** $0 (free tier)
- **Total:** ~$20-70/month

---

## Scaling (Post-MVP)

### Add User Accounts (Phase 2)

1. Supabase Auth is built-in
2. Enable in Settings → Auth
3. Add login/signup pages to Next.js
4. Create `users` table in Supabase
5. Link analyses to user_id

### Increase Database Size

1. Supabase dashboard → Billing
2. Upgrade from free tier
3. Automatic scaling

### Add More API Routes

1. Create new files in `frontend/app/api/`
2. They auto-deploy to Vercel
3. Each is a separate serverless function

---

## Files Modified/Created

✅ Frontend API Routes (Vercel serverless):
- `frontend/app/api/analyze-chart/route.ts` (Vision API)
- `frontend/app/api/reason/route.ts` (Reasoning API)

✅ Database Client:
- `frontend/lib/supabase.ts` (Supabase integration)

✅ Updated API Client:
- `frontend/lib/api.ts` (Updated for Vercel routes)

✅ Configuration:
- `frontend/package.json` (Added dependencies)
- `SUPABASE_SETUP.md` (This file)

---

## Next Steps

1. **Create Supabase project** (https://supabase.com)
2. **Get Supabase credentials** (URL + anon key)
3. **Get Claude API key** (https://console.anthropic.com)
4. **Deploy to Vercel** with environment variables
5. **Test end-to-end** (upload chart → get analysis)
6. **Monitor logs** for any errors

---

## Deploy Now

```bash
# All code is ready. Just need to:
# 1. Push latest code to GitHub
git add .
git commit -m "feat: add Vercel serverless API routes + Supabase integration"
git push origin main

# 2. Create Supabase project
# 3. Create environment variables
# 4. Redeploy Vercel
```

---

**Everything is now integrated: Vercel (frontend + backend) + Supabase (database).** 🚀

No separate backend server needed. Simpler, cheaper, faster.
