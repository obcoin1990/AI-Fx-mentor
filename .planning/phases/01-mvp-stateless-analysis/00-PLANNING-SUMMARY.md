---
title: Phase 1 Planning Complete
date: 2025-05-19
status: READY FOR EXECUTION
---

# Phase 1 MVP Stateless Analysis — Executable Plan Summary

## Overview

Phase 1 planning is complete. 7 detailed, executable plans cover all 40 v1 requirements for AI Chart Mentor MVP. Plans are organized as vertical slices with clear task breakdowns, dependencies, and acceptance criteria.

**Phase Goal:** Deliver complete upload → analyze → display workflow. Traders upload forex chart screenshots and receive instant, structured analysis with mentor-style explanations.

**Duration:** 4-6 weeks
**Team:** Frontend Engineer + Backend Engineer + AI/Prompts Engineer + QA Engineer
**Mode:** YOLO (auto-approve decisions), Fine Granularity (8-12 phases total), Parallel Execution

---

## Plan Structure

All plans follow strict format:

`yaml
---
wave: [1-3]  # Which wave for parallel execution
depends_on: [list of dependency plans]
files_modified: [list of files this plan creates/modifies]
autonomous: true  # Can executor run independently?
---
`

Each task includes:
- **read_first** — Files executor MUST read before working
- **action** — Concrete implementation steps with exact values
- **acceptance_criteria** — Grep-verifiable conditions proving task is done

---

## 7 Plans Overview

### Plan 1: Foundation (Wave 1)
**Objective:** Establish project scaffolding, CI/CD, deployment infrastructure.
**Duration:** 3-4 days
**Tasks:** 8 (git setup, env config, CI/CD pipelines, DB schema, Redis cache, deployments, docs)
**Requirements Mapped:** 7 (PRIVACY-01, PRIVACY-02, PRIVACY-03, PRIVACY-04, PERF-02, PERF-03, PERF-04)
**Autonomous:** YES (no dependencies)

**Deliverables:**
- Monorepo: frontend/, backend/, .github/workflows/
- Next.js 16.2.6, React 19, FastAPI 0.104
- GitHub Actions CI/CD (lint → test → deploy)
- Vercel + Railway configs
- PostgreSQL audit_logs (JSON only, no images) + cache_keys tables
- Redis cache strategy (48h TTL, image hash keys)
- docker-compose.yml for local 3-service development

**Files Modified:** 12
- package.json, pyproject.toml, .env.example
- .github/workflows/ (frontend-ci.yml, backend-ci.yml)
- vercel.json, railway.toml, Dockerfile, docker-compose.yml
- README.md, .gitignore, LICENSE

---

### Plan 2: Frontend UI & Upload (Wave 1)
**Objective:** Build upload interface with drag-drop, validation, theme/i18n support.
**Duration:** 4-5 days
**Tasks:** 6 (components: upload box, result display scaffold, store, i18n, theme, validation)
**Requirements Mapped:** 10 (UPLOAD-01 to 04, UX-01 to 06)
**Autonomous:** YES (depends on Plan 1 for scaffold)

**Deliverables:**
- UploadBox component (drag-drop + file picker)
- Image validation (PNG/JPG, 200x200 min, 5MB max)
- Upload progress indicator
- Zustand store for UI state
- Dark/light theme toggle + next-themes setup
- i18n configuration (EN/AR/CN with RTL)
- Mobile-responsive Tailwind layout
- Camera upload support for mobile

**Files Modified:** 11
- frontend/app/layout.tsx, page.tsx
- frontend/components/ (upload-box.tsx, result-display.tsx)
- frontend/lib/ (store.ts, i18n.ts, theme.ts)
- frontend/tailwind.config.ts, app/globals.css
- frontend/public/locales/ (en.json, ar.json, zh.json)

---

### Plan 3: Vision API & Image Processing (Wave 2)
**Objective:** Implement Claude Vision API endpoint. Extract trend, zones, patterns into JSON.
**Duration:** 4-5 days
**Tasks:** 6 (Vision endpoint, Claude integration, extraction logic, validation, logging, error handling)
**Requirements Mapped:** 6 (VISION-01 to 06) + QUALITY-03 + PERF-03
**Autonomous:** YES (depends on Plan 1 for foundation)

**Deliverables:**
- POST /api/analyze-chart endpoint (multipart/form-data)
- Claude Vision API integration with structured prompt
- Extraction: trend (bullish/bearish/consolidating)
- Extraction: swing highs/lows, support/resistance zones, chart patterns
- Price validation (no hallucinated data)
- Structured JSON response schema
- Audit logging to audit_logs table
- Error handling + timeouts

**Files Modified:** 6
- backend/routes/analyze.py
- backend/services/ (vision.py, image_processor.py)
- backend/utils/prompts.py
- backend/schemas/vision.py
- backend/main.py

---

