# Architecture Documentation

## System Architecture Overview

AI Chart Mentor follows a **Vision → JSON → Reasoning** pipeline architecture, separating concerns for clarity, debuggability, and future scaling.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT SIDE                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Next.js Frontend (React 19, TailwindCSS, next-i18n)    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │ Upload Box   │  │ Theme Toggle │  │ i18n Switcher│   │  │
│  │  │ (Drag-drop)  │  │ (Dark/Light) │  │ (EN/AR/CN)   │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ Upload → Validation → Display Results            │    │  │
│  │  │ • Image format/size check (local)                │    │  │
│  │  │ • Skeleton UI while analyzing                    │    │  │
│  │  │ • Trend badge, zone cards, scenario card         │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    HTTP POST /api/analyze-chart
                             │
┌────────────────────────────┴─────────────────────────────────────┐
│                        SERVER SIDE                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend (Python, Async)                         │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │ Routes: /api/analyze-chart, /health, /metrics      │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐        ┌──────────┐
    │  CACHE  │         │ VISION  │        │ DATABASE │
    │  Redis  │         │ SERVICE │        │PostgreSQL│
    │         │         │         │        │          │
    │Check if │────────▶│Claude   │───────▶│Store JSON│
    │cached   │   MISS  │Vision   │        │Analysis  │
    │         │         │API      │        │(30d TTL) │
    │Return   │         │         │        │          │
    │cached   │   HIT   │Extracts:│        └──────────┘
    │result   │         │- Trend  │
    │in <500ms│         │- Zones  │
    │         │         │- Support│
    │         │         │- Resist │
    │         │         │- Pattern│
    │         │         │         │
    │         │         │Returns: │
    │         │         │JSON     │
    │         │         │         │
    │Cache it │         │         │
    │48h TTL  │         │         │
    │         │         │         │
    └─────────┘         └────┬────┘
         △                    │
         │                    │ Vision Output
         │                    │ (JSON)
         │                    ▼
         │         ┌──────────────────┐
         │         │  REASONING       │
         │         │  SERVICE         │
         │         │                  │
         │         │ Claude Reasoning │
         │         │ API              │
         │         │                  │
         │         │ Generates:       │
         │         │ - Scenarios (1-2)│
         │         │ - R:R Calc       │
         │         │ - Confidence     │
         │         │ - Explanation    │
         │         │                  │
         │         │ Returns:         │
         │         │ Complete JSON    │
         │         │ Analysis         │
         │         └────────┬─────────┘
         │                  │
         │   ┌──────────────┤
         │   │              │
         │   ▼              ▼
         │ ┌──────────┐  ┌──────────┐
         │ │VALIDATION│  │MONITORING│
         │ │          │  │          │
         │ │- Conf    │  │- Metrics │
         │ │  Capping │  │- Logging │
         │ │- Low Conf│  │- Sentry  │
         │ │  Flagging│  │- Perf    │
         │ │- Halluci │  │  Tracking│
         │ │  Detection  │          │
         │ └─────┬────┘  └──────────┘
         │       │
         └───────┴─────────┬──────────────────────────────────┐
                           │                                  │
                           ▼                                  │
                ┌───────────────────────┐                    │
                │  RESPONSE TO CLIENT   │                    │
                │  ┌─────────────────┐  │                    │
                │  │ {              │  │                    │
                │  │   trend        │  │                    │
                │  │   zones[]      │  │                    │
                │  │   scenarios[]  │  │                    │
                │  │   confidence   │  │                    │
                │  │   explanation  │  │                    │
                │  │   analysis_id  │  │                    │
                │  │   timestamp    │  │                    │
                │  │ }              │  │                    │
                │  └─────────────────┘  │                    │
                └───────────────────────┘                    │
                                                             │
                        ┌────────────────────────────────────┘
                        │
                        ▼
         (Return to Frontend, Display Results)

```

---

## Request Flow - Detailed

### 1. Upload & Validation
```
User uploads chart.png
  ↓
Frontend validation:
  ✓ Format check (PNG/JPG only)
  ✓ Size check (max 5MB)
  ✓ Dimension check (min 200x200)
  ↓
POST /api/analyze-chart with:
  - file binary data
  - pair (optional, e.g., "EUR/USD")
  - timeframe (optional, e.g., "4H")
```

### 2. Backend Processing
```
Backend receives multipart/form-data
  ↓
Validation layer:
  ✓ Verify content-type
  ✓ Check file size again
  ✓ Verify image can be read
  ↓
Generate image hash (SHA256)
  ↓
Check Redis cache:
  ├─ HIT (found) → Return cached JSON in <500ms
  └─ MISS (not found) → Continue to Vision API
      ↓
      Send to Claude Vision API:
      - Encode image to base64
      - Include vision prompt
      - Max tokens: 2000
      - Timeout: 10 seconds
      ↓
      Vision API returns:
      {
        "trend": "bullish",
        "support_zones": [...],
        "resistance_zones": [...],
        "patterns_detected": [...],
        "swing_highs": [...],
        "swing_lows": [...]
      }
      ↓
      Validation & Capping:
      ✓ Confidence scores capped at 65%
      ✓ Validate all required fields
      ✓ Check for hallucinated prices
      ✓ Flag unusual volatility
      ↓
      Cache in Redis (48h TTL)
      ↓
      Send to Reasoning API:
      - Include vision JSON
      - Include reasoning prompt
      - Max tokens: 1500
      - Timeout: 10 seconds
      ↓
      Reasoning API returns:
      {
        "scenarios": [
          {
            "direction": "bullish|bearish",
            "entry_price": 1.0850,
            "stop_loss": 1.0800,
            "take_profit": 1.0950,
            "risk_reward_ratio": 2.0,
            "confidence": 62
          }
        ],
        "mentor_explanation": "...",
        "overall_confidence": 62
      }
      ↓
      Final Validation:
      ✓ Validate trade scenarios
      ✓ Cap confidence at 65%
      ✓ Flag low confidence (<50%)
      ✓ Validate explanations
      ↓
      Combine Vision + Reasoning JSON
      ↓
      Store in PostgreSQL (audit log, 30d retention)
      ↓
      Record metrics (Sentry):
      - Response time
      - Vision duration
      - Reasoning duration
      - Cache hit/miss
      - Success/failure
