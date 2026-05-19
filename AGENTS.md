# AI Chart Mentor — Project Guidance (AGENTS.md)

**Project:** AI Chart Mentor
**Initialized:** 2025-05-19
**Core Value:** Traders get instant, structured, objective chart analysis from a screenshot — eliminating manual analysis and emotional decisions.
**Status:** Ready for Phase 1 Execution

This document guides agents and team members through the project's vision, architecture, constraints, and execution approach.

---

## Quick Start

**For agents executing this project:**
1. Read `.planning/PROJECT.md` (vision, constraints, decisions)
2. Read `.planning/REQUIREMENTS.md` (all 40 v1 requirements)
3. Read `.planning/ROADMAP.md` (phase structure, success criteria)
4. Read this file (execution approach, pitfalls, non-negotiables)

**For team members:**
1. Clone repositories
2. Review this file + PROJECT.md
3. Start with Week 1 tasks from STATE.md
4. Run `/gsd-plan-phase 1` to generate detailed execution plan

---

## Project Context

### What We're Building

AI Chart Mentor is a web platform that analyzes forex trading charts using AI. Traders upload a screenshot, receive instant analysis with:
- Trend direction (bullish/bearish/consolidating)
- Support & resistance zones
- 1-2 possible trade scenarios (entry, stop-loss, take-profit, risk-reward)
- Mentor-style educational explanation
- Confidence score (capped at 65% to prevent false confidence)

**Core Value:** Remove manual analysis friction and emotional decision-making from trading.

### Success Metrics

- Traders use it daily
- 100+ chart analyses per day
- Consistent, high-quality analysis
- Users trust and improve discipline
- Tool becomes part of daily routine

### Scope: What We're NOT Building in Phase 1

- ❌ User accounts or dashboards
- ❌ Automated trading or signal alerts
- ❌ Image storage (privacy-first, stateless)
- ❌ Multi-timeframe analysis
- ❌ Real-time analysis
- ❌ TradingView integration
- ❌ Crypto or stocks (forex-only)
- ❌ Performance guarantees or "guaranteed wins"

These are deferred to Phase 2 and beyond, only after MVP is validated.

---

## Architecture Overview

### High-Level Flow

```
User uploads chart (PNG/JPG)
    ↓
Next.js frontend validates image (size, format)
    ↓
FastAPI backend receives image
    ↓
Claude Vision API extracts data
    (trend, swing highs/lows, support/resistance zones, patterns)
    ↓
Structured JSON output from vision model
    ↓
Claude Reasoning API processes extracted data
    (generates 1-2 trade scenarios, calculates R:R, assigns confidence)
    ↓
Next.js renders results
    (trend badge, zone cards, trade idea card, mentor explanation)
    ↓
Disclaimers prominently displayed
```

### Technology Stack

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| **Frontend** | Next.js | 16.2.6 | App Router; React 19; TailwindCSS v3 |
| **Frontend State** | Zustand | 5.x | Light, simple state management |
| **UI Themes** | next-themes | latest | Dark/light mode with system detection |
| **I18n** | next-i18n-routing | latest | EN/AR/CN support with RTL for Arabic |
| **Backend** | FastAPI | 0.104 | Async Python API framework |
| **Server** | Uvicorn | latest | ASGI server for FastAPI |
| **AI Vision** | Claude 3.5 Sonnet | 4.6 | Image analysis, pattern detection |
| **AI Reasoning** | Claude 3.5 Sonnet | 4.6 | Trade scenario generation, explanations |
| **Database** | PostgreSQL | 18 | Supabase-hosted; 30-day audit logs |
| **Cache** | Redis | 7.x | Redis Cloud; 48h image hash cache |
| **Storage** | Supabase Storage | — | S3-compatible; auto-delete old logs |
| **Auth** | Supabase Auth | — | Phase 2 (not Phase 1) |
| **Deploy Frontend** | Vercel | — | Native Next.js deployment |
| **Deploy Backend** | Railway | — | FastAPI + PostgreSQL support |
| **Monitoring** | Sentry | — | Error tracking |

### Key Architectural Decisions

1. **Vision → JSON → Reasoning Pipeline**
   - Vision model extracts chart data into structured JSON
   - Reasoning model then processes JSON to generate scenarios
   - **Why:** Separates concerns, enables validation, easier debugging, supports caching

2. **Stateless MVP (Phase 1)**
   - No user accounts, no image storage, no persistent state
   - Each request is independent
   - **Why:** Faster time-to-market, simpler infrastructure, privacy-first

3. **Confidence Score Capped at 65%**
   - Even high-confidence analyses never exceed 65%
   - Prevents false confidence, makes disclaimers credible
   - **Why:** Protects against overconfidence bias; users respect conservative recommendations

4. **Image Hash Caching (48h TTL)**
   - Same chart uploaded twice → use cached analysis
   - Avoids re-processing, saves API costs, faster response
   - **Why:** Traders often analyze same patterns; 40-50% cost savings

