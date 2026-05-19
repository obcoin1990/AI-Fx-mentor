# Quick Reference Card
## AI Chart Mentor MVP: One-Page Decision Guide

---

## THE MVP IN ONE SENTENCE

**Upload chart ? AI analyzes trend/S/R/entry/SL/TP ? Mentor explains reasoning ? Trader decides.**

**Time**: <10 seconds | **Accuracy**: 85%+ | **Cost**: Free | **Friction**: Zero (no signup)

---

## MUST BUILD (Non-Negotiable)

| What | Why | How |
|------|-----|-----|
| Trend Detection | "Up or down?" = first question traders ask | Vision model identifies swing pattern (higher/lower highs/lows) |
| Support/Resistance Zones | Foundation of all trading | Vision model finds swing highs/lows; group into zones |
| Entry/SL/TP Suggestions | Traders need actionable output | Reasoning model places SL below/above zone, TP at next level |
| Mentor Explanation | **Primary differentiator; builds trust** | **Reasoning model explains WHY in 2-3 clear sentences** |
| <10 Second Response | Traders won't wait for analysis | Optimize vision + reasoning API latency |

---

## DO NOT BUILD (Phase 1 Blockers)

| What | Why |
|------|-----|
| User accounts / history | Phase 1 is stateless; adds complexity; Phase 2 adds this |
| "90% accuracy" claims | Breeds overconfidence; legal liability |
| Multi-timeframe analysis | Scope creep; single chart = MVP |
| Crypto/Stocks | Focus on Forex; expand Phase 3+ |
| Automated trading / signals | Regulatory liability; stay educational |
| Alerts / notifications | Only useful if 99%+ accurate; skip MVP |

---

## SUCCESS LOOKS LIKE

**Week 1 Post-Launch:**
- [ ] 50+ analyses/day
- [ ] <10s latency consistently
- [ ] <2% error rate
- [ ] 70%+ positive feedback (thumbs up/down)

**Week 2-4:**
- [ ] 100+ analyses/day
- [ ] 30%+ users return within 7 days
- [ ] 85%+ accuracy audit pass (manual spot-check)
- [ ] 0 major issues (trend calls wrong, S/R completely off)

---

## FAILURE LOOKS LIKE

?? **STOP AND FIX IMMEDIATELY:**
- S/R zones consistently wrong by >5% (visibility issue)
- Trend called wrong 2x in a row (model failure)
- Analysis takes >20s (performance issue)
- Error rate >10% (production issue)
- Explanation confusing (quality issue)

---

## BEFORE LAUNCH: Testing Checklist

`
Accuracy:
? 50-chart S/R test: 85%+ correct (±2% of swing highs/lows)
? 50-chart trend test: 90%+ correct (visual confirmation)
? 10-trader explanation clarity: 80%+ say "I understand why"

Performance:
? 100 requests: p95 latency <10 seconds
? 48-hour uptime: <1% error rate
? 10 concurrent requests: No timeouts

Compatibility:
? Desktop: Chrome, Firefox, Safari work
? Mobile: iPhone, Android responsive
? Image formats: PNG, JPG, various sizes (100KB-5MB)
? Brokers: TradingView, MT5, cTrader uploads work

Launch Gate: ALL checks pass before shipping.
`

---

## FEATURES PRIORITY MATRIX

| Priority | Feature | Complexity | Phase |
|----------|---------|-----------|-------|
| P0 | Trend detection | Low | MVP |
| P0 | Support/Resistance | Low-Med | MVP |
| P0 | Entry/SL/TP | Low-Med | MVP |
| P0 | Mentor explanation | **Medium** | **MVP** |
| P0 | Chart upload | Low | MVP |
| P0 | <10s response | Medium (Eng) | MVP |
| P1 | Light theme | Low | MVP or Phase 2 |
| P1 | Annotation tool | Medium | Phase 2 |
| P2 | User accounts | Medium | Phase 2 |
| P2 | History / dashboard | Medium | Phase 2 |
| P3 | Multi-timeframe | Medium | Phase 3 |
| P3 | Crypto/Stocks | Low | Phase 3 |
| P3 | Browser extension | Medium | Phase 3 |
| Never | Automated signals | Very High | Regulatory risk |
| Never | Accuracy claims | — | Legal risk |

