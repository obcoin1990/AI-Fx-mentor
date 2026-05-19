# AI Chart Mentor: Architecture Research - Complete Index

## Overview

This research package provides comprehensive architecture patterns for AI Chart Mentor, addressing all questions about component design, data flow, scaling, and multi-phase evolution.

**Status**: Complete architecture research with implementation-ready patterns
**Last Updated**: May 19, 2026
**Total Documentation**: 12 guides covering all aspects

---

## Quick Navigation

### For Different Audiences:

**If you're building now (Phase 1):**
1. Start: QUICK_REFERENCE.md (this guide)
2. Then: ARCHITECTURE.md (sections 1-3)
3. Reference: IMPLEMENTATION_REFERENCE.md
4. Build: Use the code skeletons provided

**If you're planning Phase 2:**
1. Read: PHASE_ARCHITECTURE.md (Phase 2 section)
2. Review: SCALING_PATTERNS.md
3. Plan: Database & cache infrastructure

**If you're evaluating options:**
1. Start: EXECUTIVE_SUMMARY.md
2. Deep dive: Component sections in ARCHITECTURE.md
3. Decision matrix: PHASE_ARCHITECTURE.md (end)

---

## Document Guide

### Core Architecture Documents

1. **ARCHITECTURE.md** (12KB, 400 lines)
   - Component architecture (Phase 1)
   - Data flow complete pipeline
   - Image validation & preprocessing
   - Error handling strategies
   - Build order & dependencies
   - Architecture evolution

2. **IMPLEMENTATION_REFERENCE.md** (11KB, 350 lines)
   - API contract & response shapes
   - Service implementation skeletons
   - Validation schemas (Zod)
   - Error handling patterns
   - Frontend integration examples
   - Testing checklist

3. **SCALING_PATTERNS.md** (13KB, 400 lines)
   - Image hash caching (in-memory)
   - Redis caching (Phase 2)
   - Rate limiting strategies
   - Error recovery & circuit breakers
   - Queue-based processing (Bull/Redis)
   - Prometheus metrics
   - Cost optimization

4. **PHASE_ARCHITECTURE.md** (13KB, 400 lines)
   - Phase 1 architecture diagram
   - Phase 1 data flow step-by-step
   - Phase 2 architecture evolution
   - Phase 2 database schema
   - Phase 3 real-time architecture
   - Migration paths between phases
   - Decision matrix

### Summary Documents

5. **QUICK_REFERENCE.md**
   - One-page architecture summary
   - Key decisions with rationale
   - Phase comparison table
   - Implementation order
   - Common pitfalls
   - Tech stack

6. **EXECUTIVE_SUMMARY.md**
   - Vision ? JSON ? Reasoning validation
   - Component boundaries explained
   - Why separation of concerns matters
   - Scaling approach overview
   - Phase progression roadmap

---

## Answer to Each Research Question

### 1. Component Architecture

**Question**: How should chart analysis pipelines be structured?

**Answer**: (ARCHITECTURE.md, Section 1)
- 4-layer architecture: Frontend ? API Route ? Services ? APIs
- API route acts as orchestrator
- Vision & Reasoning are separate, testable services
- Clear error handling layer

**Question**: Vision model ? JSON extraction vs end-to-end analysis?

**Answer**: (ARCHITECTURE.md, Section 1.3)
- Vision ? JSON IS THE RIGHT APPROACH
- Enables validation, caching, error recovery
- Easier debugging & testing
- Cost optimization opportunities

**Question**: Separation of concerns patterns?

**Answer**: (ARCHITECTURE.md, Section 1.4)
- Pattern A: Service layer abstraction (swap Claude ? GPT-4o)
- Pattern B: Validation layer (Zod schemas)
- Pattern C: Error handling service (centralized)

**Question**: Error handling for bad chart images?

**Answer**: (ARCHITECTURE.md, Section 1.5)
- 3-stage error detection: Input ? Extraction ? Validation
- User-friendly error messages
- Graceful fallbacks for service failures

---

### 2. Data Flow

**Question**: Upload ? Vision ? JSON ? Reasoning ? Response pipeline?

**Answer**: (ARCHITECTURE.md, Section 2, PHASE_ARCHITECTURE.md)
- 8-step detailed flow documented
- 10-20 second total latency
- Step-by-step error handling at each stage

**Question**: Where to validate extracted chart data?

**Answer**: (ARCHITECTURE.md, Section 2.2)
- Layered validation: Client ? API Input ? Extraction ? Analysis
- Schema validation with Zod
- Business logic validation (numbers are reasonable)

**Question**: Image preprocessing (crop, rotate, enhance)?

**Answer**: (ARCHITECTURE.md, Section 2.3)
- MIME type check
- Size bounds check (1KB-10MB)
- Dimension check (400x300 to 4000x4000)
- EXIF auto-rotation
- Optional whitespace crop
- Optional quality enhancement
- Recommended tool: `sharp` for Node.js

