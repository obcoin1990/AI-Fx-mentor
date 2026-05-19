---
wave: 2
depends_on:
  - 02-PLAN-foundation.md
  - 03-PLAN-frontend-ui.md
files_modified:
  - backend/routes/analyze.py
  - backend/services/vision.py
  - backend/services/image_processor.py
  - backend/utils/prompts.py
  - backend/schemas/vision.py
  - backend/main.py
autonomous: true
---

# Plan 3: Vision API & Image Processing
**Objective:** Implement Claude Vision API endpoint in FastAPI. Extract trend, swing highs/lows, support/resistance zones, chart patterns from uploaded images into structured JSON.

## What We're Building
FastAPI POST /api/analyze-chart endpoint that accepts multipart/form-data with image file, validates image, calls Claude 3.5 Sonnet Vision API with structured prompt, parses response into validated JSON with trend, support zones, resistance zones, chart patterns. Validate extracted prices against chart to prevent hallucinations.

## Must-Haves
1. POST /api/analyze-chart endpoint (multipart/form-data)
2. Image file validation (format, size, dimensions)
3. Claude Vision API integration with structured prompt
4. Extract: trend (bullish/bearish/consolidating)
5. Extract: swing highs and lows
6. Extract: support zones (with # of touches)
7. Extract: resistance zones (with # of touches)
8. Extract: chart patterns (double top/bottom, channels, triangles, flags, H&S)
9. Validate extracted prices match chart data
10. Return structured JSON response
11. Log analysis to audit_logs table
12. Error handling: image validation, API timeouts, parsing failures

## Requirements Mapped
- VISION-01: Extract trend direction
- VISION-02: Identify swing highs and lows
- VISION-03: Extract support zones
- VISION-04: Extract resistance zones
- VISION-05: Detect chart patterns
- VISION-06: Return structured JSON
- QUALITY-03: Validate prices against chart (no hallucinations)
- PERF-03: Log analyses for audit trail

**Duration:** 4-5 days | **Team:** Backend Engineer + AI Engineer

---

*Plan created: 2025-05-19*