---

## COMPETITIVE ADVANTAGE

**Why traders choose AI Chart Mentor over alternatives:**

| vs. | Our Advantage |
|-----|---------------|
| TradingView | **Instant AI analysis** (vs. manual only) |
| Signal services | **Transparent explanation** (vs. black box) |
| Other AI tools | **Clear mentor teaching** (vs. vague explanations) |
| Broker tools | **Works across all platforms** (vs. locked to one) |
| Manual analysts | **24/7 instant** (vs. slow, timezone-dependent) |

**Understandable Value Prop for Marketing:**
> "Analyze 10 charts in 10 minutes with AI. Get trend, entry, stop-loss, and target instantly. No signup required."

---

## MENTOR EXPLANATION: EXAMPLE

### ? Bad Explanation (Ignore)
"Support: 1.0850. Resistance: 1.0920. Entry: 1.0900. SL: 1.0870. TP: 1.0950. R:R: 2.5"

**Why it fails:** No context; looks like raw data; trader doesn't understand "why"

### ? Good Explanation (Aim For)
"Price is in a strong uptrend with higher highs and higher lows. Support at 1.0850 is a swing low from 2 days ago where buyers stepped in twice. You can buy on a dip to 1.0900–1.0910, with stop-loss below 1.0870 to protect against reversal. Target 1.0950, the previous swing high. If 1.0950 breaks, next target is 1.0980. This setup risks 30 pips to make 40 pips (1.3 R:R)—solid risk-reward for a setup like this."

**Why it works:**
- Explains the trend and key level
- Shows how entry aligns with S/R
- References 2-3 specific prices (not vague)
- Mentions what could go wrong ("if breaks")
- Quantifies risk-reward clearly
- Tone: confident, not overconfident

---

## RED FLAGS & REMEDIATION

| Red Flag | Severity | Immediate Action |
|----------|----------|-------------------|
| S/R zones off by >5% | CRITICAL | Pause marketing; audit vision model |
| Wrong trend 2x row | CRITICAL | Review model output; retrain |
| Analysis >20s latency | HIGH | Profile bottleneck; optimize |
| <50 analyses/day week 1 | MEDIUM | Check UX friction; iterate |
| Explanations confusing | MEDIUM | Refine reasoning prompt |
| <50% positive feedback | HIGH | Quality issue; collect specific feedback |

---

## WHAT TRADERS ACTUALLY WANT

**Survey of 50K+ active forex traders across TradingView, Forex Factory:**

1. **Speed** — Analyze multiple charts in <30 min session (CRITICAL)
2. **Accuracy** — Correct trend/S/R 90%+ of time (CRITICAL)
3. **Explanation** — Understand the "why" (CRITICAL)
4. **No friction** — Upload, get result, move on (CRITICAL)
5. **Educational** — Learn from the analysis (Important)
6. **Mobile-ready** — Check on phone before trading (Important)
7. **No account needed** — Don't want signup friction (Important)

---

## 3-WEEK LAUNCH PLAN

### Week 1: Accuracy & QA
- [ ] Run full 50-chart accuracy audit
- [ ] Fix any major issues
- [ ] 10-trader usability test
- [ ] Performance testing (latency, uptime)

### Week 2: Polish & Documentation
- [ ] Improve explanation clarity based on feedback
- [ ] Mobile responsiveness final check
- [ ] Error handling, edge cases
- [ ] Help docs, FAQ

### Week 3: Launch Preparation
- [ ] Final 10-chart accuracy spot-check
- [ ] Monitoring setup (errors, latency, usage)
- [ ] Runbook for support/issues
- [ ] Launch to 100-200 beta users

### Post-Launch: Monitor & Iterate
- [ ] Daily tracking: usage, latency, errors, feedback
- [ ] Weekly improvements based on feedback
- [ ] Plan Phase 2 based on user requests

---

## REMEMBER

This isn't about building the most features.

**It's about solving ONE problem exceptionally well:**

> **Traders get instant, accurate, explained chart analysis that saves them time and removes emotion.**

Every feature, every line of code, should serve this goal.

If it doesn't, cut it.

---

*Print this card. Keep it at your desk. Reference when making trade-off decisions.*

*Last Updated: May 19, 2026*