### Plan 4: Reasoning & Results Display (Wave 2)
**Objective:** Generate trade scenarios from Vision JSON. Build result display components.
**Duration:** 4-5 days
**Tasks:** 8 (Reasoning endpoint, Claude integration, R:R calculation, React components: trend badge, zones, trade idea, explanation, disclaimers)
**Requirements Mapped:** 12 (REASON-01 to 05, OUTPUT-01 to 07, QUALITY-01 to 02, UX-06)
**Autonomous:** YES (depends on Plans 1, 3)

**Deliverables:**
- POST /api/reason endpoint (accepts Vision JSON)
- Claude Reasoning API with structured prompt
- 1-2 trade scenarios generation (direction, entry, SL, TP)
- R:R ratio calculation (TP-entry / entry-SL)
- Confidence scoring (0-65% capped)
- Mentor-style explanation (3-5 sentences)
- React components:
  - TrendBadge (Bullish/Bearish/Consolidating)
  - ZoneCard (support/resistance with touch counts)
  - TradeIdeaCard (direction, entry, SL, TP, R:R, confidence)
  - MentorExplanation component
  - Disclaimers component (prominent legal notices)
  - Context display (pair, timeframe)

**Files Modified:** 8
- backend/routes/reason.py
- backend/services/reasoning.py
- backend/utils/prompts.py
- backend/schemas/reasoning.py
- backend/main.py
- frontend/components/ (result-display.tsx, trend-badge.tsx, zone-card.tsx, trade-idea-card.tsx, mentor-explanation.tsx, disclaimers.tsx)

---

### Plan 5: Quality Validation & Consistency Testing (Wave 3)
**Objective:** Implement consistency testing, hallucination detection, confidence capping, disclaimers.
**Duration:** 3-4 days
**Tasks:** 5 (Consistency tests, hallucination detection, confidence capping, disclaimers, error handling)
**Requirements Mapped:** 6 (QUALITY-01 to 06) + REASON-03, REASON-05
**Autonomous:** YES (depends on Plans 3, 4)

**Deliverables:**
- Pytest test suite (20+ tests)
- Consistency tests: run same chart 5 times → identical output
- Hallucination detection: validate entry/SL/TP prices against chart visuals
- Confidence capping: force max 65% in code
- Low-confidence flagging: <50% marked unreliable
- Volatility/gap detection and warnings
- Rejection logic: "Unable to analyze chart" for failed extractions
- Prominent legal disclaimers (educational, not financial advice)
- Error handling for edge cases

**Files Modified:** 7
- backend/tests/ (test_vision_consistency.py, test_hallucination_detection.py, test_confidence_capping.py)
- backend/utils/validation.py
- backend/services/ (vision.py, reasoning.py)
- frontend/components/disclaimers.tsx

---

### Plan 6: Performance & Caching (Wave 3)
**Objective:** Optimize response times to <5s. Implement image hash caching with 48h TTL.
**Duration:** 3-4 days
**Tasks:** 5 (Cache implementation, API timeout handling, monitoring, lazy loading, load testing)
**Requirements Mapped:** 4 (PERF-01 to 04)
**Autonomous:** YES (depends on Plans 3, 4)

**Deliverables:**
- Redis cache by image hash (SHA256)
- 48h TTL cache strategy
- Cache hit response: <500ms
- Cache miss response: <5s (typical)
- Claude API timeout handling (10s max)
- Timeout fallback: cached analysis or "try again"
- Monitoring endpoints: /metrics/cache, /metrics/performance
- Frontend skeleton UI while loading
- Load testing: 50+ concurrent requests

**Files Modified:** 7
- backend/cache.py
- backend/routes/analyze.py
- backend/services/image_processor.py
- backend/monitoring.py
- backend/main.py
- frontend/lib/api.ts
- frontend/lib/store.ts

---

### Plan 7: Documentation & Testing (Wave 3)
**Objective:** Complete API docs, setup user testing, write contributing guidelines.
**Duration:** 2-3 days
**Tasks:** 6 (API docs, architecture docs, contributing guide, user testing plan, privacy policy, public beta prep)
**Requirements Mapped:** All 40 v1 requirements documented
**Autonomous:** YES (depends on all previous plans)

**Deliverables:**
- FastAPI auto-generated API documentation (/docs)
- Architecture overview (Vision → JSON → Reasoning pipeline)
- Contributing guidelines with git workflow
- Local development setup guides
- Deployment documentation (Vercel + Railway)
- Privacy & data retention policy
- User testing plan (5-10 traders)
- Feedback/survey form
- Known limitations and Phase 2 roadmap
- License file (MIT) + legal disclaimers

**Files Modified:** 6
- README.md (comprehensive update)
- API.md (new)
- CONTRIBUTING.md (new)
- frontend/README.md (new)
- backend/README.md (new)
- .github/workflows/docs.yml (new)

---

## Wave Assignment (Parallel Execution)