5. **Claude 3.5 Sonnet for Both Vision & Reasoning**
   - Consistent quality across pipeline
   - Good performance/cost ratio vs GPT-4o or Opus
   - **Why:** Validated by research; balances quality and cost

---

## Critical Non-Negotiables

These are non-negotiables for Phase 1. Violating them breaks the project:

### 1. Privacy First
- ❌ NEVER store uploaded chart images permanently
- ✓ Discard immediately after vision model extracts data
- ✓ Store only analysis output (JSON) for 30 days
- ✓ Auto-delete logs after 30 days via scheduled job
- ✓ NO user tracking, cookies, or analytics (Phase 1)

**Why:** Privacy is trust. Traders won't use a tool that stores their analysis strategy.

### 2. Honest Disclaimers
- ✓ Prominently display: "This is educational analysis, not financial advice"
- ✓ Display: "Do not trade based solely on this tool"
- ❌ NEVER claim "guaranteed profits," "AI never loses," or "X% win rate"
- ❌ NEVER use language implying financial advice ("You should buy," "I recommend")

**Why:** Legal liability. Securities regulators will act if disclaimers are absent or weak.

### 3. No Hallucinations
- ✓ Validate every price point, entry, stop-loss, take-profit against chart data
- ✓ Reject analyses if numbers don't match visual chart
- ✓ Test consistency: run same chart 5 times, output must be identical
- ❌ NEVER allow Claude to generate fake prices or data

**Why:** False data leads to trader losses → lawsuits → platform shutdown.

### 4. Confidence Scores (Capped at 65%)
- ✓ All confidence scores max out at 65%
- ✓ Flag analyses with <50% confidence as "unreliable"
- ✓ Show confidence for each element (trend confidence, zone confidence, idea confidence)
- ❌ NEVER exceed 65% confidence in MVP

**Why:** Prevents false confidence; keeps users cautious; builds long-term trust.

### 5. No User Accounts (Phase 1)
- ❌ NO authentication, user profiles, dashboards, or saved histories in Phase 1
- ✓ Stateless: each request is independent
- ✓ Phase 2 adds accounts (only after MVP is validated)
- ❌ NO feature creep to add accounts early

**Why:** Faster shipping, simpler MVP, less infrastructure. Validate core analysis quality first.

### 6. Forex Only (Phase 1)
- ❌ NO crypto, stocks, indices, or commodities in Phase 1
- ✓ Forex pairs only (EUR/USD, GBP/USD, etc.)
- ✓ Phase 2 adds crypto/indices (only after forex quality is proven)

**Why:** Reduces scope, allows deep focus, simpler validation. Extend after success.

### 7. No Automated Trading
- ❌ NEVER execute trades on behalf of users
- ❌ NEVER promise to automate trading strategies
- ✓ Analysis only; users make trading decisions
- ✓ Phase 3+ only (and requires licensing)

**Why:** Massive liability and regulatory risk. Stay in analysis space, not trading space.

---

## Execution Approach

### Workflow Configuration

**Mode:** YOLO
- Auto-approve decisions at each phase transition
- Trust the planning process; execute without delays

**Granularity:** Fine
- 8-12 focused phases total across all work
- Each phase has clear, testable success criteria

**Execution:** Parallel
- Independent tasks run simultaneously
- Maximize team parallelization

**Agents Enabled:** All
- Research: Investigate domain/architecture before planning phases
- Plan Check: Verify plans achieve goals
- Verifier: Confirm work satisfies requirements after each phase

**AI Models:** Balanced
- Claude 3.5 Sonnet for most agents
- Opus 4.7 for complex reasoning (selective)

### Planning & Execution Cycle

**For each phase:**

1. **Discuss Phase (Optional)** — `/gsd-discuss-phase N`
   - Clarify approach, surface unknowns, align on scope
   - Output: DISCUSSION.md with context + decisions

2. **Plan Phase** — `/gsd-plan-phase N`
   - Research domain/architecture
   - Create detailed execution plan with task breakdown
   - Verify plan will achieve phase goal
   - Output: PLAN.md (tasks, dependencies, estimates)

3. **Execute Phase** — `/gsd-execute-phase N`
   - Run tasks in order (or parallel if independent)
   - Commit work atomically after each task
   - Output: Code, tests, documentation

4. **Verify Phase** — `/gsd-verify-phase N` (automatic or manual)
   - Confirm requirements satisfied
   - Check success criteria met
   - Output: VERIFICATION.md

5. **Transition Phase** — `/gsd-transition`
   - Update PROJECT.md (move validated requirements, note decisions)
   - Prepare for next phase
   - Commit

---

## Pitfalls to Avoid

### AI Quality Pitfalls

1. **False Confidence**
   - ❌ Don't generate confidence >65%
   - ✓ Cap at 65% in code if Claude goes higher
   - ❌ Don't claim pattern works 80% of the time (unvalidated)

2. **Support/Resistance Accuracy**
   - ❌ Don't identify 10 support zones per chart (traders ignore)
   - ✓ Identify 2-3 significant zones where price actually bounced
   - ✓ Show how many touches at each level

