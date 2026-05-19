# MVP Implementation Guidance
## Actionable Steps & AI Prompts for Building AI Chart Mentor

**Purpose:** Bridge research findings to actual implementation
**Audience:** Developers, prompt engineers, QA teams

---

## PART 1: VISION MODEL REQUIREMENTS

### What the Vision Model Must Extract

The vision model (Claude 3.5 Sonnet Vision) receives a chart image and outputs structured JSON.

**Required Outputs:**

`json
{
  "trend": {
    "direction": "bullish|bearish|range",
    "confidence": 0.85,
    "basis": "string describing why (e.g., 'higher highs/lows', 'price above 200 EMA')"
  },
  "support_resistance": {
    "support_zones": [
      {"level": 1.0850, "strength": "strong", "notes": "swing low from 3 days ago"},
      {"level": 1.0800, "strength": "medium", "notes": "previous support"}
    ],
    "resistance_zones": [
      {"level": 1.0920, "strength": "strong", "notes": "failed breakout yesterday"},
      {"level": 1.0950, "strength": "medium", "notes": "prior swing high"}
    ]
  },
  "candle_structure": {
    "current_candle": {"open": 1.0880, "high": 1.0910, "low": 1.0870, "close": 1.0905},
    "candle_type": "bullish|bearish|doji|hammer",
    "wick_analysis": "string describing upper/lower wicks"
  },
  "potential_entry_zones": [
    {"price": 1.0900, "type": "bounce_off_support", "probability": 0.65},
    {"price": 1.0920, "type": "breakout", "probability": 0.45}
  ],
  "error_notes": "null|string if chart is unclear or ambiguous"
}
`

**Vision Model Prompt Template:**

`
You are a professional forex chart analyzer. Analyze this trading chart and extract the following:

1. TREND: Identify if price is in an uptrend (higher highs/lows), downtrend (lower highs/lows), or ranging sideways. Basis: look for EMA alignment, swing pattern, recent price action.

2. SUPPORT & RESISTANCE: Find the 2-3 most significant support zones and 2-3 most significant resistance zones. Define them as zones (not single prices), based on swing highs/lows and prior price action. Include strength rating (strong = tested multiple times, medium = 1-2 tests, weak = only mentioned once).

3. CANDLE STRUCTURE: Describe the most recent candle(s). Is it bullish, bearish, a hammer, a doji? What do the wicks tell you?

4. ENTRY ZONES: Based on support/resistance, what are 1-2 likely entry zones where traders might take action?

5. DATA QUALITY: Is the chart clear enough to analyze, or is it ambiguous/unclear?

Return ONLY valid JSON. Do NOT include markdown formatting, code blocks, or any text outside the JSON.
`

**Key Validation:**
- Candle data must be parseable (valid OHLC numbers)
- Support/resistance zones must align with visible swing points (±2% tolerance)
- Trend must match visual price action (higher highs = uptrend, etc.)
- If chart is ambiguous, return "error_notes" describing the issue

---

## PART 2: REASONING MODEL REQUIREMENTS

### What the Reasoning Model Must Generate

The reasoning model receives JSON from vision model and generates:
1. Trade idea (entry, stop loss, take profit, calculated R:R)
2. Mentor explanation (2-3 sentences explaining the setup and reasoning)

**Required Output:**

`json
{
  "trade_idea": {
    "direction": "long|short",
    "entry_zone": "1.0900-1.0910",
    "stop_loss": 1.0870,
    "take_profit": 1.0950,
    "risk_reward_ratio": 2.5,
    "rationale": "string explaining why this setup"
  },
  "mentor_explanation": {
    "setup_summary": "string (1-2 sentences) describing the setup",
    "key_levels": "string (1-2 sentences) explaining why entry/SL/TP levels matter",
    "risk_management": "string (1 sentence) about the risk-reward and position sizing hint",
    "caveat": "string (1 sentence) about what could go wrong or conditions to watch"
  }
}
`

**Reasoning Model Prompt Template:**

