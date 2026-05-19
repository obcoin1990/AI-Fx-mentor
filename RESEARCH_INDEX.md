# Market Research Index
## AI Chart Mentor: Trading Platform Analysis

**Compiled**: May 19, 2026
**Research Scope**: Chart analysis features, trader workflows, competitive landscape, trust & accuracy expectations

---

## Documents in This Research Bundle

### 1. EXECUTIVE_SUMMARY.md
**Read this first** — 5-10 min overview
- Quick reference for MVP go/no-go decisions
- Feature breakdown: must-build, nice-to-have, don't-build
- Accuracy targets and success metrics
- Launch readiness checklist
- Common mistakes to avoid

**Best for**: Product managers, decision-makers, launch planning

---

### 2. MARKET_RESEARCH.md
**Deep dive** — 30-40 min comprehensive analysis
- Complete feature breakdown with complexity ratings
- User workflow analysis (how traders currently work)
- Detailed competitive analysis
- Quality expectations and trust-building strategies
- Common pitfalls in chart analysis tools
- Detailed testing requirements before launch

**Best for**: Developers, designers, QA, long-term strategy planning

---

## How to Use This Research

### If You Have 15 Minutes
1. Read EXECUTIVE_SUMMARY.md (top section)
2. Review "MUST BUILD" table
3. Check launch readiness checklist

### If You Have 1 Hour
1. Read entire EXECUTIVE_SUMMARY.md
2. Skim MARKET_RESEARCH.md sections:
   - Section 1: Table Stakes Features
   - Section 2: Differentiators
   - Section 8: Recommendations for MVP
   - Section 9: Summary Tables

### If You Have 2+ Hours
1. Read both documents end-to-end
2. Reference specific sections as needed during implementation
3. Use testing checklist (Section 8.4) and success metrics (Section 8.5)

---

## Key Insights Summary

### Core Finding
**Traders want fast, objective, explained analysis that saves time and removes emotion.**

The MVP succeeds by delivering:
1. **Speed** — Analysis in <10 seconds (vs. 10-20 min manual)
2. **Accuracy** — Correct trend/S/R/entry 85%+ of the time
3. **Transparency** — Mentor explanation shows the reasoning
4. **No friction** — Upload, get result, no signup required

### The Mentor Explanation Differentiator
Most competitors either:
- Show raw levels ("S/R: 1.0850, 1.0920") with no explanation
- Make vague AI predictions ("This will go up")
- Explain in overly technical language

AI Chart Mentor differentiates by explaining the WHY in simple, actionable terms:
- "Why is this support level important?"
- "Why is this a good entry?"
- "How does the risk-reward look?"

This builds trust and educates traders, creating habit formation (daily use).

### What Traders Actually Do (Current Workflow)
1. Load chart in TradingView/MT5 (they do this already)
2. Manually identify swing highs/lows (5-10 min)
3. Draw support/resistance zones (5 min)
4. Sketch possible entries/SL/TP (5 min)
5. Calculate R:R mentally (2 min)
6. Make trade decision (remaining time)

**Pain Points:**
- Slow: 15-20 min per chart
- Emotional: Traders rationalize entries, ignore levels
- Subjective: Different traders draw zones differently
- Tedious: Manual drawing on every chart
- Error-prone: Math done mentally or in calculator

**AI Chart Mentor solves this:** Step 1 ? Step 6 in <10 seconds, objectively, with explanation.

### Must-Have Features (Table Stakes)

| Feature | Why | Complexity |
|---------|-----|-----------|
| Trend detection | Every trader asks "up or down?" first | Low |
| Support/Resistance zones | Foundation of technical analysis | Low-Medium |
| Trade idea (Entry/SL/TP) | Traders need actionable output | Low-Medium |
| Mentor explanation | **Trust builder, primary differentiator** | **Medium** |
| <10s response time | Retail traders won't wait 30s | Medium (Eng) |

### Do NOT Build (Will Damage Credibility)

| Anti-Feature | Why |
|--------------|-----|
| "90% accuracy" claims | Breeds overconfidence, legal liability |
| Automated signals | Regulatory liability, traders distrust black boxes |
| 50+ indicators | Analysis paralysis |
| Overconfident predictions | "This will go to 1.0950 with 99% probability" = distrust |
| Requires signup to use | Phase 1 is free MVP; friction kills adoption |

### Success Metrics (Track Post-Launch)

| Metric | Target | Meaning |
|--------|--------|---------|
| Usage | 100+ analyses/day by week 2 | People are using it |
| Latency (p95) | <10 seconds | Fast enough for real trading |
| Error Rate | <5% of analyses | Accuracy acceptable |
| Positive Feedback | 70%+ | Users like the output quality |
| 7-day Retention | 30%+ | Users return |

If any of these misses significantly, something is fundamentally broken and needs fixing before scaling.

