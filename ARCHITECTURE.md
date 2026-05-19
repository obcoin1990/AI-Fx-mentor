# AI Chart Mentor: Component Architecture & Data Flow

## SECTION 1: COMPONENT ARCHITECTURE

### Phase 1 (MVP) - Component Boundaries

```
+-------------------------------------------------------------+
¦                        FRONTEND                             ¦
¦  (Next.js App Router - client components + server actions)  ¦
¦  - Chart upload UI                                          ¦
¦  - Result display (trend, S/R, trade idea)                  ¦
¦  - Mentor explanation display                               ¦
¦  - Loading states & error handling                          ¦
+-------------------------------------------------------------+
         ¦ multipart/form-data (file)
         ?
+-------------------------------------------------------------+
¦               API ROUTE: /api/analyze-chart                 ¦
¦         (Next.js API Route - route handler)                 ¦
¦                                                             ¦
¦  1. Image validation (size, format, dimensions)             ¦
¦  2. Image preprocessing (optional: crop, rotate, enhance)  ¦
¦  3. Call Vision Extraction Service                          ¦
¦  4. Validate extracted JSON schema                          ¦
¦  5. Call Reasoning Service                                 ¦
¦  6. Format & return response                                ¦
¦  7. Error handling & fallback logic                         ¦
+-------------------------------------------------------------+
     ¦                        ¦                    ¦
     ?                        ?                    ?
+--------------+  +------------------+  +--------------+
¦ IMAGE STORE  ¦  ¦ VISION SERVICE   ¦  ¦ REASONING    ¦
¦ (temp cache) ¦  ¦ (Claude Vision)  ¦  ¦ SERVICE      ¦
¦              ¦  ¦                  ¦  ¦ (Claude3.5   ¦
¦ - Validation ¦  ¦ - Prompt with    ¦  ¦ Sonnet)      ¦
¦ - Compression¦  ¦   image          ¦  ¦              ¦
¦ - Cleanup    ¦  ¦ - Parse JSON out ¦  ¦ - Input:     ¦
¦              ¦  ¦ - Error handling ¦  ¦   extracted  ¦
+--------------+  +------------------+  ¦   data       ¦
                                         ¦ - Output:    ¦
                                         ¦   trade idea ¦
                                         ¦   + mentoring¦
                                         +--------------+
```

### Component Responsibilities

**Frontend Components:**
- ChartUpload.tsx: File input + drag-drop
- AnalysisLoader.tsx: Loading spinner
- TrendBadge.tsx: Visual trend display
- SupportResistanceCards.tsx: S/R zones
- TradeIdeaCard.tsx: Entry/SL/TP display
- MentorNote.tsx: Educational text
- ErrorAlert.tsx: Error messages

**API Route Handler (/api/analyze-chart):**
1. Parse multipart form data
2. Validate image (format, size, dimensions)
3. Preprocess image (optional: rotate, compress)
4. Call Vision Service ? ChartExtraction
5. Validate extraction schema
6. Call Reasoning Service ? TradeAnalysis
7. Format response to match API contract
8. Handle errors gracefully

**Vision Service:**
- Claude Vision API integration
- Strict JSON schema extraction
- Response parsing & validation
- Retry logic with backoff
- Input: image buffer
- Output: ChartExtraction JSON

**Reasoning Service:**
- Claude 3.5 Sonnet API integration
- Trade idea generation
- Mentor explanation
- Risk/reward calculation
- Input: ChartExtraction JSON
- Output: TradeAnalysis object

### Vision ? JSON vs End-to-End Analysis

YOUR APPROACH (Vision ? JSON ? Reasoning) IS CORRECT

Advantages:
| Aspect | Vision?JSON | End-to-End |
|--------|-----------|-----------|
| Debuggability | Can inspect extracted data | Hard to debug |
| Validation | Quality checkpoints | No checkpoints |
| Caching | Cache extractions | Everything cached |
| Cost optimization | Can use cheaper models later | Must use expensive model |
| Error recovery | Fallback if reasoning fails | Entire analysis fails |
| Multi-analysis | Reuse extraction | Must re-analyze |
| Testing | Mock extraction data | Mock entire pipeline |

Pattern:
Request ? [Vision] ? JSON ? [Validate] ? [Reasoning] ? Response

---

## SECTION 2: DATA FLOW ARCHITECTURE

### Complete Request-Response Flow

