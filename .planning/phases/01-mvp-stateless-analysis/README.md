# Phase 1: MVP Stateless Analysis — Planning Index

## Start Here

1. **00-PLANNING-SUMMARY.md** (12.7 KB)
   - Comprehensive overview of all 7 plans
   - Wave assignment and parallel execution strategy
   - Requirements coverage matrix (40/40)
   - Non-negotiables checklist
   - Execution checklist and next steps

2. **01-CONTEXT.md** (7.9 KB) — *Already Existed*
   - Phase boundary and goals
   - Implementation decisions (locked)
   - Team notes and timeline
   - Canonical references (required reading)

## Detailed Plans (7 Total, 4-6 Weeks)

### Wave 1: Foundation + Frontend UI (Weeks 1-2)

**02-PLAN-foundation.md** (1.6 KB)
- Objective: Project scaffolding, CI/CD, deployment, database
- Duration: 3-4 days
- Team: DevOps/Backend Lead
- Autonomous: YES (no dependencies)
- Requirements Mapped: 7 (PRIVACY-01/02/03/04, PERF-02/03/04)
- Deliverables: Monorepo, GitHub Actions, Vercel/Railway, PostgreSQL, Redis cache, docker-compose
- Files Modified: 12 (package.json, .env.example, CI/CD workflows, etc.)

**03-PLAN-frontend-ui.md** (1.9 KB)
- Objective: Upload interface with drag-drop, theme, i18n
- Duration: 4-5 days
- Team: Frontend Engineer
- Autonomous: YES (depends on Plan 1 scaffold)
- Requirements Mapped: 10 (UPLOAD-01/02/03/04, UX-01/02/03/04/05/06)
- Deliverables: UploadBox, validation, Zustand store, next-themes, next-i18n, mobile-responsive
- Files Modified: 11 (components, lib, config, locales)

### Wave 2: Vision API + Reasoning (Weeks 2-3)

**04-PLAN-vision-api.md** (1.9 KB)
- Objective: Claude Vision API endpoint, extract trend/zones/patterns
- Duration: 4-5 days
- Team: Backend Engineer + AI Engineer
- Autonomous: YES (depends on Plan 1)
- Requirements Mapped: 7 (VISION-01/02/03/04/05/06, QUALITY-03, PERF-03)
- Deliverables: POST /api/analyze-chart, Claude Vision integration, price validation, JSON output
- Files Modified: 6 (routes, services, schemas, prompts)

**05-PLAN-reasoning-display.md** (2.7 KB)
- Objective: Generate trade scenarios, build result components
- Duration: 4-5 days
- Team: Backend Engineer + Frontend Engineer
- Autonomous: YES (depends on Plans 1, 3)
- Requirements Mapped: 12 (REASON-01/02/03/04/05, OUTPUT-01/02/03/04/05/06/07, QUALITY-01/02, UX-06)
- Deliverables: POST /api/reason, R:R calculation, TrendBadge, ZoneCard, TradeIdeaCard, MentorExplanation, Disclaimers
- Files Modified: 8 (routes, services, React components)

### Wave 3: Quality, Performance, Docs (Weeks 4-6)

**06-PLAN-quality-validation.md** (2.1 KB)
- Objective: Consistency testing, hallucination detection, confidence capping
- Duration: 3-4 days
- Team: QA Engineer + Backend Engineer
- Autonomous: YES (depends on Plans 3, 4)
- Requirements Mapped: 8 (QUALITY-01/02/03/04/05/06, REASON-03/05)
- Deliverables: Pytest suite (20+ tests), consistency tests, hallucination detection, confidence enforcement, legal disclaimers
- Files Modified: 7 (test files, validation utilities, services, components)

**07-PLAN-performance-cache.md** (1.7 KB)
- Objective: <5s response time, image hash caching (48h), API timeout handling
- Duration: 3-4 days
- Team: Backend Engineer + DevOps
- Autonomous: YES (depends on Plans 3, 4)
- Requirements Mapped: 4 (PERF-01/02/03/04)
- Deliverables: Redis cache by image hash, 48h TTL, <500ms cache hits, <5s misses, monitoring endpoints, load testing
- Files Modified: 7 (cache, routes, services, monitoring, API utilities)

**08-PLAN-docs-testing.md** (1.7 KB)
- Objective: API documentation, user testing, contributing guidelines
- Duration: 2-3 days
- Team: Tech Writer + Product Manager
- Autonomous: YES (depends on all previous plans)
- Requirements Mapped: All 40 v1 requirements documented
- Deliverables: API docs, architecture guide, contributing guide, privacy policy, user testing (5-10 traders), feedback form
- Files Modified: 6 (README, API.md, CONTRIBUTING.md, guides, CI/CD docs)