### Wave 1 (Weeks 1-2): Foundation + Frontend UI
- **Plan 1: Foundation** (3-4 days) — DevOps/Backend Lead
- **Plan 2: Frontend UI & Upload** (4-5 days) — Frontend Engineer
- **Parallel:** Both teams work independently; Plan 1 provides scaffolding for Plan 2

### Wave 2 (Weeks 2-3): Vision API + Reasoning
- **Plan 3: Vision API** (4-5 days) — Backend Engineer + AI Engineer
- **Plan 4: Reasoning & Display** (4-5 days) — Backend Engineer + Frontend Engineer
- **Parallel:** Can run simultaneously; Plan 4 depends on Plan 3 Vision output format

### Wave 3 (Weeks 4-6): Quality, Performance, Docs
- **Plan 5: Quality Validation** (3-4 days) — QA Engineer + Backend Engineer
- **Plan 6: Performance & Caching** (3-4 days) — Backend Engineer + DevOps
- **Plan 7: Documentation & Testing** (2-3 days) — Tech Writer + Product Manager
- **Parallel:** All three can run simultaneously; final integration in Week 6

---

## Requirements Coverage (40/40)

| Category | Count | Plans |
|----------|-------|-------|
| Upload & Processing | 4 | Plan 2 |
| Vision Analysis | 6 | Plan 3 |
| Reasoning Analysis | 5 | Plan 4, 5 |
| Output & Display | 7 | Plan 4, 6 |
| Quality & Trust | 6 | Plan 4, 5 |
| Performance | 4 | Plan 1, 6 |
| UX & Accessibility | 6 | Plan 2, 4 |
| Privacy | 4 | Plan 1 |
| **TOTAL** | **40** | **All 7 Plans** |

✓ Every requirement mapped to exactly one plan
✓ No orphaned requirements
✓ No requirement duplication

---

## Non-Negotiables Addressed

### Privacy First
- ✓ Plan 1: Database schema enforces no image storage
- ✓ Plan 1: audit_logs stores only JSON analysis output
- ✓ Plan 1: 30-day log retention with auto-cleanup
- ✓ Plan 1: No user tracking, cookies, or analytics

### Honest Disclaimers
- ✓ Plan 4: Prominent "educational analysis, not financial advice"
- ✓ Plan 4: "Do not trade based solely on this tool"
- ✓ Plan 5: No language implying financial advice ("should," "recommend," "buy," "sell")

### No Hallucinations
- ✓ Plan 3: Price validation against chart data
- ✓ Plan 5: Hallucination detection tests
- ✓ Plan 5: Rejection logic for failed extractions

### Confidence Caps
- ✓ Plan 4: Confidence capped at 65%
- ✓ Plan 5: Confidence capping tests + code enforcement
- ✓ Plan 5: Low-confidence flagging (<50%)

### Stateless MVP (Phase 1)
- ✓ Plan 1: No user account table
- ✓ Plan 1: No persistence beyond 30-day audit logs
- ✓ Plan 2: Stateless upload (no session storage)

### Forex Only
- ✓ Plan 3: Vision prompt specifies forex pairs only
- ✓ Plan 4: Mentor explanation assumes forex context

### No Automated Trading
- ✓ Plan 4: Display says "possible scenario" (not "do this")
- ✓ Plan 4: Disclaimers emphasize user decision-making

---

## Critical Success Factors

✓ **Vision Accuracy:** Test with 20+ real forex charts by end of Week 3 (Plan 3 acceptance criteria)
✓ **Consistency:** Same chart analyzed 5 times produces identical output (Plan 5)
✓ **Response Time:** <5s for typical chart, <500ms for cached requests (Plan 6)
✓ **User Trust:** Legal disclaimers prominent and clear (Plan 4, 5)
✓ **Privacy:** Zero chart images stored; JSON logs deleted after 30 days (Plan 1)

---

## Execution Checklist

- [ ] Plan 1 (Foundation) executed and verified
- [ ] Plan 2 (Frontend UI) executed and verified
- [ ] Plan 3 (Vision API) executed and verified
- [ ] Plan 4 (Reasoning & Display) executed and verified
- [ ] Plan 5 (Quality Validation) executed and verified
- [ ] Plan 6 (Performance & Caching) executed and verified
- [ ] Plan 7 (Documentation & Testing) executed and verified
- [ ] All 40 requirements tested and passing
- [ ] User testing with 5-10 traders completed
- [ ] Legal review of disclaimers completed
- [ ] Public beta ready for launch

---

## Next Steps

1. **Assign Team Members** to each plan (see Duration and Team assignments above)
2. **Run /gsd-execute-phase 1 to start Wave 1** (Plans 1 and 2 in parallel)
3. **Monitor Critical Path:** Vision accuracy (Plan 3) is critical blocker for Plans 4-6
4. **Daily Standups:** Sync across frontend/backend to track Vision JSON output format early
5. **Weekly Gate Reviews:** After each Wave, verify requirements satisfaction before moving to next Wave

---

**Status:** Ready for Execution
**Created:** 2025-05-19
**Mode:** YOLO (auto-approve at phase transitions)
