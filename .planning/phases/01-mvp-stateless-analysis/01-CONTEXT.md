# Phase 1: MVP Stateless Analysis - Context

**Gathered:** 2025-05-19
**Status:** Ready for planning
**Source:** Project Initialization (PROJECT.md, ROADMAP.md, Research)

## Phase Boundary

**Phase Goal:** Deliver complete upload → analyze → display workflow. Traders upload forex chart screenshots and receive instant, structured analysis with mentor-style explanations. Validate core AI analysis quality and user trust.

**What we're shipping:**
- Stateless analysis (no user accounts, no persistence beyond 30-day audit logs)
- Vision model extracts: trend, swing highs/lows, support/resistance zones, chart patterns → structured JSON
- Reasoning model generates: 1-2 trade scenarios with entry/SL/TP, R:R ratios, confidence scores (capped 65%), mentor explanations
- Frontend displays: trend badge, zone cards, trade idea card, mentor explanation, legal disclaimers
- Performance: upload + analysis + display in <5 seconds; cached requests <500ms
- Privacy: no chart image storage, only 30-day JSON analysis logs

**Success criteria (from ROADMAP.md):**
1. Upload works (mobile/tablet/desktop, drag-drop, validation)
2. Vision model reliably extracts trend, zones, patterns
3. Reasoning generates scenarios with R:R, confidence (capped 65%)
4. Display is clear with visual hierarchy + disclaimers
5. Response time <5s; cache hits near-instant
6. Privacy maintained (no image storage, 30-day JSON logs only)
7. Consistency (same chart = same output)
8. User testing shows traders trust the analysis

## Implementation Decisions

### Architecture (Locked)
- **Vision → JSON → Reasoning pipeline** — Separates concerns, enables validation, easier debugging, supports caching
- **Claude 3.5 Sonnet for both vision and reasoning** — Consistent quality, good performance/cost ratio
- **PostgreSQL + Redis cache** — Audit logs (30 days) + image hash cache (48h TTL)
- **Vercel (frontend) + Railway (backend) + Supabase (database)** — Standard deployment stack

### Quality & Trust (Locked)
- **Confidence scores capped at 65%** — Prevents false confidence; disclaimers more credible
- **Legal disclaimers prominently displayed** — "This is educational analysis, not financial advice" + "Do not trade based solely on this tool"
- **No image storage** — Discard immediately after vision model extracts data
- **Consistent output** — Same chart analyzed twice must produce identical results
- **No hallucinated data** — Validate all numbers against chart data; reject if mismatch

### Tech Stack (Locked)
- **Frontend:** Next.js 16 + React 19 + TailwindCSS v3
- **Backend:** FastAPI 0.104 (Python)
- **i18n:** EN, AR (RTL), CN support via next-i18n
- **Dark/Light Theme:** next-themes with system detection

### the agent's Discretion

Implementation details the planner should decide:
- Claude Vision prompt structure (what exactly to extract)
- Claude Reasoning prompt structure (how to generate scenarios)
- Image validation thresholds (min/max dimensions, file size, compression)
- Cache key strategy (exact image hash algorithm)
- Error messages and fallback UX
- Styling details, icon choices, layout specifics
- Database indices and query optimization
- API response format details
- Testing strategy (unit, integration, e2e)

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Core value, constraints, key decisions
- `.planning/ROADMAP.md` — Phase breakdown, requirement mappings
- `.planning/REQUIREMENTS.md` — All 40 v1 requirements by category
- `.planning/AGENTS.md` — Project guidance, pitfalls, non-negotiables
- `.planning/config.json` — Workflow configuration (YOLO, fine granularity, all agents enabled)

### Research & Architecture
- `.planning/research/STACK.md` — 2025 tech stack recommendations
- `.planning/research/FEATURES.md` — Table stakes vs differentiators
- `.planning/research/ARCHITECTURE.md` — Component boundaries, data flow
- `.planning/research/PITFALLS.md` — Common mistakes to avoid
- `.planning/research/SUMMARY.md` — Synthesis of all research

## Specific Ideas

### Phase 1 Requirements (40 total)