3. **Hallucinated Numbers**
   - ❌ Don't let Claude generate prices not visible on chart
   - ✓ Validate: entry point must be visible on chart
   - ✓ Validate: stop-loss must be below support or above resistance

4. **Inconsistency**
   - ❌ Don't run same chart, get different output
   - ✓ Test: run chart 5 times, all outputs identical
   - ✓ Set random seed to zero for reproducibility

### User Experience Pitfalls

5. **Information Overload**
   - ❌ Don't output 5 paragraphs of analysis
   - ✓ Keep to 3-5 sentences max
   - ✓ Visual hierarchy: trend badge → zones → idea → explanation

6. **Missing Context**
   - ❌ Don't analyze chart without showing "EUR/USD, 4H timeframe"
   - ✓ Always display pair + timeframe
   - ✓ Show market regime (uptrend, downtrend, consolidation)

7. **No Feedback Loop**
   - ❌ Phase 1 is stateless; no way for traders to say "this was wrong"
   - ✓ Phase 2 adds feedback mechanism
   - ✓ Phase 2 tracks which patterns actually worked

### Legal/Regulatory Pitfalls

8. **Liability Exposure**
   - ❌ Don't say "Traders are making 20% monthly using our tool"
   - ❌ Don't track user P&L as if endorsing results
   - ✓ Legal review of all disclaimers before launch
   - ✓ Consult securities lawyer in Phase 2 (when adding accounts)

9. **Implied Financial Advice**
   - ❌ Don't use words "should," "recommend," "buy," "sell"
   - ✓ Use neutral language: "The chart suggests a bullish pattern"
   - ✓ Neutral: "A trader might consider entry at X"

10. **Performance Claims**
    - ❌ Don't say "AI wins 80% of trades"
    - ❌ Don't publish user testimonials claiming profits
    - ✓ Show analysis only; neutral outcomes

### Infrastructure Pitfalls

11. **API Cost Explosions**
    - ❌ Don't process same chart 10x per day
    - ✓ Cache by image hash (48h)
    - ✓ Monitor token usage; alert if >$50/day

12. **Vendor Lock-In**
    - ❌ Don't design system that only works with Claude
    - ✓ Abstraction layer for model selection
    - ✓ Phase 2 tests GPT-4o as alternative

13. **Privacy Violations**
    - ❌ Don't store chart images without explicit user consent
    - ✗ Don't add analytics/tracking in Phase 1
    - ✓ Clear data retention policy (30 days, then delete)

---

## Success Criteria for Phase 1

Phase 1 MVP is done when:

1. ✓ Traders can upload charts on mobile/desktop via drag-drop
2. ✓ Vision model accurately extracts trend, zones, patterns from 20+ test charts
3. ✓ Reasoning model generates 1-2 trade scenarios with R:R and confidence
4. ✓ Display shows trend badge, zone cards, idea card, mentor explanation
5. ✓ Same chart analyzed twice produces identical output
6. ✓ Response time <5s; cached requests <500ms
7. ✓ Legal disclaimers are prominent and clear
8. ✓ 5-10 user testers say "I find this helpful and trustworthy"
9. ✓ No privacy violations; chart images not stored
10. ✓ No hallucinated data; all prices validated

---

## When to Ask for Help

**Pause and escalate if:**

- Claude vision model hallucinates prices not on chart
- Claude reasoning generates trades with high confidence (you must cap at 65%)
- Consistency tests fail (same chart gives different output)
- Response time exceeds 10 seconds (investigate caching or timeouts)
- User testers report low trust ("analysis doesn't seem right")
- Anything feels like it could expose the project to legal liability

**For each of these, escalate with:**
1. What went wrong
2. What you've tried
3. Proposed solution
4. Impact on Phase 1 timeline

---

## Resources

**In `.planning/`:**
- `PROJECT.md` — Vision, constraints, decisions
- `REQUIREMENTS.md` — All 40 v1 requirements
- `ROADMAP.md` — 3-phase structure, success criteria
- `STATE.md` — Current status, progress tracker
- `research/` — Stack, features, architecture, pitfalls research
- `config.json` — Workflow settings (YOLO, fine granularity, parallel)

**External:**
- Claude API docs: https://docs.anthropic.com
- Next.js docs: https://nextjs.org/docs
- FastAPI docs: https://fastapi.tiangolo.com
- Supabase docs: https://supabase.com/docs

---

## Contact & Escalation

For questions or blockers, escalate to:
1. **Architecture decisions:** Review ROADMAP.md + KEY DECISIONS section
2. **Scope questions:** Check REQUIREMENTS.md (v1/v2/out-of-scope tables)
3. **Timeline questions:** See STATE.md (Week 1-6 breakdown)
4. **Pitfalls/blockers:** Refer to this file's PITFALLS section
5. **Legal questions:** Consult securities lawyer before Phase 2

---

**This document is living.** Update as you learn:
- Challenges encountered
- Decisions made
- Lessons learned
- Refinements to approach

*Project initialized: 2025-05-19*
*Ready for Phase 1 execution.*
