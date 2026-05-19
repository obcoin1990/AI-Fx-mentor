# Requirements: AI Chart Mentor

**Defined:** 2025-05-19
**Core Value:** Traders get instant, structured, objective chart analysis from a screenshot — eliminating manual analysis and emotional decisions.

## v1 Requirements

All requirements must be shipping in Phase 1 MVP.

### Upload & Processing

- [ ] **UPLOAD-01**: User can upload forex chart screenshot (PNG/JPG format)
- [ ] **UPLOAD-02**: System validates image is readable (min 200x200, max 5MB)
- [ ] **UPLOAD-03**: System rejects non-image files with clear error
- [ ] **UPLOAD-04**: Upload progress displays to user

### AI Analysis - Vision

- [ ] **VISION-01**: Vision model extracts trend direction (bullish/bearish/consolidating)
- [ ] **VISION-02**: Vision model identifies swing highs and lows from candles
- [ ] **VISION-03**: Vision model extracts support price zones (identified by multiple price touches)
- [ ] **VISION-04**: Vision model extracts resistance price zones (identified by multiple price touches)
- [ ] **VISION-05**: Vision model detects chart patterns (double top/bottom, channels, triangles, flags, head & shoulders)
- [ ] **VISION-06**: Vision model returns structured JSON with all extracted data

### AI Analysis - Reasoning

- [ ] **REASON-01**: Reasoning model generates 1-2 possible trade scenarios (direction, entry, stop-loss, take-profit)
- [ ] **REASON-02**: Reasoning model calculates risk-reward ratio for each scenario (entry-to-TP / entry-to-SL)
- [ ] **REASON-03**: Reasoning model assigns confidence score (0-100%, capped at 65% in MVP)
- [ ] **REASON-04**: Reasoning model produces mentor-style explanation (plain English, no jargon without definition)
- [ ] **REASON-05**: Reasoning model flags if confidence is low (<50%, analysis unreliable)

### Analysis Output & Display

- [ ] **OUTPUT-01**: System displays trend badge (Bullish / Bearish / Consolidating)
- [ ] **OUTPUT-02**: System displays support zone card with price range and how many touches
- [ ] **OUTPUT-03**: System displays resistance zone card with price range and how many touches
- [ ] **OUTPUT-04**: System displays trade idea card with direction, entry, SL, TP, R:R ratio
- [ ] **OUTPUT-05**: System displays mentor explanation (3-5 sentences max, educational tone)
- [ ] **OUTPUT-06**: System displays confidence score for each element
- [ ] **OUTPUT-07**: System displays "Analysis for [PAIR], [TIMEFRAME]" context (extracted from image or user input)

### Quality & Trust

- [ ] **QUALITY-01**: System includes legal disclaimer: "This is educational analysis, not financial advice"
- [ ] **QUALITY-02**: System includes disclaimer: "Do not trade based solely on this tool"
- [ ] **QUALITY-03**: System validates all numbers against chart data (no hallucinated prices)
- [ ] **QUALITY-04**: System rejects analyses if key data extraction fails (shows "Unable to analyze chart")
- [ ] **QUALITY-05**: System runs same chart twice, outputs must be consistent (deterministic)
- [ ] **QUALITY-06**: System includes "watch out" warning if unusual volatility or gaps detected

### Performance & Reliability

- [ ] **PERF-01**: System responds within 5 seconds for typical chart (vision + reasoning + display)
- [ ] **PERF-02**: System handles Claude API timeout: returns cached analysis if available, else "try again"
- [ ] **PERF-03**: System logs all analyses for debugging and audit trail
- [ ] **PERF-04**: System caches analyses by image hash (48h TTL) to avoid re-processing identical charts

### User Experience

- [ ] **UX-01**: UI/UX supports dark and light themes
- [ ] **UX-02**: UI/UX supports internationalization (EN, AR, CN with RTL for Arabic)
- [ ] **UX-03**: UI is mobile-responsive (works on phone + tablet + desktop)
- [ ] **UX-04**: Mobile app (if applicable) has native upload from camera
- [ ] **UX-05**: Drag & drop upload box for easy chart submission
- [ ] **UX-06**: Results display clearly with visual hierarchy (trend → zones → idea → explanation)

### Data & Privacy

- [ ] **PRIVACY-01**: System does NOT store chart images after analysis
- [ ] **PRIVACY-02**: System stores ONLY analysis output (JSON) for audit/debugging
- [ ] **PRIVACY-03**: System does NOT collect user data (no user accounts, tracking, or cookies)
- [ ] **PRIVACY-04**: Stored analyses deleted after 30 days

---

## v2 Requirements

Deferred to Phase 2 (add user accounts, persistence, feedback):

### User Accounts & History

- User authentication (email/password or OAuth)
- User profiles with saved analysis history
- Search/filter past analyses by date, pair, pattern
- Favorite analyses for quick reference

### Feedback & Learning

