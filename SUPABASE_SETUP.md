# Supabase Setup Guide - AI Chart Mentor

## Quick Start (5 minutes)

### 1. Create Supabase Project

1. Go to https://supabase.com
2. Sign up or log in
3. Click "New Project"
4. **Project Name:** `ai-chart-mentor`
5. **Database Password:** Create strong password (save it!)
6. **Region:** Choose closest to your users
7. Click "Create new project"

Wait for provisioning (2-3 minutes)...

### 2. Get Connection Strings

Once project is ready:

1. Go to **Settings** → **Database**
2. Find **Connection Strings** section
3. Copy the **URI** (PostgreSQL connection string)
4. Format: `postgresql://postgres:[PASSWORD]@db.[REGION].supabase.co:5432/postgres`

This becomes your `DATABASE_URL`

### 3. Enable Redis (Upstash Add-on)

Option A: Use Supabase Redis (if available in your region)
- Settings → Add-ons
- Search for Redis
- Click "Install"

Option B: Use Upstash (recommended, always available)
1. Go to https://upstash.com
2. Sign up with GitHub
3. Create Redis database
4. Copy connection string
5. This becomes your `REDIS_URL`

### 4. Create API Keys

1. Go to **Settings** → **API**
2. Copy **Project URL** (format: `https://[PROJECT_ID].supabase.co`)
3. Copy **anon public** key (for frontend)
4. Copy **service_role** key (for backend, keep secret!)

These become:
- `NEXT_PUBLIC_SUPABASE_URL` (frontend)
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` (frontend)
- `SUPABASE_SERVICE_ROLE_KEY` (backend only)

### 5. Initialize Database Schema

1. Go to **SQL Editor**
2. Create new query
3. Paste this SQL:

```sql
-- Create audit_logs table
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
  ip_hash VARCHAR(64),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create retention policy (30 days)
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Auto-delete logs older than 30 days
CREATE OR REPLACE FUNCTION delete_old_logs()
RETURNS void AS $$
BEGIN
  DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- Create index for faster queries
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_pair ON audit_logs(pair);
```

4. Click "Run"
5. Confirm success in output

### 6. Get Auth URL (Optional for Phase 2)

Settings → Auth → Configure
- This is for user accounts (Phase 2)
- Skip for Phase 1 MVP

---

## Environment Variables Summary

After Supabase setup, you'll have:

```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT_ID].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[ANON_KEY]
SUPABASE_SERVICE_ROLE_KEY=[SERVICE_ROLE_KEY]

# Database (from Settings → Database)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[REGION].supabase.co:5432/postgres

# Redis (from Upstash)
REDIS_URL=redis://[USERNAME]:[PASSWORD]@[HOST]:[PORT]

# Claude API
ANTHROPIC_API_KEY=sk-ant-[KEY]

# Vercel Frontend URL
NEXT_PUBLIC_API_URL=https://your-vercel-domain.vercel.app
```

---

## Verify Connection

Run this in your terminal to test database connection:

```bash
psql "postgresql://postgres:[PASSWORD]@db.[REGION].supabase.co:5432/postgres" \
  -c "SELECT NOW();"
```

Should return current timestamp. ✅

---

## What You Get

✅ PostgreSQL database (50GB free)
✅ Real-time subscriptions (optional)
✅ Built-in auth (for Phase 2)
✅ API endpoints (auto-generated)
✅ Dashboard for data management
✅ 30-day log retention (via trigger)
✅ Row-level security

---

## Cost Estimation

- **Supabase:** $0 (free tier for MVP)
- **Upstash Redis:** $0 (free tier)
- **Total:** Free for development/MVP

---

Save your credentials in a secure location. You'll need them for the next steps.
