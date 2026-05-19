---
wave: 3
depends_on:
  - 04-PLAN-vision-api.md
  - 05-PLAN-reasoning-display.md
files_modified:
  - backend/cache.py
  - backend/routes/analyze.py
  - backend/services/image_processor.py
  - backend/monitoring.py
  - backend/main.py
  - frontend/lib/api.ts
  - frontend/lib/store.ts
autonomous: true
---

# Plan 6: Performance & Caching
**Objective:** Optimize response times to <5s (typical chart). Implement image hash caching with 48h TTL, API timeout handling with cached fallback, monitoring endpoints, lazy loading. Test with real charts and measure latency.

## What We're Building
Redis cache by image hash (SHA256) with 48h TTL to avoid re-processing identical charts. API timeout handling: if Claude takes >10s, return cached analysis or "try again" message. Response time monitoring: track vision, reasoning, frontend latency. Frontend lazy loading: show skeleton UI while backend processes.

## Must-Haves
1. Image hash caching: SHA256 of image → analysis JSON
2. Cache TTL: 48 hours
3. Cache lookup before calling Claude
4. Cache hit response time: <500ms
5. Cache miss response time: <5s (typical)
6. Claude API timeout: 10s max wait
7. Timeout fallback: cached analysis if available, else "try again"
8. Monitor vision latency: target <3s
9. Monitor reasoning latency: target <2s
10. Frontend skeleton UI while loading
11. /metrics/performance endpoint
12. Load test: 50+ concurrent requests

## Requirements Mapped
- PERF-01: <5s response time (vision + reasoning + display)
- PERF-02: Claude API timeout → cache fallback or "try again"
- PERF-03: Log all analyses (already in audit_logs)
- PERF-04: Cache by image hash, 48h TTL

**Duration:** 3-4 days | **Team:** Backend Engineer + DevOps

---

*Plan created: 2025-05-19*