`
You are a forex trading mentor analyzing a chart setup. Based on this extracted chart data:

[INSERT VISION MODEL JSON HERE]

Generate a trade idea and mentor explanation following these rules:

TRADE IDEA:
- Direction: Choose LONG or SHORT based on trend and entry zone
- Entry Zone: Give a 10-20 pip range (not a single price). Should be at support (long) or resistance (short)
- Stop Loss: Place below entry zone for longs, above for shorts. Should be near next support/resistance level or beyond swing point
- Take Profit: Place at next significant resistance (long) or support (short). Should be 1.5x or more risk-reward
- Risk-Reward: Calculate as (TP - Entry) / (Entry - SL). This is simple math; must be accurate

MENTOR EXPLANATION:
- Setup Summary: Explain the trend, key level, and why now is a good time to trade (1-2 sentences)
- Key Levels: Explain why entry/SL/TP placement makes sense (1-2 sentences)
- Risk Management: Comment on the R:R ratio and when to size position (1 sentence)
- Caveat: What could go wrong? What conditions could invalidate this setup? (1 sentence)

Tone: Professional, educational, confident but not overconfident. Use "likely," "suggests," "if" rather than "will," "guaranteed."

Return ONLY valid JSON. No markdown, no code blocks.
`

**Key Validation:**
- Risk-reward calculation must be exact (math check: (TP-Entry)/(Entry-SL))
- Entry zone must be at support (long) or resistance (short)
- Stop loss must be beyond the zone (not within it)
- Take profit must be next significant level (not arbitrary distance)
- Explanation must be 150-300 words total (concise, scannable)
- No overly technical language (teach a beginner, not an academic)

---

## PART 3: QUALITY ASSURANCE CHECKLIST

### Pre-Launch Accuracy Testing (Must Complete)

**Test Dataset:** 50 real EUR/USD, GBP/USD, USD/JPY charts (mix of timeframes: M5, M15, H1, H4)

**For Each Chart, Verify:**

`
Trend Detection:
? Trend direction matches visual (higher highs = bullish, etc.)
? Confidence score is reasonable (0.6-0.95)
? Basis explanation is accurate (references actual price action)

Support/Resistance:
? Levels align with swing highs/lows (within ±2%)
? At least 2-3 zones identified per direction
? Strength ratings are accurate (strong = tested multiple times)
? No "hallucinated" levels (every level must be visible on chart)

Entry/SL/TP:
? Entry is at support (long) or resistance (short)
? Stop loss is beyond the zone (not tight/arbitrary)
? Take profit is at next significant level (not guessed)
? Risk-reward is calculated correctly (math verification)
? Setup is viable (trader would actually take this trade)

Mentor Explanation:
? Summary clearly explains why the setup is valid
? References specific levels (not vague: "near support" ? "1.0850")
? Tone is confident but not overconfident
? Language is clear (beginner can understand)
? No overly technical jargon
? 150-300 words (scannable, not a wall of text)

Data Quality:
? JSON is valid (no syntax errors)
? Numbers are reasonable (no decimal places missing, realistic values)
? No null fields where data is required
`

**Success Criteria:**
- 85%+ of S/R zones accurate (visible on chart at ±2%)
- 90%+ of trend calls correct (visual confirmation)
- 80%+ of entry/SL/TP viable (trader would take setup)
- 80%+ of explanations clear (3 traders independently say "I understand the reasoning")

**If Accuracy < Targets:**
- For S/R: Review vision model extraction; may need fine-tuning
- For Trend: Check EMA-based vs. swing-based trend definition; align on standard
- For Entry/SL/TP: Check reasoning prompt; may need more specific guidelines
- For Explanation: Collect trader feedback and iterate on prompt

---

## PART 4: PERFORMANCE & LATENCY TARGETS

### API Response Time Budget

`
Vision Model Processing: <5 seconds (p95)
Reasoning Model Processing: <3 seconds (p95)
Image Upload/Download: <1 second (p95)
Database/Response: <1 second (p95)
---
Total End-to-End: <10 seconds (p95)
`

