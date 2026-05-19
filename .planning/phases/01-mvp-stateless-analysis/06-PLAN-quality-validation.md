---
wave: 3
depends_on:
  - 04-PLAN-vision-api.md
  - 05-PLAN-reasoning-display.md
files_modified:
  - backend/tests/test_vision_consistency.py
  - backend/tests/test_hallucination_detection.py
  - backend/tests/test_confidence_capping.py
  - backend/utils/validation.py
  - backend/services/vision.py
  - backend/services/reasoning.py
  - frontend/components/disclaimers.tsx
autonomous: true
---

# Plan 5: Quality Validation & Consistency Testing
**Objective:** Implement consistency testing (same chart = same output), hallucination detection (validate prices against chart data), confidence score capping (max 65%), and legal disclaimers. Establish quality gates before production.

## What We're Building
Pytest test suite for vision/reasoning consistency (run same chart 5 times, verify identical output), hallucination detection (validate all entry/SL/TP prices visible on chart), confidence capping logic (force max 65%), low-confidence flagging (<50%), volatility/gap warnings. React disclaimers component with prominent legal notices and educational tone.

## Must-Haves
1. Consistency test: run same chart 5 times → identical output
2. Hallucination detection: validate entry/SL/TP against chart visuals
3. Confidence capping: force max 65% in code
4. Low-confidence flagging: <50% marked as unreliable
5. Volatility detection: flag unusual gaps or high volatility
6. Rejection logic: show "Unable to analyze chart" if key extraction fails
7. Disclaimer component: prominent "educational analysis, not financial advice"
8. Disclaimer: "Do not trade based solely on this tool"
9. Test suite: 20+ test cases covering edge cases
10. Error handling: graceful fallback for invalid analyses

## Requirements Mapped
- QUALITY-01: Educational disclaimer
- QUALITY-02: Non-advice disclaimer
- QUALITY-03: Validate all numbers against chart
- QUALITY-04: Reject analyses if extraction fails
- QUALITY-05: Consistency (same chart = same output)
- QUALITY-06: Volatility/gap warning
- REASON-03: Confidence capped at 65%
- REASON-05: Flag confidence <50%

**Duration:** 3-4 days | **Team:** QA Engineer + Backend Engineer

---

*Plan created: 2025-05-19*