---

## Quick Reference

### By Requirement Category

| Category | Count | Plan |
|----------|-------|------|
| Upload & Processing | 4 | 03 |
| Vision Analysis | 6 | 04 |
| Reasoning Analysis | 5 | 05, 06 |
| Output & Display | 7 | 05, 07 |
| Quality & Trust | 6 | 05, 06 |
| Performance | 4 | 02, 07 |
| UX & Accessibility | 6 | 03, 05 |
| Privacy | 4 | 02 |
| **TOTAL** | **40** | **All 7** |

### By Timeline

- **Week 1-2 (Wave 1):** Plans 02, 03 (Foundation + Frontend)
- **Week 2-3 (Wave 2):** Plans 04, 05 (Vision API + Reasoning)
- **Week 4-6 (Wave 3):** Plans 06, 07, 08 (Quality + Performance + Docs)

### By Team

- **Frontend Engineer:** Plans 03, 05 (UI/components)
- **Backend Engineer:** Plans 02, 04, 05, 06, 07 (infrastructure, APIs, cache)
- **AI/Prompts Engineer:** Plans 04, 05 (Claude Vision/Reasoning)
- **QA Engineer:** Plans 06, 07 (testing, validation)
- **DevOps/Tech Writer:** Plans 02, 07, 08 (infrastructure, docs)

---

## Execution Workflow

### Before Starting (Preparation)

1. Read this index file (you are here)
2. Read **01-CONTEXT.md** for phase goals and decisions
3. Read **00-PLANNING-SUMMARY.md** for comprehensive overview
4. Assign team members to plans based on duration/team assignments above
5. Run /gsd-execute-phase 1 to begin Wave 1 execution

### During Execution (Per Plan)

1. Executor reads all canonical references (ROADMAP.md, REQUIREMENTS.md, AGENTS.md)
2. Executor reads **read_first** files for each task
3. Executor implements **action** steps with exact values (not vague suggestions)
4. Executor verifies **acceptance_criteria** before marking task complete
5. Commit changes after each task with clear messages
6. Escalate blockers immediately (ask for help in real-time)

### After Execution (Per Wave)

1. Verify all acceptance criteria for all plans in the wave
2. Run test suites (frontend lint/build, backend pytest)
3. Verify all files modified match expected outputs
4. Gate review before advancing to next wave

### At Phase Transition

1. Run /gsd-transition to update PROJECT.md
2. Log decisions, challenges, and lessons learned
3. Update STATE.md with progress
4. Prepare Phase 2 planning if validation successful

---

## Key Success Factors

✓ **Vision Accuracy:** Test with 20+ real forex charts (Plan 04 acceptance)
✓ **Consistency:** Same chart 5× = identical output (Plan 06 testing)
✓ **Performance:** <5s for typical, <500ms for cached (Plan 07)
✓ **Privacy:** Zero images stored, 30-day JSON retention (Plan 02 schema)
✓ **Confidence:** Capped at 65%, <50% flagged as unreliable (Plan 05)
✓ **Trust:** Prominent legal disclaimers, educational tone (Plan 04, 05)

---

## Troubleshooting

**Question:** Which plan should I start with?
**Answer:** Always start with Plan 02 (Foundation) — it's Wave 1 and has no dependencies.

**Question:** Can I run Plans 03 and 05 in parallel?
**Answer:** NO — Plan 05 depends on Plan 04 output (Vision JSON schema). Wave 2 must complete Vision API first.

**Question:** What if Vision extraction is unreliable?
**Answer:** Escalate immediately in Week 2. This blocks Plans 04-06. Iterate on Claude Vision prompt and test data.

**Question:** Can I skip Plan 06 (Quality Validation)?
**Answer:** NO — non-negotiable. QUALITY-01/02 (disclaimers), QUALITY-05 (consistency), and confidence capping are required.

**Question:** How do I know if I'm done with a task?
**Answer:** All acceptance_criteria must be grep-verifiable (check files, grep patterns, verify outputs).

---

## Navigation

- **For Phase Execution:** Start with Plan 02 → 03 → 04 → 05 → 06 → 07 → 08
- **For Team Leads:** See "By Team" section above to assign plans
- **For Requirement Traceability:** See "By Requirement Category" table
- **For Timeline Planning:** See "By Timeline" section

---

**Last Updated:** 2025-05-19
**Status:** READY FOR EXECUTION
**Mode:** YOLO (auto-approve at phase transitions)
