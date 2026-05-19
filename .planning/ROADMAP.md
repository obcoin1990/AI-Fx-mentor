# Roadmap: AI Chart Mentor

## Overview

AI Chart Mentor ships in 3 phases, each delivering complete vertical user capabilities. Phase 1 is a self-contained MVP where traders upload a chart screenshot and receive instant, AI-powered analysis with mentor-style guidance. Phase 2 adds accounts, persistence, and learning feedback loops. Phase 3 scales with browser extensions, real-time analysis, and multi-asset support.

**Core Value Across All Phases:** Traders get instant, structured, objective chart analysis from a screenshot — eliminating manual analysis and emotional decisions.

---

## Phase 1: MVP Stateless Analysis
**Goal:** Deliver complete upload → analyze → display workflow. Traders upload forex chart screenshots and receive instant, structured analysis with mentor-style explanations. Validate core AI analysis quality and user trust.

**Mode:** mvp

**Duration:** 4-6 weeks

**Scope:** Stateless analysis only (no accounts, no persistence beyond 30-day audit logs, no user tracking)

### Requirements Mapped

**Upload & Processing (4 requirements)**
- UPLOAD-01: User can upload forex chart screenshot (PNG/JPG format)
- UPLOAD-02: System validates image is readable (min 200x200, max 5MB)
- UPLOAD-03: System rejects non-image files with clear error
- UPLOAD-04: Upload progress displays to user

**AI Analysis - Vision Extraction (6 requirements)**
- VISION-01: Vision model extracts trend direction (bullish/bearish/consolidating)
- VISION-02: Vision model identifies swing highs and lows from candles
- VISION-03: Vision model extracts support price zones (identified by multiple price touches)
- VISION-04: Vision model extracts resistance price zones (identified by multiple price touches)
- VISION-05: Vision model detects chart patterns (double top/bottom, channels, triangles, flags, head & shoulders)
- VISION-06: Vision model returns structured JSON with all extracted data

**AI Analysis - Reasoning (5 requirements)**
- REASON-01: Reasoning model generates 1-2 possible trade scenarios (direction, entry, stop-loss, take-profit)
- REASON-02: Reasoning model calculates risk-reward ratio for each scenario (entry-to-TP / entry-to-SL)
- REASON-03: Reasoning model assigns confidence score (0-100%, capped at 65% in MVP)
- REASON-04: Reasoning model produces mentor-style explanation (plain English, no jargon without definition)
- REASON-05: Reasoning model flags if confidence is low (<50%, analysis unreliable)

**Analysis Output & Display (7 requirements)**
- OUTPUT-01: System displays trend badge (Bullish / Bearish / Consolidating)
- OUTPUT-02: System displays support zone card with price range and how many touches
- OUTPUT-03: System displays resistance zone card with price range and how many touches
- OUTPUT-04: System displays trade idea card with direction, entry, SL, TP, R:R ratio
- OUTPUT-05: System displays mentor explanation (3-5 sentences max, educational tone)
- OUTPUT-06: System displays confidence score for each element
- OUTPUT-07: System displays "Analysis for [PAIR], [TIMEFRAME]" context (extracted from image or user input)

**Quality & Trust (6 requirements)**
- QUALITY-01: System includes legal disclaimer: "This is educational analysis, not financial advice"
- QUALITY-02: System includes disclaimer: "Do not trade based solely on this tool"
- QUALITY-03: System validates all numbers against chart data (no hallucinated prices)
- QUALITY-04: System rejects analyses if key data extraction fails (shows "Unable to analyze chart")
- QUALITY-05: System runs same chart twice, outputs must be consistent (deterministic)
- QUALITY-06: System includes "watch out" warning if unusual volatility or gaps detected

**Performance & Reliability (4 requirements)**
- PERF-01: System responds within 5 seconds for typical chart (vision + reasoning + display)
- PERF-02: System handles Claude API timeout: returns cached analysis if available, else "try again"
- PERF-03: System logs all analyses for debugging and audit trail
- PERF-04: System caches analyses by image hash (48h TTL) to avoid re-processing identical charts