- Feedback mechanism: "Was this analysis helpful?"
- Track which patterns actually worked
- Auto-disable patterns with <60% accuracy
- A/B test Claude vs GPT-4o outputs

### Extended Scope

- Multi-timeframe analysis (analyze same pair across 1H, 4H, 1D)
- Support for Crypto pairs (BTC/USDT, ETH/USDT, etc.)
- Support for Indices (SPX, DAX, etc.)
- Auto-draw support/resistance levels on uploaded image

---

## v3+ Requirements

Phase 3 and beyond (browser extension, real-time, advanced):

- Browser extension for TradingView
- Real-time chart capture and analysis
- Personalized trading mentor profile
- Integration with broker APIs (Phase 4)
- Backtesting historical patterns
- Automated trade alerts

---

## Out of Scope

Explicitly excluded from all phases:

| Feature | Reason |
|---------|--------|
| **Automated Trading Execution** | Liability risk; requires licensing. Users make trading decisions, not AI. |
| **Signals Service / Alerts** | (Phase 2 minimum) Users can't act on alerts without persistent accounts. |
| **Live Chart Integration** | Phase 1 is stateless; real-time requires infrastructure investment. |
| **MT5 / TradingView API Connection** | Too complex for MVP; direct broker/platform APIs Phase 3+. |
| **Subscription / Freemium Model** | Phase 2 minimum (need accounts first). MVP is free. |
| **Backtesting Engine** | Requires historical data infrastructure (expensive). Phase 3+. |
| **Stocks (Phase 1)** | Scope limited to forex. Stocks Phase 3+ after crypto validation. |
| **Performance Guarantees** | Never claim "AI wins 80% of the time" or similar. |
| **Copy Trading** | Users can't auto-copy trades; they analyze and decide. |
| **Sentiment Analysis** | Too complex for MVP. Stick to technical chart analysis. |
| **News Integration** | Out of scope; adds data source management burden. |

---

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| UPLOAD-01 | Phase 1 | Mapped ✓ |
| UPLOAD-02 | Phase 1 | Mapped ✓ |
| UPLOAD-03 | Phase 1 | Mapped ✓ |
| UPLOAD-04 | Phase 1 | Mapped ✓ |
| VISION-01 | Phase 1 | Mapped ✓ |
| VISION-02 | Phase 1 | Mapped ✓ |
| VISION-03 | Phase 1 | Mapped ✓ |
| VISION-04 | Phase 1 | Mapped ✓ |
| VISION-05 | Phase 1 | Mapped ✓ |
| VISION-06 | Phase 1 | Mapped ✓ |
| REASON-01 | Phase 1 | Mapped ✓ |
| REASON-02 | Phase 1 | Mapped ✓ |
| REASON-03 | Phase 1 | Mapped ✓ |
| REASON-04 | Phase 1 | Mapped ✓ |
| REASON-05 | Phase 1 | Mapped ✓ |
| OUTPUT-01 | Phase 1 | Mapped ✓ |
| OUTPUT-02 | Phase 1 | Mapped ✓ |
| OUTPUT-03 | Phase 1 | Mapped ✓ |
| OUTPUT-04 | Phase 1 | Mapped ✓ |
| OUTPUT-05 | Phase 1 | Mapped ✓ |
| OUTPUT-06 | Phase 1 | Mapped ✓ |
| OUTPUT-07 | Phase 1 | Mapped ✓ |
| QUALITY-01 | Phase 1 | Mapped ✓ |
| QUALITY-02 | Phase 1 | Mapped ✓ |
| QUALITY-03 | Phase 1 | Mapped ✓ |
| QUALITY-04 | Phase 1 | Mapped ✓ |
| QUALITY-05 | Phase 1 | Mapped ✓ |
| QUALITY-06 | Phase 1 | Mapped ✓ |
| PERF-01 | Phase 1 | Mapped ✓ |
| PERF-02 | Phase 1 | Mapped ✓ |
| PERF-03 | Phase 1 | Mapped ✓ |
| PERF-04 | Phase 1 | Mapped ✓ |
| UX-01 | Phase 1 | Mapped ✓ |
| UX-02 | Phase 1 | Mapped ✓ |
| UX-03 | Phase 1 | Mapped ✓ |
| UX-04 | Phase 1 | Mapped ✓ |
| UX-05 | Phase 1 | Mapped ✓ |
| UX-06 | Phase 1 | Mapped ✓ |
| PRIVACY-01 | Phase 1 | Mapped ✓ |
| PRIVACY-02 | Phase 1 | Mapped ✓ |
| PRIVACY-03 | Phase 1 | Mapped ✓ |
| PRIVACY-04 | Phase 1 | Mapped ✓ |

**Coverage:**
- v1 requirements: 40 total
- Mapped to phases: 40 ✓
- Unmapped: 0 ✓

---

*Requirements defined: 2025-05-19*
*Last updated: 2025-05-19 after roadmap creation*