**Upload & Processing (4)**
- UPLOAD-01: User can upload forex chart screenshot (PNG/JPG)
- UPLOAD-02: System validates image (min 200x200, max 5MB)
- UPLOAD-03: System rejects non-images with clear error
- UPLOAD-04: Upload progress displays

**Vision Analysis (6)**
- VISION-01: Extract trend direction (bullish/bearish/consolidating)
- VISION-02: Identify swing highs and lows
- VISION-03: Extract support zones (identified by multiple price touches)
- VISION-04: Extract resistance zones (identified by multiple price touches)
- VISION-05: Detect chart patterns (double top/bottom, channels, triangles, flags, head & shoulders)
- VISION-06: Return structured JSON

**Reasoning Analysis (5)**
- REASON-01: Generate 1-2 trade scenarios (direction, entry, SL, TP)
- REASON-02: Calculate risk-reward ratio for each scenario
- REASON-03: Assign confidence score (0-100%, capped at 65%)
- REASON-04: Mentor-style explanation (plain English, educational)
- REASON-05: Flag if confidence <50% (unreliable)

**Display & Output (7)**
- OUTPUT-01: Trend badge (Bullish/Bearish/Consolidating)
- OUTPUT-02: Support zone card with price range and touches
- OUTPUT-03: Resistance zone card with price range and touches
- OUTPUT-04: Trade idea card (direction, entry, SL, TP, R:R)
- OUTPUT-05: Mentor explanation (3-5 sentences max)
- OUTPUT-06: Confidence score display per element
- OUTPUT-07: Context display (pair, timeframe)

**Quality & Trust (6)**
- QUALITY-01: Legal disclaimer (educational analysis, not financial advice)
- QUALITY-02: Non-advice disclaimer (don't trade based solely on this)
- QUALITY-03: Validate all numbers against chart data
- QUALITY-04: Reject if key extraction fails
- QUALITY-05: Consistency test (same chart = same output)
- QUALITY-06: Watch out warning (unusual volatility, gaps)

**Performance & Reliability (4)**
- PERF-01: Response <5 seconds
- PERF-02: Claude API timeout handling (return cached or "try again")
- PERF-03: Log all analyses for audit trail
- PERF-04: Cache by image hash (48h TTL)

**UX & Accessibility (6)**
- UX-01: Dark and light theme support
- UX-02: Internationalization (EN/AR/CN with RTL)
- UX-03: Mobile-responsive (phone/tablet/desktop)
- UX-04: Mobile camera upload (if applicable)
- UX-05: Drag-drop upload box
- UX-06: Clear visual hierarchy (trend → zones → idea → explanation)

**Privacy (4)**
- PRIVACY-01: Do NOT store chart images
- PRIVACY-02: Store ONLY analysis output (JSON)
- PRIVACY-03: No user accounts, tracking, cookies
- PRIVACY-04: Delete analyses after 30 days

### Team Notes

- **Timeline:** 4-6 weeks
- **Team:** Frontend engineer (Next.js), Backend engineer (FastAPI), AI/Prompts engineer
- **Critical path:** Vision model accuracy (weeks 2-3) → Reasoning quality (week 4-5) → Performance optimization (week 6)
- **User testing:** Target 5-10 traders in final week

### Real-World Context

**Problem we're solving:**
Traders waste time manually analyzing charts and make emotional decisions. They need instant, objective, structured analysis with confidence levels they can trust.

**Market validation:**
- TradingView is most popular platform for retail traders
- Chart analysis is core workflow (daily, multiple pairs)
- Traders want patterns identified + trade ideas + mentor guidance
- Biggest pain: information overload (need clarity and simplicity)

## Deferred Ideas

**Phase 2 (Weeks 7-20):**
- User accounts (Supabase Auth)
- Analysis history + search/filter
- Feedback loop (helpful? trade outcome?)
- Multi-timeframe analysis (1H, 4H, 1D consensus)
- Extended assets (Crypto: BTC/USDT; Indices: SPX, DAX)
- A/B test Claude vs GPT-4o

**Phase 3+ (Later):**
- TradingView browser extension
- Real-time alerts on new setups
- Personalized mentor profiles
- REST + GraphQL API
- Backtesting engine
- Risk simulator

---

*Phase: 01-mvp-stateless-analysis*
*Context gathered: 2025-05-19 from Project Initialization*