**Optimization Tips:**

1. **Parallel Processing:** Call vision and reasoning models in sequence (not parallel; reasoning depends on vision output)
2. **Caching:** Cache common S/R zones if same instrument/timeframe is analyzed multiple times (trade-off: freshness vs. speed)
3. **Image Compression:** Resize large images (>2MB) before sending to vision model (saves API time)
4. **Error Handling:** If vision model times out, return degraded response (trend only, no S/R) rather than failing completely

**Monitor These Metrics:**
- Vision model latency (aim: <5s)
- Reasoning model latency (aim: <3s)
- End-to-end latency (aim: <10s p95)
- Error rate (aim: <1% API failures)
- Hallucination rate (aim: 0%; verify in QA)

---

## PART 5: COMMON ISSUES & FIXES

### Issue: S/R Zones Hallucinated (Don't Exist on Chart)

**Cause:** Vision model generating levels from training data, not visible chart

**Fix:**
1. Add constraint to vision prompt: "Only identify levels you can see on the chart"
2. Validate each S/R level against recent highs/lows (programmatic check)
3. If validation fails, remove the level from output

---

### Issue: Explanation is Too Technical

**Cause:** Reasoning model using technical jargon ("bullish engulfing," "confluence," "order flow")

**Fix:**
1. Add tone instruction: "Explain like you're teaching a friend, not a PhD student"
2. Provide examples of good explanations (in-context learning)
3. Simplify vocabulary in prompt: Use "buy zone" instead of "confluent demand zone"

---

### Issue: Risk-Reward Calculated Incorrectly

