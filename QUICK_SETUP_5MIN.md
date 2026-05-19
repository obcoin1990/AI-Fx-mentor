# AI Chart Mentor - FASTEST Setup Ever (5 Minutes)

**⏱️ Time needed:** 5 minutes of actual clicking
**💰 Cost:** $0 (free tier)
**🎯 Result:** Full production deployment live**

---

## QUICK START (Copy-Paste These Steps)

### Step 1️⃣ Create Supabase Project (2 min)

**Do this:**
1. Open: https://supabase.com/dashboard/sign-up
2. Click **"Continue with GitHub"** (or create account)
3. Click **"New Project"**
4. Fill in:
   - **Name:** `ai-chart-mentor`
   - **Database Password:** Create strong one, save it!
   - **Region:** Pick closest region
5. Click **"Create new project"**
6. ⏳ Wait 2-3 minutes for it to create...

**Then get your credentials:**
1. Once ready, go to **Settings** (⚙️ icon left sidebar)
2. Click **API**
3. **Copy these two values** (you'll need them in 2 minutes):
   ```
   NEXT_PUBLIC_SUPABASE_URL = https://[PROJECT_ID].supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY = eyJ...
   ```
4. **Save them in a text file** (keep safe!)

**Run database setup:**
1. In Supabase, click **"SQL Editor"** (left sidebar)
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
5. You should see: `✓ Success`

✅ **Supabase is ready!**

---

### Step 2️⃣ Get Claude API Key (1 min)

**Do this:**
1. Open: https://console.anthropic.com/
2. Sign in with your account (create if needed)
3. Click **"Get API Key"** or go to API Keys section
4. Click **"Create New Key"**
5. **Copy the key** and save it:
   ```
   ANTHROPIC_API_KEY = sk-ant-xxxxxxxxxxxxx
   ```

✅ **Claude key is ready!**

---

### Step 3️⃣ Update Vercel Environment Variables (2 min)

**Do this:**
1. Open: https://vercel.com/obcoin1990s-projects
2. Click on **"frontend"** project
3. Click **"Settings"** (top menu)
4. Click **"Environment Variables"** (left sidebar)
5. **Add these 3 variables** (copy from your text file):

```
NEXT_PUBLIC_SUPABASE_URL
↓
(paste your Supabase URL)

NEXT_PUBLIC_SUPABASE_ANON_KEY
↓
(paste your Supabase anon key)

ANTHROPIC_API_KEY
↓
(paste your Claude API key)
```

6. Click **"Save"** for each one
7. Go to **"Deployments"** tab (top)
8. Find the latest deployment
9. Click **"Redeploy"** button
10. ⏳ Wait 3-5 minutes for build

---

### Step 4️⃣ Test It Works (1 min)

Once Vercel says ✅ **"Ready"**:

1. Click the deployment URL
2. Try uploading a test chart image
3. Wait for analysis
4. Should see: **Trend, Support/Resistance, Trade Scenarios**

🎉 **Done!**

---

## What You're Copying

| Value | Where to get it | Paste into Vercel as |
|-------|-----------------|---------------------|
| `https://xxxxx.supabase.co` | Supabase → Settings → API → Project URL | `NEXT_PUBLIC_SUPABASE_URL` |
| `eyJxxx...` | Supabase → Settings → API → Anon Public Key | `NEXT_PUBLIC_SUPABASE_ANON_KEY` |
| `sk-ant-xxxxx` | Anthropic Console → Create API Key | `ANTHROPIC_API_KEY` |

---

## Troubleshooting Quick Fixes

**Build fails in Vercel?**
- Make sure all 3 environment variables are set
- Click Redeploy again

**Chart upload doesn't work?**
- Wait for Vercel build to finish (check status)
- Check browser console (F12) for errors
- Reload the page

**Database doesn't log results?**
- Supabase credentials might be wrong
- Copy them again from Settings → API

---

## That's It!

**5 minutes of work = production system live** 🚀

Everything else is already done:
- ✅ Code deployed to Vercel
- ✅ API routes ready
- ✅ Database schema ready
- ✅ All dependencies installed

Just need your credentials plugged in.

---

## Support Links

- Supabase: https://supabase.com
- Anthropic: https://console.anthropic.com
- Vercel: https://vercel.com
- GitHub repo: https://github.com/obcoin1990/AI-Fx-mentor

---

**When you have 5 minutes free, do these 3 steps above and it'll be live.**

Good luck! 🎉