```
USER BROWSER
  ?
[1. Upload Chart]
  +- File picker / drag-drop
  +- Client validation
  +- POST /api/analyze-chart

  ? HTTP Request
  
[2. API: Image Validation]
  +- Parse multipart form
  +- Check format (PNG/JPG)
  +- Check size (max 10MB)
  +- Check dimensions (400x300 to 4000x4000)
  +- Return 400 if invalid

  ? Validation passes
  
[3. Image Preprocessing]
  +- Detect rotation (EXIF)
  +- Auto-rotate if needed
  +- Crop whitespace (optional)
  +- Enhance contrast (optional)
  +- Convert to base64

  ?
  
[4. Vision Service]
  +- Call Claude Vision API
  +- Wait 5-10 seconds
  +- Parse JSON response
  +- Validate against schema

  ? Extraction succeeds
  
[5. Extraction Validation]
  +- Check required fields
  +- Validate level values
  +- Check confidence > 40%
  +- Return 400 if validation fails

  ? Validation passes
  
[6. Reasoning Service]
  +- Call Claude 3.5 Sonnet
  +- Generate trade ideas
  +- Calculate risk/reward
  +- Write mentor explanation
  +- Return TradeAnalysis

  ?
  
[7. Response Formatting]
  +- Shape data to API contract
  +- Add metadata
  +- Return 200 with JSON

  ? HTTP Response
  
[8. Frontend Display]
  +- Parse response
  +- Show trend badge
  +- Display S/R cards
  +- Show trade idea
  +- Display mentor note
```

### Data Validation Strategy (Layered)

```
CLIENT VALIDATION (Frontend)
+- File size check
+- File type check
+- Purpose: Fail fast, UX

  ?

API INPUT VALIDATION
+- Strict file size
+- Format verification
+- Dimensions bounds
+- Purpose: Security

  ?

EXTRACTION VALIDATION
+- JSON schema (Zod)
+- Business logic checks
¦  +- Levels are reasonable
¦  +- Trend matches zones
¦  +- Confidence > 0
+- Purpose: Data quality

  ?

ANALYSIS VALIDATION
+- Trade logic check
+- Risk/reward correct
+- Entry/SL/TP order valid
```

### Image Preprocessing

```
Raw Image Input
  ?
[MIME Type Check] ? PNG or JPG?
  ?
[Size Check] ? 1KB to 10MB?
  ?
[Dimension Check] ? 400x300 to 4000x4000?
  ?
[EXIF Rotation] (Optional) ? Auto-rotate
  ?
[Whitespace Crop] (Optional) ? Remove excess
  ?
[Quality Enhancement] (Optional) ? Enhance brightness
  ?
[Base64 Encoding] ? Ready for Claude Vision
```

### Caching Strategy (Phase 1+)

```
REQUEST
  ?
[Check Cache]
  +- Hash image (SHA256)
  +- Look up by hash
  +- If found: return cached result
  +- If not: continue pipeline

  ?

[Run Pipeline] ? Full analysis

  ?

[Store in Cache]
  +- Key: image_hash
  +- TTL: 7 days
  +- Reduces API costs
```

Benefits:
- Same chart uploaded multiple times ? same analysis
- Cost: ~$0.003 saved per cached request
- Speed: ~2 seconds vs 15 seconds

---

## SECTION 3: SCALING & ERROR HANDLING

### Error Handling for Bad Charts

```
INPUT VALIDATION ERRORS
+- No file: 400 Bad Request
+- Wrong format (BMP): 400 Bad Request
+- Too large (>10MB): 413 Payload Too Large
+- Zero dimensions: 400 Bad Request

VISION EXTRACTION ERRORS
+- Not a chart: 400 + "Chart not recognized"
+- Model timeout: 504 Gateway Timeout
+- Rate limit: 429 Too Many Requests
+- Model error: 502 Bad Gateway

VALIDATION ERRORS
+- Invalid JSON: 502
+- Missing fields: 502
+- Low confidence: 400 + warning flag

FALLBACK STRATEGY
If both vision & reasoning fail:
+- Return fallback analysis
+- Status 200 (not 500)
+- Include "service unavailable" warning
+- User can try again
```

User-Friendly Messages:
```
IMAGE_VALIDATION_FAILED:
  Title: "Chart image not recognized"
  Description: "Please upload a clear forex chart screenshot"
  
UNSUPPORTED_FORMAT:
  Title: "File format not supported"
  Description: "Only PNG and JPG are supported"
  
SERVICE_UNAVAILABLE:
  Title: "Analysis service temporarily unavailable"
  Description: "Please try again in a few minutes"
  
TIMEOUT:
  Title: "Analysis took too long"
  Description: "Try a simpler or clearer chart"
```

### Request Rate & Concurrency

**Phase 1**: Synchronous processing
- 10-15 seconds per request
- Baseline: 240-360 analyses per hour
- Works for < 50 requests/minute

**Phase 2**: Add Rate Limiting
- 20 requests per minute per user
- Redis-based (Upstash)
- Per-IP limits for anonymous users