**Question**: Output formatting and caching?

**Answer**: (ARCHITECTURE.md, Section 2.4 & 2.5)
- Caching via SHA256 image hash
- 7-day TTL
- Cost savings: ~$0.003 per cached image
- Response schema documented with all fields

---

### 3. Scaling Considerations

**Question**: How do platforms handle high-volume requests?

**Answer**: (SCALING_PATTERNS.md, Sections 1-3)
- Phase 1: Synchronous (10-15s baseline, works < 50 RPM)
- Phase 2: Add rate limiting (20 RPM per user)
- Phase 2+: Add async queue (500+ RPM with Bull)

**Question**: Queue vs synchronous processing?

**Answer**: (SCALING_PATTERNS.md, Section 4)
- Synchronous: Simple, good for MVP validation
- Queue-based: Better for > 100 analyses/day
- Provides code for both patterns

**Question**: Model caching strategies?

**Answer**: (SCALING_PATTERNS.md, Section 1 & 3)
- Vision: Cache extractions by image hash
- Reasoning: Cache system prompts
- Cost reduction: 40% savings via caching

**Question**: Fallback when models are slow/erroring?

**Answer**: (SCALING_PATTERNS.md, Section 3)
- Timeouts: Vision 30s, Reasoning 15s
- Retry logic: Exponential backoff (max 3 attempts)
- Circuit breaker: Auto-open after 5 failures
- Fallback response: Safe default analysis

---

### 4. Integration Patterns (Phase 2+)

**Question**: How to integrate with external trading data?

**Answer**: (ARCHITECTURE.md, Section 4)
- Phase 2: Real-time price enrichment
- Phase 2: Validate S/R against historical
- Phase 3: Broker API connections
- Phase 3: Economic calendar integration

**Question**: TradingView API integration patterns?

**Answer**: (ARCHITECTURE.md, Section 4.2)
- Service abstraction for TradingView API
- Get live price
- Get historical bars
- Validate extracted levels against history

**Question**: Broker API connections?

**Answer**: (ARCHITECTURE.md, Section 4.3)
- MT5 via Python backend wrapper
- Account balance integration
- Position size calculation
- One-click order placement (Phase 3)

**Question**: Real-time chart streaming approaches?

**Answer**: (ARCHITECTURE.md, Section 4.4)
- WebSocket for real-time price updates
- Server-Sent Events alternative
- Live price ? auto-update trade ideas

---

### 5. Multi-Timeframe Support (Phase 2)

**Question**: How should multi-timeframe analysis be structured?

**Answer**: (PHASE_ARCHITECTURE.md, Section 5)
- Option A: Single request ? Multiple analyses (Recommended)
- Option B: Separate requests per timeframe
- Option A saves 40% in vision extraction costs

**Question**: Single request ? multiple analyses or separate requests?

**Answer**: (PHASE_ARCHITECTURE.md, Section 5.1)
- Single request: User uploads M5 chart ? API analyzes as M5, H1, H4
- Share vision extraction across analyses
- More efficient

**Question**: Analysis correlation across timeframes?

**Answer**: (PHASE_ARCHITECTURE.md, Section 5.3)
- Confluence scoring: How much do timeframes agree?
- Alignment percentage (0-100)
- Divergence warnings
- Higher confidence if all timeframes align

---

## Architecture Decision Summary

### Vision ? JSON ? Reasoning Pipeline ? CORRECT

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Pipeline Style** | Vision ? JSON ? Reasoning | Separates concerns, enables caching, easier debugging |
| **Vision Model** | Claude 3.5 Sonnet Vision | Excellent chart understanding, good cost |
| **Reasoning Model** | Claude 3.5 Sonnet | Consistent quality with vision, good cost |
| **API Style** | Synchronous (Phase 1) | Simple, fast to ship, validates product |
| **Async Processing** | Queue-based (Phase 2+) | Bull Queue + Redis, scales to 500+ RPM |
| **Caching** | Image hash ? Extraction | Save ~40% costs, especially multi-user |
| **Error Strategy** | Fallback response | Return 200 with safe default instead of 5xx |
| **Authentication** | Supabase (Phase 2+) | Built-in auth, PostgreSQL, good pricing |

---

## Build Order (Recommended)

### Phase 1 MVP (18-24 hours)

```
Week 1:
+- Day 1-2: API infrastructure + vision service
+- Day 2-3: Reasoning service + validation
+- Day 3-4: Frontend UI + E2E testing

Deliverables:
+- /api/analyze-chart endpoint ?
+- Vision extraction service ?
+- Reasoning service ?
+- ChartUpload component ?
+- AnalysisDisplay components ?
+- Deployed to Vercel ?
```

### Phase 2 Scale (23-29 hours, can start after Phase 1 ships)

```
Week 3-4:
+- Supabase setup + auth
+- Redis cache layer
+- Rate limiting
+- History API endpoints
+- Multi-timeframe support
+- Image annotation (optional)
```

