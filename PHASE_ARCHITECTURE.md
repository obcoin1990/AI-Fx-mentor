# AI Chart Mentor: Phase-Specific Architecture

## Phase 1 (MVP) - Stateless Analysis

### Architecture Overview

```
+-------------------------------------------------------------+
¦                    USER BROWSER                             ¦
¦  +---------------------------------------------------------+ ¦
¦  ¦          Next.js Client Application                     ¦ ¦
¦  ¦  +- ChartUpload component                              ¦ ¦
¦  ¦  +- AnalysisDisplay components                         ¦ ¦
¦  ¦  +- Error handling                                     ¦ ¦
¦  +---------------------------------------------------------+ ¦
+------------+-------------------------------------------------+
             ¦ HTTP POST /api/analyze-chart
             ?
+-------------------------------------------------------------+
¦                   VERCEL EDGE NETWORK                        ¦
¦  +---------------------------------------------------------+ ¦
¦  ¦        Next.js API Route: /api/analyze-chart            ¦ ¦
¦  ¦                                                         ¦ ¦
¦  ¦  1. Validate & parse multipart form                    ¦ ¦
¦  ¦  2. Call Vision Service                                ¦ ¦
¦  ¦  3. Validate extraction                                ¦ ¦
¦  ¦  4. Call Reasoning Service                             ¦ ¦
¦  ¦  5. Return formatted response                          ¦ ¦
¦  +---------------------------------------------------------+ ¦
+-------------+----------------------+------------+------------+
              ¦                      ¦            ¦
   API Keys in env vars              ¦            ¦
         ANTHROPIC_API_KEY           ¦            ¦
              ¦                      ¦            ¦
              ?                      ?            ?
         +-------------+       +----------+  +------------+
         ¦   Claude    ¦       ¦  Vision  ¦  ¦ Reasoning  ¦
         ¦   Vision    ¦       ¦ Service  ¦  ¦  Service   ¦
         ¦   API       ¦       ¦ (local)  ¦  ¦  (local)   ¦
         ¦             ¦       ¦          ¦  ¦            ¦
         ¦ Image ?     ¦-------¦ Extract  ¦  ¦ Analyze    ¦
         ¦ JSON        ¦       ¦ Data     ¦  ¦ & Generate ¦
         +-------------+       ¦          ¦  ¦ Ideas      ¦
                               +----------+  +------------+
                                    ¦              ¦
                               Claude             Claude
                               Vision API         Sonnet API
                               (v1/messages)      (v1/messages)
```

### Data Flow Phase 1

```
Input: User uploads chart.png (2MB)

Step 1: Client-side validation (Browser)
+- Is file PNG/JPG? ?
+- Is size < 10MB? ?
+- Does image look like a chart? ?
+- Post to /api/analyze-chart

Step 2: Server validation
+- Parse multipart form
+- Is file present? ?
+- MIME type check
+- Size bounds check (1KB-10MB)
+- Continue or return 400

Step 3: Image preprocessing
+- Convert to buffer
+- Check dimensions (400x300 to 4000x4000)
+- Auto-rotate if needed (EXIF)
+- Compress to base64 (~1-2MB)

Step 4: Vision extraction (5-10 seconds)
+- POST to Claude Vision API
+- Include base64 image
+- Request JSON extraction
+- Parse response
+- Validate schema (Zod)

Vision returns:
{
  trend: "bullish",
  support_zones: [{level_min: 1.082, level_max: 1.083}],
  resistance_zones: [{level_min: 1.091, level_max: 1.092}],
  confidence: 0.87
}

Step 5: Validation checkpoint
+- Required fields present? ?
+- Numbers are reasonable? ?
+- Confidence > 40%? ?
+- Continue or return 502

Step 6: Reasoning (3-5 seconds)
+- Format extraction as context
+- POST to Claude 3.5 Sonnet
+- Request trade ideas + mentor note
+- Parse response
+- Return analysis

Reasoning returns:
{
  idea: {
    direction: "buy",
    entry: "1.0835",
    stop_loss: 1.0800,
    take_profit: 1.0920,
    risk_reward: "1:3",
    rationale: "..."
  },
  mentor_note: "..."
}

Step 7: Format response
+- Return 200 OK with JSON

Output: AnalysisResponse JSON
+- Client displays trend, S/R, idea, mentor note

Total time: ~10-20 seconds
```

### Deployment Phase 1

