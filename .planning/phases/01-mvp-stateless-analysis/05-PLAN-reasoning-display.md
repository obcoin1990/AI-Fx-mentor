---
wave: 2
depends_on:
  - 02-PLAN-foundation.md
  - 04-PLAN-vision-api.md
files_modified:
  - backend/routes/reason.py
  - backend/services/reasoning.py
  - backend/utils/prompts.py
  - backend/schemas/reasoning.py
  - backend/main.py
  - frontend/components/result-display.tsx
  - frontend/components/trend-badge.tsx
  - frontend/components/zone-card.tsx
  - frontend/components/trade-idea-card.tsx
  - frontend/components/mentor-explanation.tsx
  - frontend/components/disclaimers.tsx
autonomous: true
---

# Plan 4: Reasoning & Results Display
**Objective:** Implement Claude Reasoning API to generate trade scenarios from vision JSON. Build React components to display trend badge, zone cards, trade idea card, mentor explanation, and legal disclaimers.

## What We're Building
FastAPI POST /api/reason endpoint that accepts vision JSON output, calls Claude 3.5 Sonnet Reasoning API with structured prompt, generates 1-2 trade scenarios (direction, entry, SL, TP) with R:R calculations and confidence scores (capped 65%), produces mentor-style explanation. Frontend React components for visual hierarchy: trend badge → zone cards → trade idea card → mentor explanation + disclaimers.

## Must-Haves
1. POST /api/reason endpoint (accepts vision JSON)
2. Claude Reasoning API integration with prompt
3. Generate 1-2 trade scenarios (direction, entry, SL, TP)
4. Calculate R:R ratio for each scenario (TP-entry / entry-SL)
5. Assign confidence score (0-65%, capped)
6. Flag confidence <50% as unreliable
7. Mentor-style explanation (3-5 sentences, plain English)
8. Return structured JSON response
9. Trend badge component (Bullish/Bearish/Consolidating)
10. Support zone card (price range, # touches)
11. Resistance zone card (price range, # touches)
12. Trade idea card (direction, entry, SL, TP, R:R, confidence)
13. Mentor explanation component (3-5 sentences)
14. Legal disclaimers (educational analysis, not financial advice)
15. Display pair and timeframe context
16. Visual hierarchy with clear spacing and typography

## Requirements Mapped
- REASON-01: Generate 1-2 trade scenarios
- REASON-02: Calculate risk-reward ratio
- REASON-03: Assign confidence (0-65% capped)
- REASON-04: Mentor-style explanation
- REASON-05: Flag low confidence (<50%)
- OUTPUT-01: Trend badge display
- OUTPUT-02: Support zone card
- OUTPUT-03: Resistance zone card
- OUTPUT-04: Trade idea card
- OUTPUT-05: Mentor explanation
- OUTPUT-06: Confidence score display
- OUTPUT-07: Pair/timeframe context
- QUALITY-01: Educational disclaimer
- QUALITY-02: Non-advice disclaimer
- UX-06: Visual hierarchy

**Duration:** 4-5 days | **Team:** Backend Engineer (reasoning) + Frontend Engineer (UI)

---

*Plan created: 2025-05-19*