### Phase 3 Enterprise (19-24 hours)

```
Week 5-6:
+- WebSocket real-time
+- Browser extension
+- Broker integrations
+- Economic calendar
```

---

## Tech Stack (Finalized)

```
FRONTEND:
+- Next.js 14+ (App Router)
+- TailwindCSS + Headless UI
+- React hooks + server actions
+- next-i18next (EN, AR, CN, RTL)
+- next-themes (dark/light)

BACKEND:
+- Next.js API Routes
+- TypeScript
+- Zod (validation)
+- sharp (image processing)
+- axios or fetch (HTTP)

AI/ML:
+- Claude 3.5 Sonnet Vision
+- Claude 3.5 Sonnet Reasoning
+- Structured prompts (JSON output)

INFRASTRUCTURE (Phase 1):
+- Vercel (hosting)
+- Environment variables (secrets)

INFRASTRUCTURE (Phase 2+):
+- Supabase (DB + Auth)
+- Upstash Redis (cache + queue)
+- Bull Queue (async jobs)
+- S3 or Vercel Blob (image storage)
+- Sentry (error tracking)
+- Datadog (metrics)

TESTING:
+- Vitest + @testing-library/react
+- Playwright (E2E)
+- Postman/Insomnia (API)

DEVOPS:
+- GitHub + Actions
+- Vercel auto-deploy
+- Environment branches
```

---

## Common Pitfalls & Solutions

| Pitfall | Why | Solution |
|---------|-----|----------|
| API timeout on first request | Claude rate limits | Implement retry + backoff |
| Bad extraction JSON | Vision model hallucinates | Always validate schema with Zod |
| Inconsistent trade ideas | Vague prompts | Strict prompt format + examples |
| Memory leaks in cache | No TTL on entries | Set cache TTL to 7 days |
| Slow image processing | Large images ? slow upload | Preprocess: resize, compress |
| No debugging context | Minimal logging | Log extraction, latencies, errors |
| Scaling issues at 100+ RPM | No rate limiting | Implement per-IP/user limits |
| Users confused by bad analysis | Low confidence not flagged | Detect & warn on confidence < 40% |

---

## Key Files in This Research Package

All files located in:
`C:\Users\ob-ta\OneDrive\Documents\projectai\OBagent\reseurces\ai-chart-mentor\`

**Read in this order:**
1. QUICK_REFERENCE.md (this document)
2. ARCHITECTURE.md (detailed patterns)
3. IMPLEMENTATION_REFERENCE.md (code + schemas)
4. PHASE_ARCHITECTURE.md (evolution)
5. SCALING_PATTERNS.md (advanced optimization)

---

## Next Steps

### This Week (Start Building Phase 1):
- [ ] Read ARCHITECTURE.md completely
- [ ] Create `/lib/services/vision.service.ts`
- [ ] Create `/lib/services/reasoning.service.ts`
- [ ] Create `/lib/validation/extraction.schema.ts`
- [ ] Create `/app/api/analyze-chart/route.ts`
- [ ] Write unit tests
- [ ] Create ChartUpload component
- [ ] Test end-to-end

### Phase 1 Polish:
- [ ] Error handling (all failure modes)
- [ ] Image preprocessing
- [ ] Loading states
- [ ] Test with 20+ chart images
- [ ] Deploy to Vercel

### Phase 2 Planning (After Phase 1 ships):
- [ ] Design Supabase schema (use PHASE_ARCHITECTURE.md)
- [ ] Plan authentication flow
- [ ] Plan cache key strategy
- [ ] Plan rate limiting thresholds

---

## Architecture Quality Checklist

- ? Separation of concerns (Vision ? Reasoning ? API route)
- ? Layered validation (Client ? API ? Schema ? Business logic)
- ? Error handling strategy (Graceful fallbacks, user-friendly messages)
- ? Scalable foundation (Can add caching, queue, DB without rewrites)
- ? Cost-optimized (Caching reduces Claude API costs by 40%)
- ? Testable services (Mock-friendly interfaces)
- ? Monitoring-ready (Metric hooks already defined)
- ? Phase evolution path (Clear Phase 1 ? 2 ? 3 migration steps)

---

## Final Recommendation

**Your planned Vision ? JSON ? Reasoning pipeline is architecturally sound.**

The modular design enables:
- Easy testing at each stage
- Independent scaling of components
- Cost optimization via caching
- Error recovery with fallbacks
- Clear migration path to phases 2-3

**Focus on:**
1. Getting vision extraction working first
2. Strong validation at each stage
3. User-friendly error messages
4. Test with real chart images

**Don't overthink:**
- Database (add in Phase 2)
- WebSockets (add in Phase 3)
- Broker integrations (add in Phase 3)
- Multi-timeframe (add in Phase 2)

**Ship Phase 1 first. Validate. Then scale.**