**User Experience (6 requirements)**
- UX-01: UI/UX supports dark and light themes
- UX-02: UI/UX supports internationalization (EN, AR, CN with RTL for Arabic)
- UX-03: UI is mobile-responsive (works on phone + tablet + desktop)
- UX-04: Mobile app (if applicable) has native upload from camera
- UX-05: Drag & drop upload box for easy chart submission
- UX-06: Results display clearly with visual hierarchy (trend → zones → idea → explanation)

**Data & Privacy (4 requirements)**
- PRIVACY-01: System does NOT store chart images after analysis
- PRIVACY-02: System stores ONLY analysis output (JSON) for audit/debugging
- PRIVACY-03: System does NOT collect user data (no user accounts, tracking, or cookies)
- PRIVACY-04: Stored analyses deleted after 30 days

**Total Phase 1 Requirements:** 40 ✓

### Success Criteria

1. **Upload Works** — Traders can upload forex chart screenshots (PNG/JPG) on desktop, tablet, and mobile via drag-and-drop or file picker. Validation catches invalid files with clear error messages.

2. **AI Analysis Extracts Data** — Vision model reliably identifies trend, swing highs/lows, support/resistance zones, and chart patterns from typical forex charts. Extracted JSON is well-formed and matches visual inspection.

3. **Analysis Generates Scenarios** — Reasoning model produces 1-2 trade scenarios (direction, entry, SL, TP) with calculated R:R ratios and confidence scores (capped at 65%). Explanations are mentor-style and educational.

4. **Display is Clear & Trustworthy** — Results show trend badge, zone cards, trade idea card, mentor explanation, and legal disclaimers. Visual hierarchy guides traders from trend → zones → idea → explanation.

5. **Response Times are Fast** — Upload + Vision + Reasoning + Display completes in <5 seconds on typical charts. Cache hits are near-instant. Timeouts gracefully fallback to cached results or "try again" message.

6. **Privacy is Maintained** — Chart images are not stored. Only analysis output (JSON) is retained for 30 days for audit. No user accounts, tracking, or cookies.

7. **Quality is Consistent** — Same chart analyzed twice produces identical output (deterministic). Analyses with low confidence (<50%) are flagged. Invalid or inconsistent data triggers "Unable to analyze chart" message.

8. **Traders Trust the Output** — User testing shows traders find the analysis credible, educational, and useful for decision-making. Disclaimers are visible and respected.

### Architecture Highlights

- **Frontend:** Next.js 16 + React 19 (responsive, dark/light theme, i18n support)
- **Backend:** FastAPI 0.104 (stateless API, vision + reasoning endpoints)
- **AI Models:** Claude 3.5 Sonnet (vision extraction + reasoning)
- **Database:** PostgreSQL for 30-day audit logs + Redis for 48h image hash cache
- **Deployment:** Vercel (frontend) + Railway (FastAPI backend) + Supabase (PostgreSQL + storage cleanup job)
- **Cache Strategy:** Image hash → analysis output (48h TTL); API timeouts fallback to cache

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Forex-only in Phase 1 | Reduces scope, allows deep focus on one asset class to validate quality |
| Stateless analysis (no accounts) | Faster time-to-market, simpler MVP, no auth infrastructure needed in Phase 1 |
| Vision → JSON → Reasoning pipeline | Separates concerns, allows structured extraction before reasoning, easier debugging |
| Confidence score capped at 65% | Prevents false confidence; disclaimers carry more weight when scores are conservative |
| Claude 3.5 Sonnet for both vision and reasoning | Consistent quality, good performance/cost ratio, supports structured JSON output |
| Image cache by hash (48h) | Avoids re-processing identical charts, improves response time, reduces API costs |
| 30-day audit log retention | Balances debugging needs with privacy; older logs auto-delete via scheduled job |

### Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Vision model hallucinating prices | QUALITY-03: Validate extracted prices against chart data; reject if mismatch detected |
| Reasoning model low-quality scenarios | Test with 50+ real forex charts; iterate on prompts until consistent quality; use REASON-05 flag |
| Slow response times | Cache by image hash; pre-compute common patterns; set timeout to 10s (allow 5s for response) |
| User distrust due to wrong analysis | Disclaimers prominently displayed; confidence cap at 65%; flag low-confidence analyses |
| API rate limits (Claude) | Implement request queueing + exponential backoff; cache 48h to reduce re-processing |

---

## Phase 2: Accounts & Learning Feedback
**Goal:** Enable traders to save analyses, track patterns, and refine model accuracy through feedback loops. Add multi-timeframe analysis and extend asset class support (crypto, indices). Validate that feedback improves model performance.

**Mode:** growth

**Duration:** 8-12 weeks (after Phase 1 validation)

**Scope:** User accounts, analysis history, feedback loops, multi-timeframe support, extended asset classes

### Requirements

**User Accounts & Persistence (4 new requirements)**
- AUTH-01: User authentication (email/password or OAuth2 via Supabase)
- AUTH-02: User accounts with profile (name, trading style, experience level)
- HISTORY-01: Save individual analyses with metadata (pair, timeframe, timestamp, asset class)
- HISTORY-02: Search/filter past analyses by date, pair, pattern, asset class

**Feedback & Learning (4 new requirements)**
- FEEDBACK-01: "Was this analysis helpful?" feedback mechanism
- FEEDBACK-02: Track which patterns actually worked (user marks trade outcome)
- FEEDBACK-03: Auto-disable patterns with <60% accuracy
- FEEDBACK-04: A/B test Claude vs GPT-4o outputs; track which performs better

**Extended Scope (4 new requirements)**
- MULTI-01: Multi-timeframe analysis (analyze same pair across 1H, 4H, 1D)
- MULTI-02: Confidence correlation across timeframes (consensus strength)
- ASSET-01: Support for Crypto pairs (BTC/USDT, ETH/USDT, etc.) in addition to forex
- ASSET-02: Support for Indices (SPX, DAX, etc.) in addition to forex

**Analysis Enhancement (3 new requirements)**
- ENHANCE-01: Auto-draw support/resistance levels on uploaded chart image
- ENHANCE-02: Favorite/bookmark favorite analyses for quick reference
- ENHANCE-03: Export analysis as PDF or image for sharing

**Total Phase 2 Requirements:** 15 new (55 cumulative with Phase 1)

### Success Criteria

1. **User Accounts Work** — Traders sign up via email/password or OAuth, create profiles, and remain logged in. Account data persists across sessions.

2. **History is Searchable** — Traders view all saved analyses, filter by date/pair/pattern/asset class, and click to view full analysis details.

3. **Feedback Loop Closes** — Traders mark "helpful/not helpful" and track trade outcomes (won/loss/break-even). System aggregates feedback and flags low-accuracy patterns.

4. **Multi-Timeframe Analysis Works** — Traders upload a chart and request analysis across 1H/4H/1D. System shows consensus: high confidence if all timeframes agree, low confidence if timeframes conflict.

5. **Extended Assets Supported** — Vision model correctly identifies crypto pairs (BTC/USDT) and indices (SPX). Analysis quality matches forex performance.

6. **Model Accuracy Improves Over Time** — Feedback data shows patterns with >60% accuracy; patterns with <60% accuracy are auto-disabled in recommendations.

7. **PDF Export Works** — Traders can download analysis as PDF with chart image, trend badge, zones, idea, and explanation.

### Architecture Highlights

- **Database:** Supabase PostgreSQL expanded for user accounts, analyses, feedback, and pattern performance tracking
- **Auth:** Supabase Auth (email + OAuth)
- **Frontend:** New dashboard with analysis history, search, filter, and feedback UI
- **Backend:** Endpoints for feedback ingestion, pattern performance tracking, and A/B test routing
- **Cache:** Expand Redis to cache user profiles and pattern performance data
- **Scheduled Jobs:** Pattern accuracy calculation (daily), low-accuracy pattern disable (weekly)

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Supabase Auth for user accounts | Managed auth service; integrates with PostgreSQL; OAuth built-in; faster than custom auth |
| Feedback-driven pattern disable | Prevents system from recommending low-accuracy patterns; improves user trust over time |
| Multi-timeframe consensus model | Traders want confidence across timeframes; disagreement signals uncertainty to users |
| A/B test Claude vs GPT-4o | Validate which model performs better; allows switching if GPT-4o improves quality/cost ratio |
| PDF export for sharing | Enables users to save/share analyses without losing context; increases distribution via social proof |