```
GitHub Repository
    ¦
    +- git push
    ?
GitHub Actions (CI)
    +- Run tests
    +- Lint code
    +- Build
    
    ? (if pass)
    
Vercel (CD)
    +- Deploy Next.js app
    +- Set environment variables
    ¦  +- ANTHROPIC_API_KEY
    ¦  +- Others (if any)
    +- Live at: ai-chart-mentor.vercel.app

Client browsers connect to:
    https://ai-chart-mentor.vercel.app/api/analyze-chart
```

### Storage Phase 1

```
Stateless ? No database needed

Temporary storage:
+- Image buffer (in RAM during request)
+- Extraction JSON (in RAM)
+- Analysis result (in response, then discarded)

No persistence:
+- No user accounts
+- No history
+- No session state
+- No file storage
```

---

## Phase 2 (Scale + Accounts) - Stateful with Persistence

### Architecture Evolution

```
PHASE 1 ? PHASE 2 Changes:

Add:
+- Supabase (PostgreSQL + Auth)
+- Redis (Upstash for cache)
+- Job queue (Bull/Redis)
+- Image storage (S3 or Vercel Blob)

Existing:
+- Next.js API routes (extended)
+- Claude Vision & Sonnet APIs (same)
+- Vercel deployment (same)
+- Frontend (enhanced with auth)
```

### Phase 2 Architecture

```
+-------------------------------------------------------------+
¦                    USER BROWSER                             ¦
¦  Next.js Client (Enhanced)                                  ¦
¦  +- Login / Register                                        ¦
¦  +- ChartUpload (same as Phase 1)                          ¦
¦  +- History dashboard                                       ¦
¦  +- Multi-timeframe UI                                      ¦
+-------------------------------------------------------------+
             ¦ HTTP (with auth token)
             ?
+-------------------------------------------------------------+
¦                   VERCEL EDGE NETWORK                        ¦
¦  Next.js API Routes (Extended)                              ¦
¦  +- /api/auth/* (Supabase auth)                            ¦
¦  +- /api/analyze-chart (same, +caching)                    ¦
¦  +- /api/analyze-chart-async (queue-based)                 ¦
¦  +- /api/history (user's analyses)                         ¦
¦  +- /api/user/profile                                       ¦
¦  +- /api/analysis/{id} (single analysis)                   ¦
+------------------------------------------------------------+
           ¦                      ¦
           ?                      ?
    +-------------+        +----------------+
    ¦   Supabase  ¦        ¦  Redis/Upstash ¦
    ¦ (Auth + DB) ¦        ¦   (Cache +     ¦
    ¦             ¦        ¦    Queue)      ¦
    ¦ Tables:     ¦        ¦                ¦
    ¦ - users     ¦        ¦ - Image cache  ¦
    ¦ - analyses  ¦        ¦ - Rate limits  ¦
    ¦ - sessions  ¦        ¦ - Job queue    ¦
    +-------------+        +----------------+
           ¦                      ¦
           ¦                      ?
           ¦                +-------------+
           ¦                ¦ Bull Queue  ¦
           ¦                ¦  Worker     ¦
           ¦                ¦             ¦
           ¦                ¦ Process:    ¦
           ¦                ¦ - Vision    ¦
           ¦                ¦ - Reasoning ¦
           ¦                ¦ - Store DB  ¦
           ¦                +-------------+
           ¦                       ¦
           ?                       ?
      +----------------------------------+
      ¦   Claude APIs                    ¦
      ¦   (Vision + Sonnet)              ¦
      +----------------------------------+

Additional (optional):
+- S3 or Vercel Blob (store chart images)
+- Sentry (error tracking)
+- Datadog (monitoring)
+- GitHub Actions (CI/CD)
```

### Phase 2 Data Model

```sql
-- users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  tier TEXT DEFAULT 'free', -- free, pro, enterprise
  monthly_analyses INT DEFAULT 0
);

-- chart_analyses table
CREATE TABLE chart_analyses (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  image_hash TEXT, -- for caching
  image_url TEXT, -- S3 URL
  trend TEXT, -- bullish, bearish, ranging
  support JSONB, -- array of zones
  resistance JSONB, -- array of zones
  idea JSONB, -- {direction, entry, SL, TP, RR}
  mentor_note TEXT,
  confidence FLOAT,
  processing_time_ms INT,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX (user_id),
  INDEX (image_hash),
  INDEX (created_at)
);

-- user_preferences table
CREATE TABLE user_preferences (
  user_id UUID PRIMARY KEY REFERENCES users(id),
  timeframes TEXT[] DEFAULT '{"H1", "H4", "D1"}',
  trading_style TEXT, -- scalping, swing, position
  risk_per_trade FLOAT DEFAULT 2.0, -- percent
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Phase 2 API Additions

```
POST /api/auth/register
  +- Email + password
  +- Create Supabase user

