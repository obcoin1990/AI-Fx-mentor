# AI Analysis Workflow

1. User uploads chart screenshot.
2. Backend receives image via API route.
3. Vision model extracts:
   - Candles
   - Highs/lows
   - Trend
   - Key levels
4. Reasoning model converts extracted data into:
   - Trade ideas
   - Mentor explanation
5. Response returned to frontend:
   - JSON with levels, ideas, text
   - (Optional) annotated image