```

### 3. Response & Display
```
Return complete JSON to frontend:
{
  "analysis_id": "uuid",
  "timestamp": "2025-05-19T10:30:00Z",
  "pair": "EUR/USD",
  "timeframe": "4H",
  "trend": "bullish",
  "trend_confidence": 62.5,
  "support_zones": [...],
  "resistance_zones": [...],
  "patterns_detected": [...],
  "scenarios": [...],
  "mentor_explanation": "...",
  "overall_confidence": 62.5,
  "volatility_warning": null
}
↓
Frontend renders:
├─ Trend badge (bullish = green, bearish = red, consolidating = gray)
├─ Support zones card
├─ Resistance zones card
├─ Trade idea card (scenario 1, scenario 2 if available)
├─ Mentor explanation box
├─ Confidence display (visual gauge, 65% max)
├─ Disclaimers (prominent, yellow box)
└─ Volatility warning (if present)
```

---

## Technology Stack Details

| Layer | Technology | Purpose | Version |
|-------|-----------|---------|---------|
| **Frontend** | Next.js | Server-side rendering, routing | 16.2.6 |
| | React | UI components, state management | 19 |
| | TailwindCSS | Utility-first styling | v3 |
| | next-i18n-routing | i18n with RTL support | Latest |
| | Zustand | Lightweight state | 5.x |
| | TypeScript | Type safety | 5.x |
| **Backend** | FastAPI | Web framework, async | 0.104.0 |
| | Uvicorn | ASGI server | 0.24+ |
| | Anthropic | Claude API client | 0.7+ |
| | Pydantic | Data validation, schemas | 2.0+ |
| **Database** | PostgreSQL | Analysis audit logs | 18 |
| | Supabase | Managed PostgreSQL | Cloud |
| **Cache** | Redis | 48h image hash cache | 7.x |
| | Redis Cloud | Managed Redis | Cloud |
| **Storage** | Supabase Storage | S3-compatible (future) | Cloud |
| **Monitoring** | Sentry | Error tracking, alerts | Cloud |
| **Deployment** | Vercel | Frontend hosting | Cloud |
| | Railway | Backend hosting | Cloud |

---

## Performance Targets

| Metric | Target | Implementation |
|--------|--------|-----------------|
| **New Analysis (cache miss)** | <5 seconds | Vision 2-3s, Reasoning 2-2.5s |
| **Cached Analysis (cache hit)** | <500ms | Redis GET, no API calls |
| **Vision API** | <3 seconds | Claude Vision with 10s timeout |
| **Reasoning API** | <2 seconds | Claude Reasoning with 10s timeout |
| **Cache Hit Rate** | >30% | Same chart → same hash → cached |
| **Response Time p95** | <5 seconds new, <500ms cached | Load testing under 50+ concurrent |
| **Uptime (Phase 1)** | Best effort | No SLA commitment |
| **Success Rate** | >95% | Monitoring, alerting, incident response |

---

## Data Flow Security

```
User's Chart Image
  ↓
  ├─ Sent to Claude Vision API (Anthropic)
  │  ├─ TLS 1.3 encryption in transit
  │  ├─ Processed, not stored by Anthropic (their policy)
  │  └─ Vision JSON returned
  │
  ├─ Chart image DISCARDED (not stored in our DB)
  │
  ├─ Analysis JSON stored in PostgreSQL (30 days)
  │  ├─ TLS encryption in transit
  │  ├─ Database encryption at rest (Supabase)
  │  └─ Auto-deleted after 30 days
  │
  └─ Used for monitoring/improvement only
     ├─ No personal data mixed in
     ├─ No user tracking
     └─ Complies with privacy-first policy
```

---

## Error Handling & Fallbacks

| Failure Point | Handling |
|--------------|----------|
| **Image validation fails** | Return 400 error with details (format, size, etc.) |
| **Vision API timeout (>10s)** | Return 504 with error message |
| **Reasoning API timeout (>10s)** | Return partial result (vision only) with warning |
| **Database error** | Log error, still return analysis to user (best effort) |
| **Redis unavailable** | Disable caching, continue normally (slower) |
| **Invalid analysis JSON** | Log, reject, return 500 error |
| **Hallucinated prices detected** | Reject analysis, flag in logs, return 400 |

---

## Future Architecture (Phase 2+)

- **User accounts** → Authentication layer, user profile storage
- **Multi-timeframe** → Queue system for parallel analysis
- **Backtesting** → Historical data storage, trade simulation
- **Webhooks** → Real-time alerts to user devices
- **API access** → Third-party integrations, rate limiting
- **Blockchain audit** → Immutable analysis record (optional)
- **Advanced caching** → CDN for static assets, geographically distributed

---

*Architecture last updated: 2025-05-19*
*For: Phase 1 MVP*