---

## Phase 3: Scale & Automation
**Goal:** Expand to real-time analysis, browser extensions, and advanced personalization. Enable traders to integrate analysis into live trading workflows.

**Mode:** scale

**Duration:** 12-16 weeks (after Phase 2 validation)

**Scope:** Real-time chart capture, browser extensions, personalized mentor profiles, API for third-party integration

### Requirements

**Real-Time & Browser Integration (4 new requirements)**
- REALTIME-01: Browser extension for TradingView that captures chart screenshots on-demand
- REALTIME-02: Real-time push notifications for new trade setups detected on monitored pairs
- REALTIME-03: One-click analysis from TradingView charts (no manual upload needed)
- REALTIME-04: Monitor multiple pairs simultaneously; alerts on high-confidence setups

**Personalization (3 new requirements)**
- PERSONA-01: Personalized trading mentor profile (trading style, risk tolerance, preferred patterns)
- PERSONA-02: Model outputs tailored to user style (conservative traders get lower R:R targets; aggressive traders get higher targets)
- PERSONA-03: Pattern recommendations based on user history (patterns that worked for this trader are prioritized)

**API & Integration (3 new requirements)**
- API-01: REST API for third-party integrations (custom trading dashboards, signal services)
- API-02: Webhook support for analysis events (trigger downstream actions)
- API-03: Rate limiting and API key management for third-party developers

**Advanced Features (3 new requirements)**
- ADVANCED-01: Backtesting engine to test patterns against historical data
- ADVANCED-02: Risk simulator (what-if scenarios for different position sizes)
- ADVANCED-03: Correlation analysis across multiple pairs (identify hedging opportunities)

**Total Phase 3 Requirements:** 13 new (68 cumulative with Phase 1 + Phase 2)

### Success Criteria

1. **TradingView Extension Works** — Traders install extension, open any forex/crypto/indices chart on TradingView, and analyze with one click. Analysis appears in side panel or popup.

2. **Real-Time Alerts Work** — Traders set up monitoring for 5-10 pairs. When new high-confidence setup detected, trader receives browser notification and/or email alert.

3. **Mentor Profile is Personal** — System learns trader's style and adjusts recommendations. Conservative traders see lower R:R targets; aggressive traders see higher targets.

4. **API is Used by Third Parties** — At least 3 third-party integrations are built on the API (custom dashboards, Discord bots, Telegram alerts).

5. **Backtesting Validates Strategy** — Traders backtest a pattern against 1-year history and see win rate, max drawdown, and profit factor.

### Architecture Highlights

- **Browser Extension:** TypeScript + TradingView-compatible hooks + Manifest V3 (Chrome)
- **Real-Time Backend:** WebSocket support for push notifications + scheduled jobs for pattern detection
- **API Layer:** GraphQL + REST endpoints for third-party access; OpenAPI schema for documentation
- **Backtesting Engine:** Separate service that queries historical OHLCV data from data providers (or user-uploaded CSV)
- **Notification Service:** Email + browser push + webhook support
- **Admin Dashboard:** Pattern performance analytics, user engagement metrics, API usage monitoring

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| TradingView extension first (not MT5) | TradingView is most popular among retail traders; larger addressable market |
| WebSocket for push notifications | Low-latency, bidirectional communication; enables real-time alerts |
| GraphQL API option | Flexible query language; reduces over-fetching; better for mobile/extension clients |
| Backtesting via external data service | Don't build historical data ingestion; use existing providers (Yahoo Finance, Twelve Data, etc.) |
| Mentor personalization via user profile | Traders define their style; system uses it to weight pattern recommendations |