**Phase 2+**: Add Queue-Based Processing
- Async job queue (Bull/Redis)
- Return 202 Accepted immediately
- Client polls for result via job_id
- Handles 500+ requests/hour

---

## SECTION 4: INTEGRATION PATTERNS (Phase 2+)

### TradingView API Integration

```
AI Chart Mentor Core Service
  +- Vision extraction
  +- Reasoning
  
  + TradingView API (Phase 2)
  +- Real-time price data
  +- Historical bars
  +- Validate S/R levels
  
  + Broker API (Phase 3)
  +- Account balance
  +- Position size calculation
  +- One-click order placement
  
  + Economic Calendar (Phase 3)
  +- Major news events
  +- Risk warnings
```

---

## SECTION 5: MULTI-TIMEFRAME SUPPORT (Phase 2)

### Architecture Options

**Option A: Single Request ? Multiple Analyses (Recommended)**
```
User uploads 1 chart
  ?
API request: ?timeframes=M5,H1,H4
  ?
[Vision analyzes ONCE]
  ?
[Reasoning for M5] + [Reasoning for H1] + [Reasoning for H4]
  ?
[Confluence Check] ? How much do analyses agree?
  ?
Response with multi-timeframe ideas + confluence score
```

Benefits:
- 40% cost savings (share vision)
- Confluence scoring for stronger signals
- Better user experience

**Option B: Separate Requests (Simple)**
- User provides 3 images
- Run full pipeline 3x
- Higher API costs

---

## SECTION 6: BUILD ORDER & DEPENDENCIES

### Phase 1 (MVP) - 18-24 Hours Total

```
STEP 1: Backend API Infrastructure (2-3 hours)
+- /api/analyze-chart route
+- Error handling middleware
+- Input validation (Zod)
+- Logging setup
  
  ?

STEP 2: Vision Service (4-5 hours)
+- Claude Vision API client
+- Image preprocessing (sharp)
+- Extraction schema
+- Validation layer
  
  ?

STEP 3: Reasoning Service (3-4 hours)
+- Claude 3.5 Sonnet client
+- Trade idea prompts
+- Mentor explanation generation
  
  ?

STEP 4: API Contract & Testing (2-3 hours)
+- Response formatting
+- Contract tests
+- Documentation
  
  ?

STEP 5: Frontend UI (4-5 hours)
+- ChartUpload component
+- AnalysisDisplay component
+- Error handling UI
+- Loading states
  
  ?

STEP 6: E2E Testing & Polish (3-4 hours)
+- Test with real charts
+- Error case testing
+- Performance testing
+- Accessibility

  ?

?? LAUNCH PHASE 1
```

### Phase 2 (Scale + Accounts) - 23-29 Hours

```
+- Rate Limiting & Caching (3 hours)
+- User Authentication (4-5 hours)
+- Database & History (3-4 hours)
+- Multi-Timeframe (5-6 hours)
+- TradingView Integration (4-5 hours)
+- Image Annotation (4-5 hours)
```

### Phase 3 (Real-Time & Extension) - 19-24 Hours

```
+- WebSocket Real-Time (4-5 hours)
+- Browser Extension (4-5 hours)
+- Extension Chart Capture (5-6 hours)
+- Broker Integration (6-8 hours)
```

---

## SECTION 7: QUICK START

### Immediate (This Week)

- [ ] Create `/lib/services/vision.service.ts`
- [ ] Create `/lib/services/reasoning.service.ts`
- [ ] Create `/lib/validation/extraction.schema.ts`
- [ ] Create `/app/api/analyze-chart/route.ts`
- [ ] Unit tests for services
- [ ] ChartUpload component
- [ ] Test end-to-end with real chart

### Phase 1 Polish (Next 2 Weeks)

- [ ] Error handling (all failure modes)
- [ ] Image preprocessing
- [ ] Client-side validation
- [ ] Loading states
- [ ] Error notifications
- [ ] Test with 20+ chart images
- [ ] Accessibility audit
- [ ] Performance: < 15s response time
- [ ] Deploy to staging

### Phase 2 Prep

- [ ] Design Supabase schema
- [ ] Plan authentication flow
- [ ] Design cache key strategy
- [ ] Plan rate limiting thresholds
- [ ] Design multi-timeframe API

---

## KEY TAKEAWAYS

1. **Vision ? JSON ? Reasoning** is the RIGHT architecture
2. **Separate concerns** = easier scaling + testing
3. **Validation at each stage** = better error handling
4. **Phase 1 is synchronous** - simple & fast to ship
5. **Phase 2 adds persistence** - with minimal refactoring
6. **Error handling first** - prevents 80% of user complaints

**Build Phase 1. Ship it. Validate. Then scale with Phase 2.**