POST /api/auth/login
  +- Email + password
  +- Return JWT token

GET /api/history
  +- Auth required
  +- Query params: ?limit=20&offset=0&sort=date
  +- Return paginated analyses

GET /api/history/{analysis_id}
  +- Auth required
  +- Return single analysis with image

DELETE /api/history/{analysis_id}
  +- Auth required
  +- Delete analysis

POST /api/analyze-chart-async
  +- Queue-based processing
  +- Return 202 with job_id
  +- Client polls /api/job-status/{job_id}

GET /api/job-status/{job_id}
  +- Return job progress
  +- Return result when ready

GET /api/user/profile
  +- Auth required
  +- Return user preferences + stats

PUT /api/user/profile
  +- Auth required
  +- Update user preferences
```

### Phase 2 Deployment

```
GitHub Repository (same)
    ¦
    +- git push
    ?
GitHub Actions + Environment Secrets
    +- ANTHROPIC_API_KEY
    +- SUPABASE_URL
    +- SUPABASE_ANON_KEY
    +- REDIS_URL (Upstash)
    +- Run tests
    
    ?
Vercel Deployment (same)
    +- Set environment variables
    
Additional Services:
+- Supabase (PostgreSQL database + auth)
+- Upstash (Redis for cache + queue)

Cost implications:
+- Supabase: ~$25-50/month (free tier available)
+- Upstash: ~$0.2 per day + usage
+- Vercel: Still within free tier
+- Claude API: Based on usage (~$50-150/month at 100-500 analyses/day)
```

---

## Phase 3 (Real-Time & Browser Extension)

### Phase 3 Additions

```
Phase 2 Architecture +

+- WebSocket Server (real-time updates)
¦  +- Price stream subscriptions
¦  +- Live chart refresh triggers
¦
+- Browser Extension (Chrome/Firefox)
¦  +- Content script (inject into TradingView)
¦  +- Background service worker
¦  +- Popup UI
¦  +- Storage (local cache)
¦
+- Broker API Integrations
¦  +- MT5 (via Python backend)
¦  +- Interactive Brokers
¦  +- Oanda
¦
+- Economic Calendar Integration
   +- Track major events
```

### Extension Architecture

```
User on TradingView.com
    ¦
    +- Content script detects chart
    +- Screenshot chart canvas
    +- Send to extension background
    
    ?
Extension Popup
    ¦
    +- Display "Analyze with Chart Mentor"
    +- User clicks
    +- Send image to API
    
    ?
Backend API
    ¦
    +- Analyze chart
    +- Return analysis
    
    ?
Extension Popup
    ¦
    +- Display trend badge
    +- Show S/R levels
    +- Show trade idea
    +- Overlay on TradingView chart (optional)
```

---

## Decision Matrix: Which Phase Are You In?

### Phase 1 If:
- ? You're validating product-market fit
- ? < 100 analyses per day expected
- ? Single chart per upload
- ? No user accounts needed yet
- ? Want fastest time-to-market

### Phase 2 If:
- ? You have users coming back
- ? > 100 analyses per day
- ? Users want history
- ? Need tiered pricing (free/pro)
- ? Want to reduce API costs via caching

### Phase 3 If:
- ? Thousands of daily analyses
- ? Traders need real-time updates
- ? TradingView integration is key
- ? Want broker integration
- ? Building for enterprise users

---

## Migration Paths

### Phase 1 ? Phase 2

1. Add Supabase
   - Create auth & database tables
   - Minimal code changes (services already abstracted)

2. Add Redis cache
   - Wrap vision service with cache layer
   - No API contract changes

3. Add async queue
   - New endpoint: /api/analyze-chart-async
   - Phase 1 endpoint still works

4. Add history endpoints
   - New endpoints: /api/history, /api/analysis/{id}
   - Existing analysis logic unchanged

Effort: ~2-3 weeks for experienced team

### Phase 2 ? Phase 3

1. Add WebSocket server
   - New /ws endpoint
   - Separate concern from analysis

2. Add browser extension
   - Separate codebase (TypeScript + Webpack)
   - API calls same as web app

3. Add broker integrations
   - New service layer (broker.service.ts)
   - No changes to analysis logic

Effort: ~3-4 weeks for experienced team