---

## Requirement Traceability Matrix

| ID | Category | Requirement | Phase 1 | Phase 2 | Phase 3 | Status |
|----|----|-----------|---------|---------|---------|--------|
| UPLOAD-01 | Upload | User can upload forex chart | ✓ | — | — | Pending |
| UPLOAD-02 | Upload | Validate image readable | ✓ | — | — | Pending |
| UPLOAD-03 | Upload | Reject non-images | ✓ | — | — | Pending |
| UPLOAD-04 | Upload | Upload progress display | ✓ | — | — | Pending |
| VISION-01 | Vision | Extract trend | ✓ | — | — | Pending |
| VISION-02 | Vision | Identify swing highs/lows | ✓ | — | — | Pending |
| VISION-03 | Vision | Extract support zones | ✓ | — | — | Pending |
| VISION-04 | Vision | Extract resistance zones | ✓ | — | — | Pending |
| VISION-05 | Vision | Detect chart patterns | ✓ | — | — | Pending |
| VISION-06 | Vision | Return structured JSON | ✓ | — | — | Pending |
| REASON-01 | Reasoning | Generate trade scenarios | ✓ | — | — | Pending |
| REASON-02 | Reasoning | Calculate R:R ratio | ✓ | — | — | Pending |
| REASON-03 | Reasoning | Assign confidence score | ✓ | — | — | Pending |
| REASON-04 | Reasoning | Mentor explanation | ✓ | — | — | Pending |
| REASON-05 | Reasoning | Flag low confidence | ✓ | — | — | Pending |
| OUTPUT-01 | Output | Trend badge | ✓ | — | — | Pending |
| OUTPUT-02 | Output | Support zone card | ✓ | — | — | Pending |
| OUTPUT-03 | Output | Resistance zone card | ✓ | — | — | Pending |
| OUTPUT-04 | Output | Trade idea card | ✓ | — | — | Pending |
| OUTPUT-05 | Output | Mentor explanation | ✓ | — | — | Pending |
| OUTPUT-06 | Output | Confidence score display | ✓ | — | — | Pending |
| OUTPUT-07 | Output | Context display | ✓ | — | — | Pending |
| QUALITY-01 | Quality | Educational disclaimer | ✓ | — | — | Pending |
| QUALITY-02 | Quality | Non-advice disclaimer | ✓ | — | — | Pending |
| QUALITY-03 | Quality | Validate numbers | ✓ | — | — | Pending |
| QUALITY-04 | Quality | Reject invalid analyses | ✓ | — | — | Pending |
| QUALITY-05 | Quality | Deterministic output | ✓ | — | — | Pending |
| QUALITY-06 | Quality | Volatility warning | ✓ | — | — | Pending |
| PERF-01 | Performance | <5s response time | ✓ | — | — | Pending |
| PERF-02 | Performance | API timeout handling | ✓ | — | — | Pending |
| PERF-03 | Performance | Analysis logging | ✓ | — | — | Pending |
| PERF-04 | Performance | 48h analysis cache | ✓ | — | — | Pending |
| UX-01 | UX | Dark/light theme | ✓ | — | — | Pending |
| UX-02 | UX | i18n (EN/AR/CN) | ✓ | — | — | Pending |
| UX-03 | UX | Mobile responsive | ✓ | — | — | Pending |
| UX-04 | UX | Camera upload | ✓ | — | — | Pending |
| UX-05 | UX | Drag & drop | ✓ | — | — | Pending |
| UX-06 | UX | Visual hierarchy | ✓ | — | — | Pending |
| PRIVACY-01 | Privacy | No image storage | ✓ | — | — | Pending |
| PRIVACY-02 | Privacy | Store only JSON | ✓ | — | — | Pending |
| PRIVACY-03 | Privacy | No user tracking | ✓ | — | — | Pending |
| PRIVACY-04 | Privacy | 30-day retention | ✓ | — | — | Pending |