**Cause:** Reasoning model doing math wrong (shouldn't happen, but LLMs struggle with math)

**Fix:**
1. Make R:R a deterministic calculation, not LLM-generated
2. Pass calculated R:R into reasoning model (from vision model)
3. Add validation: if R:R < 1.0, flag as error (trades must be at least break-even)

---

### Issue: Entry Zone Too Tight (10 pip range vs. 20 pip)

**Cause:** Vision model confusing entry zone with exact price level

**Fix:**
1. Specify in prompt: "Entry zone should be 15-30 pips wide, accommodating wicks and noise"
2. Programmatically expand tight zones: if <10 pips, expand to ±10 from center
3. Validate: Entry zone should span at least 1-2 candle bodies

---

### Issue: Mentor Explanation Doesn't Match Entry/SL/TP

**Cause:** Vision and reasoning models not aligned; explanation references levels not in the trade idea

**Fix:**
1. Make reasoning model reference specific prices from trade idea
2. Add validation: Check that explanation mentions entry, SL, TP price levels
3. If mismatch, re-run reasoning with explicit price list in prompt

---

## PART 6: TESTING CHECKLIST (Before Launch)

### Week 1: Accuracy Validation

- [ ] Vision model: 50-chart accuracy test (S/R, trend, candle structure)
- [ ] Reasoning model: 50-chart viability test (entry/SL/TP, R:R calc, explanation)
- [ ] Combined: 10 traders review 10 charts each, give feedback on clarity and accuracy
- [ ] Error handling: Test with blurry, zoomed-in, zoomed-out charts (edge cases)
- [ ] Data validation: Ensure all JSON outputs are valid, no null fields

### Week 2: Performance & Scale

- [ ] Latency: Measure p95 time-to-result across 100 requests
- [ ] Uptime: Run for 48 hours continuous; capture any timeouts/errors
- [ ] Concurrency: Test with 10 simultaneous requests (API rate limits)
- [ ] Image handling: Test with PNG, JPG, various sizes (100KB - 5MB)
- [ ] Mobile: Responsive design on iPhone 12, Samsung Galaxy S21

### Week 3: UX & Usability

- [ ] Upload: 5 traders test drag-drop, paste, file upload. All should work seamlessly
- [ ] Reading results: 5 traders can read and understand analysis in <30 sec
- [ ] Mobile usability: iPhone/Android; can scroll, read, interpret
- [ ] Dark theme: Eye comfort during extended use
- [ ] Error messages: Clear, actionable messages (not technical jargon)

### Week 4: Cross-Browser & Broker Compatibility

- [ ] Desktop browsers: Chrome, Firefox, Safari (latest versions)
- [ ] Mobile browsers: Safari iOS, Chrome Android
- [ ] Chart sources: Upload from TradingView, MT5, cTrader, broker platforms
- [ ] Timeframes: M5, M15, M30, H1, H4, D1 (test at least 5)
- [ ] Instruments: EUR/USD, GBP/USD, USD/JPY, AUD/USD (at least 4)

### Success Criteria for Launch

All of the following must be TRUE:

- ? 85%+ accuracy on S/R zones (50-chart test)
- ? 90%+ accuracy on trend (50-chart test)
- ? 80%+ clarity on explanations (trader feedback)
- ? <10 second p95 latency (100-request test)
- ? <1% error rate (48-hour uptime test)
- ? All 5 traders can upload & read results in <2 min (usability test)
- ? Works on mobile (responsive, readable)
- ? Works across 5+ browsers/platforms

If ANY criteria fails ? do not launch. Fix, retest, then launch.

---

## PART 7: LAUNCH DAY

### 24 Hours Before

- [ ] Final accuracy audit: 10-chart spot check
- [ ] Latency check: Run 10 consecutive requests
- [ ] Backup & failover: Ensure monitoring and rollback plan ready
- [ ] Support plan: Who responds to issues? Response time? (Aim: <30 min for critical issues)

### Launch Hour

- [ ] Monitor error rate, latency, concurrency in real-time
- [ ] Check user feedback (Discord, Twitter, email)
- [ ] Be ready to rollback if error rate > 5%

### Week 1 Post-Launch

Track these daily:
- Usage: Analyses per day
- Latency: p50, p95, p99 (should be <10s p95)
- Error rate: % of requests failing
- User feedback: Thumbs up/down, comments
- Support tickets: Issues reported

**Threshold for Action:**
- If usage < 50/day ? low adoption; check marketing/word-of-mouth
- If latency > 20s p95 ? performance issue; investigate bottleneck
- If error rate > 5% ? production issue; consider rollback
- If feedback < 50% positive ? quality issue; prioritize improvements

---

## PART 8: POST-LAUNCH ITERATION (Weeks 2-4)

### Based on Early Feedback

**If S/R Accuracy < 85%:**
- Review vision model output on failed cases
- Adjust extraction thresholds (e.g., "swing point must be tested twice")
- Retrain or fine-tune if systematic bias

**If Explanations Are Confusing (< 70% positive feedback):**
- Collect 5-10 specific examples of confusing explanations
- Refine reasoning prompt with clearer language
- A/B test 2-3 different explanation styles
- Pick the one that gets 80%+ clarity

**If Latency Creeping Up (>12s):**
- Profile API calls; identify slowest component
- Optimize image compression, API calls, or add caching
- Consider switching models if current model too slow

**If Specific Instruments Fail (e.g., GBP/USD wrong S/R):**
- Audit those charts separately
- May be broker data differences (pip sizes, decimals)
- Add broker-specific calibration if needed

### Metrics to Track for Phase 2 Roadmap

- Which asset classes users request (crypto, stocks?)
- What additional features users mention (history, annotations?)
- How often same user returns (daily, weekly, once-and-done?)
- Which timeframes are most popular (M15, H1, D1?)

---

## Final Notes

This guidance is designed to translate research findings into concrete implementation. The key insight is:

**Traders will adopt AI Chart Mentor if:**
1. It's faster than manual analysis
2. It's at least 85% accurate
3. It explains why clearly
4. It works instantly (no signup, <10s analysis)

Everything else is secondary. Focus on nailing these four things in the MVP, then iterate based on real user feedback.

Good luck! 

---

*End of Implementation Guidance*
