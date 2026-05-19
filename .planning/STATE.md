# Project State: AI Chart Mentor

**Last Updated:** 2025-05-19
**Current Phase:** Phase 1 (MVP Initialization)
**Status:** Ready for Execution

---

## Project Reference

See: `.planning/PROJECT.md` (updated 2025-05-19)

**Core Value:** Traders get instant, structured, objective chart analysis from a screenshot — eliminating manual analysis and emotional decisions.

**Current Focus:** Phase 1 MVP — Stateless analysis (upload → analyze → display)

---

## Phase 1 Progress

**Phase 1:** MVP Stateless Analysis
**Duration:** 4-6 weeks
**Status:** ⏳ Not Started (Ready to Plan)

### Requirements Coverage

| Category | Count | Status |
|----------|-------|--------|
| Upload & Processing | 4 | Mapped ✓ |
| AI Vision | 6 | Mapped ✓ |
| AI Reasoning | 5 | Mapped ✓ |
| Display & Output | 7 | Mapped ✓ |
| Quality & Trust | 6 | Mapped ✓ |
| Performance | 4 | Mapped ✓ |
| UX & Accessibility | 6 | Mapped ✓ |
| Privacy | 4 | Mapped ✓ |
| **Total** | **40** | **✓ 100% Mapped** |

### Success Criteria

1. ⏳ Upload works (mobile/tablet/desktop, drag-drop, validation)
2. ⏳ Vision model reliably extracts trend, zones, patterns
3. ⏳ Reasoning generates 1-2 scenarios with R:R, confidence (capped 65%)
4. ⏳ Display clear with visual hierarchy + disclaimers
5. ⏳ Response time <5s; cache hits near-instant
6. ⏳ Privacy maintained (no image storage, 30-day JSON logs only)
7. ⏳ Consistency (same chart = same output)
8. ⏳ User testing shows traders trust the analysis

### Implementation Breakdown (by week)

**Week 1: Foundation**
- [ ] Initialize Next.js 16 frontend + FastAPI backend
- [ ] Set up dark/light theme system + i18n (EN/AR/CN with RTL)
- [ ] Configure deployment (Vercel, Railway, Supabase)
- [ ] Create file upload UI (drag-drop, validation)

**Week 2-3: Vision Model**
- [ ] Design Claude Vision API contract (extract trend, zones, patterns → JSON)
- [ ] Implement vision endpoint + error handling
- [ ] Test on 20+ real forex charts
- [ ] Validate extraction accuracy (trend, swing highs/lows, zones, patterns)

**Week 4-5: Reasoning & Display**
- [ ] Design Claude Reasoning API contract (generate scenarios, R:R, confidence, mentor explanation)
- [ ] Implement reasoning endpoint
- [ ] Build result display components (trend badge, zone cards, idea card, explanation)
- [ ] Add disclaimers prominently
- [ ] Implement confidence capping (max 65%)

**Week 6: Quality & Launch**
- [ ] Performance optimization (caching, timeouts, error handling)
- [ ] Consistency testing (same chart → same output)
- [ ] Legal review of disclaimers
- [ ] User testing (5-10 traders)
- [ ] Public beta launch

### Tech Stack

**Frontend:**
- Next.js 16 + React 19
- TailwindCSS v3
- next-themes (dark/light)
- next-i18n (EN/AR/CN)
- Zustand (state management)

**Backend:**
- FastAPI 0.104
- Uvicorn
- Claude 3.5 Sonnet API
- Anthropic SDK

**Database & Cache:**
- PostgreSQL 18 (Supabase) — audit logs
- Redis — image hash cache (48h TTL)

**Deployment:**
- Vercel (frontend)
- Railway (FastAPI backend)
- Supabase (PostgreSQL + cleanup jobs)

**Monitoring:**
- Sentry (error tracking)
- LogRocket (session replay)

---

## Upcoming Phases

### Phase 2: Accounts & Learning (Weeks 7-20)

After Phase 1 MVP is shipped and validated:
- User accounts (Supabase Auth)
- Analysis history + search/filter
- Feedback loop (helpful? outcome? accuracy tracking)
- Multi-timeframe analysis (1H, 4H, 1D consensus)
- Extended assets (Crypto: BTC/USDT, ETH/USDT; Indices: SPX, DAX, etc.)
- Pattern performance tracking + auto-disable low-accuracy patterns
- A/B test Claude vs GPT-4o

**Success Gates:**
- 100+ daily active traders using MVP
- >80% report analysis is helpful
- Patterns with >60% accuracy enabled; <60% disabled

### Phase 3: Scale & Automation (Weeks 21+)

After Phase 2 learning feedback loops are validated:
- TradingView browser extension
- Real-time alerts on new setups
- Personalized mentor profiles
- REST + GraphQL API
- Backtesting engine
- Risk simulator

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Vision model hallucination** | Users see made-up price levels | Validate extracted prices against chart data; reject if mismatch |
| **Reasoning low quality** | Users don't trust scenarios | Test on 50+ charts; iterate prompts; flag low-confidence analyses |
| **Slow response time** | Users abandon tool | Cache by image hash; pre-compute patterns; timeout at 10s |
| **Legal liability** | Regulatory action, lawsuits | Prominent disclaimers; cap confidence at 65%; never claim "financial advice" |
| **API rate limits** | Service crashes under load | Implement request queuing + backoff; cache to reduce re-processing |
| **User data breach** | Privacy violation, trust loss | Don't store images; encrypt logs; 30-day retention with auto-delete |

---

## Key Decisions

| Decision | Rationale | Status |
|----------|-----------|--------|
| Forex-only Phase 1 | Reduces scope, validates quality before extending | ✓ Approved |
| No user accounts Phase 1 | Faster shipping, simpler MVP | ✓ Approved |
| Vision → JSON → Reasoning | Separates concerns, enables caching, easier debugging | ✓ Approved |
| Confidence capped 65% | Prevents false confidence, disclaimers more credible | ✓ Approved |
| Claude 3.5 Sonnet for both | Consistent quality, cost-effective | ✓ Approved |
| Image hash cache (48h) | Avoids re-processing, reduces API costs | ✓ Approved |
| 30-day audit log retention | Balance debugging + privacy | ✓ Approved |
| Vertical MVP structure | Ship end-to-end feature every phase | ✓ Approved |
| Fine granularity, parallel execution | 8-12 fine-grained phases; independent tasks run in parallel | ✓ Approved |
| YOLO mode, all agents enabled | Auto-approve; research, plan-check, verifier all enabled | ✓ Approved |

---

## Next Steps

**Immediate (This Week):**
1. Review ROADMAP.md with team
2. Confirm Phase 1 timeline (4-6 weeks)
3. Assign team members to core areas (frontend, backend, AI prompts)
4. Provision cloud infrastructure (Vercel, Railway, Supabase accounts)
5. Create GitHub repos for frontend, backend

**Next Week (Week 1):**
1. Initialize Next.js 16 + FastAPI projects
2. Set up CI/CD (GitHub Actions)
3. Configure dark/light theme + i18n
4. Build file upload UI (drag-drop, validation)

**Week 2-3:**
1. Implement Claude Vision API (extract trend, zones, patterns)
2. Test on 20+ real charts
3. Iterate on vision prompts for accuracy

**Week 4-6:**
1. Implement Claude Reasoning API
2. Build display components
3. Performance optimization + testing
4. User testing + feedback
5. Public beta launch

---

*Project initialized: 2025-05-19*
*Ready for Phase 1 planning: `/gsd-plan-phase 1`*
