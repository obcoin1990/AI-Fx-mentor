# AI Chart Mentor

## What This Is

A web platform that analyzes forex trading chart screenshots using AI vision and reasoning models. Traders upload a chart image and receive instant, structured analysis: trend direction, support/resistance zones, trade scenarios with entry/stop-loss/take-profit levels, risk-reward ratios, and mentor-style educational explanations. The goal is to give traders an objective, disciplined approach to chart analysis that reduces emotional decision-making and saves time.

## Core Value

**Traders get instant, structured, objective chart analysis from a screenshot — eliminating manual analysis and emotional decisions.**

This is the ONE thing that must work. Everything else serves this.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**MVP (Phase 1 — Forex Only)**
- [ ] User can upload forex chart screenshot (PNG/JPG)
- [ ] AI vision model extracts trend, swing highs/lows, support/resistance, chart patterns
- [ ] AI reasoning model generates trade scenarios with entry/SL/TP
- [ ] AI calculates risk-reward ratio for each scenario
- [ ] Platform displays mentor-style explanation of chart analysis
- [ ] Platform shows structured analysis: trend badge, support/resistance cards, trade idea card, mentor notes
- [ ] Response includes trend, support zones, resistance zones, trade idea (direction, entry, SL, TP, RR), mentor explanation

**Phase 2 — Accounts & History**
- [ ] User authentication (email/password or OAuth)
- [ ] User accounts with saved analyses
- [ ] Personal analysis history dashboard
- [ ] Multi-timeframe analysis support
- [ ] Auto-draw support/resistance levels on chart image
- [ ] Extended scope: Crypto + Indices

**Phase 3 — Browser Extension & Real-Time**
- [ ] Browser extension for TradingView integration
- [ ] Real-time chart capture and analysis
- [ ] Personalized trading mentor profile

### Out of Scope

- **Automated Trading** — No algo execution or automated signals
- **Signals Service** — No subscription alerts or broadcast signals
- **Live Chart Integration (Phase 1)** — No real-time streaming; screenshots only in MVP
- **MT5/TradingView API Connection (Phase 1)** — Direct broker/platform integration deferred
- **User Accounts & Dashboards (Phase 1)** — MVP is stateless analysis
- **Multi-Timeframe Analysis (Phase 1)** — Single chart per upload
- **Backtesting Engine** — No historical performance testing
- **Stocks (Phase 1)** — Forex focus only; stocks deferred to Phase 3+

## Context

### Domain & Market
- Target: Retail forex traders (retail, semi-professional)
- Problem: Manual chart analysis is time-consuming and emotionally biased
- Opportunity: AI can provide instant, objective, structured analysis at scale

### Technical Environment
- Frontend: Next.js (implied from existing component structure)
- Backend: Next.js API routes
- AI Models: Claude 3.5 Sonnet Vision + Claude 3.5 Sonnet reasoning (or GPT-4o alternatives)
- Database: Supabase (for Phase 2+ user data)
- Image Handling: PNG/JPG support
- Internationalization: i18n system supports EN, AR, CN with RTL for Arabic
- UI: Dark/light theme support via next-themes + TailwindCSS

### AI Pipeline
1. User uploads chart screenshot
2. Vision model analyzes image → extracts candles, highs/lows, trend, key levels → returns structured JSON
3. Reasoning model processes extracted data → generates trade ideas, mentor explanation
4. Response sent to frontend: JSON (trend, support, resistance, trade idea) + mentor note

### Success Metrics
- **Usage**: Traders use the tool daily
- **Volume**: 100+ chart analyses per day
- **Quality**: AI provides consistent, high-quality, structured analysis
- **Trust**: Users trust the mentor-style guidance and improve trading discipline
- **Adoption**: Tool becomes part of daily trading routine

## Constraints

- **Focus (MVP)**: Forex-only in Phase 1 — keeps MVP simple and focused
- **Architecture**: Stateless analysis in Phase 1 (no user accounts, dashboards, or history)
- **Image Format**: PNG/JPG only (no proprietary chart formats)
- **Model Selection**: Claude 3.5 Sonnet or GPT-4o for both vision and reasoning (ensure consistent quality)
- **Scope Limitation**: No automated trading, signals service, or live streaming in MVP

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Forex-only in Phase 1 | Reduces scope, allows deep focus on one asset class | — Pending validation |
| No authentication in Phase 1 | Faster time-to-market, simpler MVP, less infrastructure | — Pending (added in Phase 2) |
| Vision → JSON → Reasoning pipeline | Separates concerns, allows structured extraction before reasoning, easier to debug | — Pending validation |
| Claude 3.5 Sonnet for both vision and reasoning | Consistent quality across the pipeline, good performance/cost ratio | — Pending implementation |
| Stateless analysis only in Phase 1 | Reduces backend complexity, faster shipping | — Pending validation |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2025-05-19 after initialization*
