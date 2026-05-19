# Privacy Policy & Legal Notices

## AI Chart Mentor - Privacy Policy

**Effective Date:** 2025-05-19  
**Last Updated:** 2025-05-19

---

## 1. Introduction

AI Chart Mentor ("we," "us," "the Company") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and protect your data when you use our platform.

**Key Principle:** We collect minimal data and discard chart images immediately after analysis.

---

## 2. What Data We Collect

### Data You Provide
- **Chart Images**: Uploaded PNG/JPG files
- **Pair & Timeframe**: Optional metadata (EUR/USD, 4H, etc.)
- **Your Feedback**: When you submit bug reports or suggestions

### Data We Automatically Collect
- **IP Address**: For rate limiting and security
- **Device Info**: Browser type, OS (for analytics)
- **Performance Metrics**: Response times, cache hits
- **Error Logs**: Failed analyses, API errors

### Data We Do NOT Collect
- ❌ User accounts or profiles (Phase 1)
- ❌ Personally identifiable information (PII)
- ❌ Trading history or financial data
- ❌ Cookies or persistent identifiers
- ❌ Location data
- ❌ Payment information (Phase 1)

---

## 3. How We Use Your Data

### Chart Images
**We analyze your chart image ONLY to:**
1. Extract trend, zones, patterns using Claude Vision API
2. Return analysis JSON to you
3. **Then immediately discard the image** (not stored)

**The image is:**
- Sent directly to Claude API via Anthropic's servers
- Never stored in our database
- Not shared with third parties
- Not used for training or retraining models

### Analysis Results (JSON)
**We store only the analysis output:**
- Trend direction (bullish/bearish/consolidating)
- Support/resistance zones and confidence
- Trade scenarios
- Mentor explanation
- Confidence score
- Timestamp and analysis ID

**Retention:** 30 days, then automatically deleted

**Use:** Audit logging, performance metrics, quality improvement

### Performance Metrics
**We collect:**
- Response time (vision API, reasoning API, total)
- Cache hit/miss counts
- Error types and frequencies
- Active user count

**Use:** Infrastructure monitoring, SLA tracking, capacity planning

### Error Logs
**We log:**
- API failures (Claude Vision timeout, etc.)
- Image validation errors
- Chart format issues
- Response codes

**Use:** Debugging, alerting, improving reliability

---

## 4. Data Retention

| Data Type | Retention | Reason |
|-----------|-----------|--------|
| Chart Images | Immediate deletion | Privacy-first policy |
| Analysis JSON | 30 days | Audit log, quality review |
| Error Logs | 30 days | Debugging, monitoring |
| Performance Metrics | 90 days | Trend analysis |
| IP Addresses | 7 days | Rate limiting, security |

All data is automatically deleted after retention period via scheduled jobs.

---

## 5. Data Security

### Encryption
- **In Transit:** TLS 1.3 (HTTPS)
- **At Rest:** PostgreSQL encryption at the database level
- **Redis Cache:** Configured for security (no persistence of sensitive data)

### Access Controls
- Minimal team access to logs
- No access to raw analysis data without approval
- API keys and secrets managed via environment variables
- Database backups encrypted

### Compliance
- No GDPR data (Phase 1 stateless, no PII)
- SOC 2 compliance roadmap (Phase 2)
- Regular security audits planned
- Incident response plan documented

---

## 6. Third-Party Services

### Claude API (Anthropic)
- **Purpose:** Vision analysis, reasoning
- **Data:** Your chart image, analysis request
- **Retention:** Anthropic's API terms (typically 30 days)
- **Privacy:** https://www.anthropic.com/privacy

### Supabase (PostgreSQL + Storage)
- **Purpose:** Database and audit logs
- **Data:** Analysis results (no images)
- **Retention:** 30 days auto-delete
- **Privacy:** https://supabase.com/privacy

### Vercel (Frontend Hosting)
- **Purpose:** Frontend deployment
- **Data:** Static assets, no personal data
- **Privacy:** https://vercel.com/legal/privacy-policy

### Railway (Backend Hosting)
- **Purpose:** Backend deployment
- **Data:** API server logs
- **Retention:** 30 days
- **Privacy:** https://railway.app/legal

### Redis Cloud (Caching)
- **Purpose:** 48-hour image hash cache
- **Data:** Analysis JSON only (no images)
- **Privacy:** https://redis.com/legal/privacy-policy

### Sentry (Error Tracking)
- **Purpose:** Error monitoring and alerting
- **Data:** Error messages, stack traces
- **Retention:** 90 days
- **Privacy:** https://sentry.io/privacy/

---

## 7. Your Rights

### You Have the Right To:
- Know what data we collect about you
- Request deletion of your data (within 30-day retention)
- Understand how we use your data
- Opt-out of analytics tracking

### How to Exercise Your Rights
Email: privacy@aichartmentor.com (contact TBD)

We will respond within 30 days.

---

## 8. Data Breach Notification

If we experience a data breach:
1. We will investigate within 48 hours
2. Notify affected users within 72 hours
3. Describe the breach and steps taken
4. Provide recommendations for protection

---

## 9. Changes to Privacy Policy

We may update this policy as our services evolve. Changes will be:
- Posted on this page with updated date
- Sent to users via email (if you have an account in Phase 2)
- Effective 30 days after posting

---

## 10. Contact

**Questions about your privacy?**

Email: privacy@aichartmentor.com (pending setup)

---

---

# Terms of Service

## AI Chart Mentor - Terms of Service

**Effective Date:** 2025-05-19

---

## 1. Acceptance of Terms

By using AI Chart Mentor, you agree to these Terms of Service. If you do not agree, do not use the service.

---

## 2. Educational Disclaimers