**Coverage Summary:**
- **Phase 1 (v1 MVP):** 40 requirements ✓
- **Phase 2 (Growth):** 15 new requirements (55 cumulative)
- **Phase 3 (Scale):** 13 new requirements (68 cumulative)
- **Total Mapped:** 68
- **Unmapped:** 0 ✓

---

## Phase Transition Criteria

### Phase 1 → Phase 2 (Go/No-Go Checklist)

**Must Have:**
- [ ] Phase 1 live with >100 daily active users
- [ ] User feedback shows >70% satisfaction ("would use again")
- [ ] AI analysis quality consistent across 50+ test charts
- [ ] Response time <5s for 95% of analyses
- [ ] No critical bugs blocking uploads or analysis
- [ ] Legal disclaimers reviewed by counsel

**Should Have:**
- [ ] User request for history/saves feature
- [ ] Interest in multi-asset support (crypto, indices)
- [ ] Retention data showing >30% return rate
- [ ] Partner interest (e.g., trading communities)

**Nice to Have:**
- [ ] Mobile app downloads >1k
- [ ] Social media sharing evidence
- [ ] Feature requests for Phase 2 items

### Phase 2 → Phase 3 (Go/No-Go Checklist)

**Must Have:**
- [ ] Phase 2 live with user accounts, history, and feedback
- [ ] Feedback mechanism shows pattern accuracy correlation (low-accuracy patterns flagged)
- [ ] Monthly active users >1k
- [ ] Multi-timeframe analysis works without degradation
- [ ] Crypto/indices analysis quality matches forex
- [ ] <10% error rate on analysis outputs

**Should Have:**
- [ ] User requests for browser extension
- [ ] Real-time analysis use cases identified
- [ ] API interest from third parties
- [ ] Mentor personalization roadmap validated

**Nice to Have:**
- [ ] Backtesting requests from users
- [ ] Advanced pattern detection ideas
- [ ] Partnership opportunities

---

## Timeline Overview

| Phase | Duration | Start | End | Key Deliverables |
|-------|----------|-------|-----|------------------|
| Phase 1 (MVP) | 4-6 weeks | Week 1 | Week 6 | Live app, all 40 v1 requirements, public beta |
| Phase 2 (Growth) | 8-12 weeks | Week 7-8 | Week 18-20 | User accounts, feedback, multi-asset, multi-timeframe |
| Phase 3 (Scale) | 12-16 weeks | Week 21-24 | Week 36-40 | TradingView extension, real-time, backtesting, API |

---

## Success Metrics (By Phase)

### Phase 1
- **Adoption:** 100+ daily active users by end of phase
- **Quality:** AI analysis consistency >85% on repeat charts
- **Trust:** User satisfaction >70% ("would use again")
- **Performance:** 95th percentile response time <5s
- **Reliability:** 99.5% uptime; <1% analysis failures

### Phase 2
- **Retention:** 30% month-over-month retention (users return within 30 days)
- **Engagement:** Average 5+ analyses per active user per month
- **Feedback Quality:** Pattern accuracy correlation visible in feedback data
- **Asset Expansion:** Crypto/indices analysis quality matches forex (>85% consistency)
- **Growth:** Monthly active users >1k

### Phase 3
- **Extension Adoption:** 5k+ extension installs
- **Real-Time Usage:** 500+ traders actively monitoring pairs
- **API Ecosystem:** 3+ third-party integrations live
- **Backtesting:** 1k+ backtests run per month
- **Revenue Ready:** Path to monetization (API tier, premium features) validated

---

## Notes

- All phases assume forex market validation in Phase 1; extended assets only if Phase 1 succeeds
- Phase 1 is intentionally stateless to reduce infrastructure complexity and ship faster
- Feedback loop (Phase 2) is critical to improving model accuracy; don't skip this
- Real-time/extension (Phase 3) requires stable, high-quality API; prioritize Phase 2 quality
- Each phase transition requires explicit validation; don't auto-advance
- Privacy constraints (no image storage, 30-day retention) apply across all phases

---

*Roadmap created: 2025-05-19*
*Last updated: 2025-05-19*