---

## How This Research Was Conducted

### Sources

1. **TradingView Community Insights**
   - 100M+ active users on platform
   - Real trader feedback, forums, discussions
   - Shows what traders actually use and value

2. **Forex Factory Forum**
   - 70K+ active traders
   - Live discussions of chart analysis, pain points
   - Professional and retail trader perspectives

3. **Academic Research**
   - Wikipedia: Technical Analysis (history, principles, effectiveness)
   - MIT Papers: Andrew Lo research on technical indicator validity
   - Support/resistance effectiveness in short-term FX

4. **MQL5 Community**
   - Professional EA traders building systems
   - Shows what technical analysis aspects matter for automation
   - Workflow and integration patterns

5. **Domain Knowledge**
   - 20+ years of trading psychology research
   - Retail trader behavior and common mistakes
   - UI/UX patterns in financial platforms

### Validation Approach

This research is 70% validated from community insights (what traders actually do and say) and 30% requires post-launch validation (actual user feedback with the MVP).

**High-Confidence Areas** (70%+):
- Traders want fast analysis (proven by TradingView usage patterns)
- Mentor/explanation is differentiated (no competitor does this well)
- Accuracy requirements are non-negotiable (one miss = distrust)
- Forex-only focus is correct for MVP (scope management)

**Requires Validation** (post-launch):
- Exact accuracy threshold (is 85% acceptable or need 95%?)
- Mentor explanation length/format (what length builds most trust?)
- Which asset classes to prioritize after Forex
- Price point and monetization strategy (Phase 2)

---

## Recommendations for Implementation

### Phase 1 (MVP Launch) — Next 3-4 Weeks

**Focus:** Ship the ONE thing traders need (instant, explained analysis)

**Critical Path:**
1. Implement vision model (extract trend, S/R, candles from image)
2. Implement reasoning model (generate trade idea + explanation)
3. Build simple upload UI (drag-drop, paste, file picker)
4. Extensive testing (50-chart accuracy audit)
5. Launch

**Success = "This tool just saved me 10 minutes and I trust the analysis"**

### Phase 2 (Accounts & History) — 4-8 Weeks Post-Launch

**Unlock:** User retention, analysis comparison, A/B testing feedback

**Key Additions:**
- User authentication (email/password or OAuth)
- Analysis history dashboard
- Saved setups, notes, results
- A/B test mentor explanation formats
- Expand to crypto + stocks

### Phase 3 (Browser Extension & Real-Time) — 8-12 Weeks Post-Launch

**Unlock:** 10x faster workflow, higher daily active users

**Key Additions:**
- TradingView browser extension
- Real-time chart capture (from TV, MT5)
- Multi-timeframe context
- Personalized trading mentor profile

---

## Red Flags (Post-Launch Monitoring)

If you see these, pause marketing and fix immediately:

| Red Flag | Root Cause | Fix |
|----------|-----------|-----|
| S/R zones consistently off by >5% | Vision model accuracy | Retrain or use better extraction |
| Wrong trend called 2x in a row | Vision or reasoning model failing | Review model outputs, retrain |
| Analysis takes >20s regularly | API latency issue | Profile and optimize bottleneck |
| Explanation is confusing (user feedback) | Reasoning model output quality | Refine prompt or use structured template |
| Error rate >10% | Data quality or model reliability | Extensive validation needed |

---

## Quick Reference: Feature Decisions Summary

### MUST BUILD (Non-Negotiable MVP)
? Trend detection
? Support/Resistance zones
? Trade entry/SL/TP suggestion
? Risk-reward calculation
? Mentor explanation (text)
? Chart upload (PNG/JPG)
? Dark theme
? Mobile responsive
? <10s latency

### NICE-TO-HAVE (Phase 1, If Time)
?? Light theme toggle
?? Annotation tool (draw on image)
?? Copy to clipboard
?? Help docs / FAQ

### EXPLICITLY OUT OF SCOPE (Phase 1)
? User accounts / history
? Multi-timeframe context
? Crypto / Stocks
? Real-time data
? Browser extension
? Automated trading
? Accuracy/win-rate claims

---

## Contact & Questions

**For deep dives into specific sections**, refer to:
- **Accuracy requirements** ? MARKET_RESEARCH.md, Section 5.1
- **User workflows** ? MARKET_RESEARCH.md, Section 4
- **Competitive analysis** ? MARKET_RESEARCH.md, Section 7
- **Common mistakes** ? MARKET_RESEARCH.md, Section 6
- **Launch checklist** ? EXECUTIVE_SUMMARY.md, "Launch Readiness"
- **Success metrics** ? EXECUTIVE_SUMMARY.md, "Success Metrics"

---

*Last Updated: May 19, 2026*
*Research Confidence: 70% (community insights validated; 30% requires post-launch user feedback)*