### ⚠️ NOT Financial Advice
This tool provides **educational analysis only**. It does **NOT constitute financial advice**, investment recommendations, or trading signals.

**You should NOT:**
- Trade based solely on this tool's output
- Assume any analysis guarantees profits
- Trust the tool without independent verification
- Use this tool with money you cannot afford to lose

**You MUST:**
- Conduct your own research
- Consult a licensed financial advisor
- Use proper risk management
- Only trade what you can afford to lose

### Confidence Cap at 65%
- All confidence scores are capped at maximum 65%
- This prevents overconfidence bias
- Even 65% confidence is not "high confidence"
- No analysis should be treated as highly reliable

### Past Performance ≠ Future Results
- Chart patterns observed in the past may not repeat
- Market conditions change constantly
- This tool has no guarantee of effectiveness
- Your results may differ significantly from others

---

## 3. Liability Waiver

**THE SERVICE IS PROVIDED "AS IS" WITHOUT WARRANTIES.**

We specifically disclaim:
- Merchantability or fitness for a particular purpose
- Accuracy or completeness of analysis
- Suitability for your trading strategy
- Freedom from errors or omissions

### Limitation of Liability

To the fullest extent permitted by law:
- We are not liable for any trading losses
- We are not liable for any errors in analysis
- We are not liable for missed opportunities
- We are not liable for technical failures

**You assume 100% of the risk** when you use this tool.

---

## 4. Acceptable Use

You agree NOT to:
- Use the tool for automated trading without human review
- Share login credentials (future Phase 2 feature)
- Attempt to breach security
- Scrape or download analysis data at scale
- Use the tool for unlicensed financial advice
- Upload copyrighted chart images without permission

Violations may result in service termination.

---

## 5. Intellectual Property

- **Our IP:** Claude Vision API integration, analysis algorithms, UI design
- **Your IP:** Chart images you upload belong to you
- **No License Transfer:** Using our tool doesn't grant you rights to our code

---

## 6. Stateless MVP (Phase 1)

In Phase 1:
- We do NOT store your trading history
- We do NOT track your performance
- We do NOT save your preferences
- Each analysis is independent

---

## 7. Forex Only (Phase 1)

This tool is designed for **forex pairs only** (EUR/USD, GBP/USD, etc.).

- **Not recommended for:** Crypto, stocks, commodities, indices
- **Future:** Phase 2 may expand to other instruments
- **Quality:** Analysis may be inaccurate for non-forex

---

## 8. Limitations

### Technical Limitations
- Vision API can fail or timeout (>10 seconds)
- Chart patterns may not be detected in unusual markets
- Unusual volatility may cause unreliable analysis
- Mobile image quality may affect results

### Market Limitations
- Works best for trending markets
- May fail in choppy/ranging markets
- May miss key levels in gap-prone charts
- Does not account for news/events

---

## 9. Service Interruptions

We will:
- Use reasonable efforts to keep the service available
- Schedule maintenance and communicate in advance
- Have backups and disaster recovery plans
- Monitor 24/7 and respond to issues quickly

We will NOT:
- Provide refunds for downtime (service is free Phase 1)
- Guarantee 100% uptime (no SLA Phase 1)
- Compensate for trading losses during outages

---

## 10. Third-Party Services

This tool uses Claude API (Anthropic). We are not responsible for:
- Anthropic's service quality
- Changes to Claude's capabilities
- Anthropic's data practices (see their privacy policy)

---

## 11. Termination

We reserve the right to terminate or suspend your access if:
- You violate these terms
- You use the tool for unlicensed financial advice
- You attempt to breach security
- Legal requirements demand termination

---

## 12. Dispute Resolution

### Informal Resolution
Contact us with your concern: privacy@aichartmentor.com (pending setup)
We will attempt to resolve within 30 days.

### Arbitration
If informal resolution fails, disputes will be resolved through binding arbitration under [jurisdiction - TBD], not litigation.

---

## 13. Changes to Terms

We may update these terms. Changes are:
- Effective immediately upon posting
- Applied to new usage only (not retroactively)
- Notified to users if significant (Phase 2+)

---

## 14. Governing Law

These terms are governed by [jurisdiction - TBD] law.

---

## 15. Entire Agreement

These Terms, plus Privacy Policy, plus any other notices, constitute the entire agreement between you and us.

---

## 16. Contact

**Questions about these terms?**

Email: legal@aichartmentor.com (pending setup)

---

---

# Summary: Key Legal Points for Traders

## ✓ You Should Know

1. **NOT Financial Advice** — This tool is educational, not a recommendation to trade
2. **No Guarantees** — Past patterns don't guarantee future profits
3. **Risk Management** — Only trade what you can afford to lose
4. **65% Cap** — Highest confidence is 65%, prevents overconfidence
5. **Do Your Own Research** — Use multiple sources, don't rely on this tool alone
6. **No Trading History** — Phase 1 doesn't save your trades or performance
7. **Free Service Phase 1** — No refunds for downtime, best effort only
8. **Privacy First** — Your chart image is discarded immediately, only analysis saved

## ❌ You Must NOT

- Trade based solely on this tool's output
- Assume any confidence score means "high confidence"
- Use money you can't afford to lose
- Use this tool without proper risk management
- Trade the live market based on the first setup
- Leverage this tool without independent verification

## ✓ You MUST DO

- Confirm entry/SL/TP prices visually on your chart
- Use proper position sizing
- Set stop-losses at appropriate levels
- Think independently about your trades
- Keep trading journal and review results
- Consult a licensed financial advisor if needed

---

**By using AI Chart Mentor, you acknowledge you have read, understood, and agree to these terms.**

*Last updated: 2025-05-19*
