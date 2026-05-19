# AI Chart Mentor API Documentation

## Overview

The AI Chart Mentor API provides instant forex chart analysis through a simple REST interface. Upload a chart image and receive trend analysis, support/resistance zones, and trade scenarios.

## Base URL

```
http://localhost:8000  # Local development
https://api.aichartmentor.com  # Production (TBD)
```

## Authentication

Phase 1 MVP is stateless - no authentication required. Phase 2 will add user authentication.

## Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-chart-mentor-backend",
  "version": "0.1.0"
}
```

**Status Code:** `200 OK`

---

### Analyze Chart

Upload a forex chart image and get instant analysis.

```http
POST /api/analyze-chart
Content-Type: multipart/form-data
```

**Request Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `file` | File | Yes | Chart image (PNG or JPG) |
| `pair` | String | No | Forex pair (e.g., EUR/USD) |
| `timeframe` | String | No | Chart timeframe (e.g., 4H) |

**Request Example:**
```bash
curl -X POST http://localhost:8000/api/analyze-chart \
  -F "file=@chart.png" \
  -F "pair=EUR/USD" \
  -F "timeframe=4H"
```

**Response Schema:**

```json
{
  "trend": "bullish",
  "zones": [
    {
      "type": "support",
      "price": 1.0750,
      "touches": 3,
      "strength": "strong"
    },
    {
      "type": "resistance",
      "price": 1.0900,
      "touches": 2,
      "strength": "moderate"
    }
  ],
  "scenarios": [
    {
      "direction": "bullish",
      "entry_price": 1.0800,
      "stop_loss": 1.0750,
      "take_profit": 1.0900,
      "risk_reward_ratio": 2.0,
      "confidence_score": 45.0
    }
  ],
  "mentor_explanation": "EUR/USD is in an uptrend...",
  "confidence_score": 45.0,
  "volatility_warning": null,
  "analysis_id": "abc123",
  "timestamp": "2025-05-19T10:30:00Z"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `trend` | string | "bullish", "bearish", or "consolidating" |
| `zones` | array | Support and resistance zones |
| `scenarios` | array | Trade scenarios (1-2 potential setups) |
| `mentor_explanation` | string | Educational explanation (3-5 sentences) |
| `confidence_score` | number | Overall confidence (0-65%) |
| `volatility_warning` | string\|null | Warning if unusual volatility detected |
| `analysis_id` | string | Unique ID for audit logging |
| `timestamp` | string | ISO 8601 timestamp |

**Zone Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | "support" or "resistance" |
| `price` | number | Price level |
| `touches` | integer | Number of price touches at level |
| `strength` | string | "weak", "moderate", or "strong" |

**Scenario Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `direction` | string | "bullish" or "bearish" |
| `entry_price` | number | Suggested entry price |
| `stop_loss` | number | Suggested stop-loss price |
| `take_profit` | number | Suggested take-profit price |
| `risk_reward_ratio` | number | TP-Entry / Entry-SL ratio |
| `confidence_score` | number | Confidence (0-65%, capped) |

**Status Codes:**

| Code | Meaning |
|------|---------|
| `200` | Analysis successful |
| `400` | Invalid image (format, size, dimensions) |
| `429` | Rate limited (too many requests) |
| `500` | Server error |
| `504` | Analysis timeout (>10s) |

**Error Response:**
```json
{
  "detail": "Image too large (6.2MB). Maximum size is 5MB.",
  "error_code": "IMAGE_TOO_LARGE"
}
```

---

## Image Requirements

| Requirement | Value |
|-------------|-------|
| **Format** | PNG or JPEG |
| **Min Dimensions** | 200x200 pixels |
| **Max Size** | 5 MB |
| **Color Mode** | Any (grayscale, RGB, etc.) |

---

## Response Times

| Scenario | Target |
|----------|--------|
| Cache hit | <500ms |
| First analysis | <5 seconds |
| Timeout fallback | 10 seconds |

---

## Rate Limiting

- **Phase 1:** No rate limiting (MVP)
- **Phase 2:** 100 requests/hour per user

---

## Caching

Analysis results are cached by image hash (SHA256) with 48-hour TTL.

- Same image → cached result
- Cache hit response: <500ms
- Saves API costs and improves performance

---

## Interactive Documentation

FastAPI automatically generates interactive API docs:

- **Swagger UI:** `GET /docs`
- **ReDoc:** `GET /redoc`

Visit these URLs to explore and test endpoints interactively.

---

## Error Handling

### Common Errors

**Invalid Image Format:**
```json
{
  "detail": "Only PNG and JPG images are allowed",
  "error_code": "INVALID_FORMAT"
}
```

**Image Too Small:**
```json
{
  "detail": "Image too small (150x150px). Minimum size is 200x200px.",
  "error_code": "IMAGE_TOO_SMALL"
}
```

**Analysis Failed:**
```json
{
  "detail": "Unable to analyze chart. Please try another image.",
  "error_code": "ANALYSIS_FAILED"
}
```

**Server Error:**
```json
{
  "detail": "Internal server error",
  "error_code": "SERVER_ERROR"
}
```

---

## Best Practices

### Client-Side

1. **Validate before upload**
   - Check image type (PNG/JPG)
   - Verify dimensions (>200x200)
   - Check file size (<5MB)

2. **Handle timeouts gracefully**
   - Set 10-second timeout
   - Retry with exponential backoff
   - Show fallback message after timeout

3. **Show progress**
   - Use upload progress callbacks
   - Animate loading spinner during analysis
   - Display confidence score appropriately

### Server-Side

4. **Logging**
   - All analyses logged to audit trail
   - No chart images stored (privacy)
   - Cleanup logs after 30 days

5. **Monitoring**
   - Track response times
   - Monitor API health
   - Alert on errors

---

## Limitations (Phase 1)

- ❌ No user authentication
- ❌ No analysis history
- ❌ Forex pairs only
- ❌ Single timeframe analysis
- ❌ No multi-asset support (crypto, stocks, indices)

These will be added in Phase 2 after MVP validation.

---

## Disclaimer

⚠️ **Important:** This API provides educational analysis only, not financial advice.

- Analysis confidence is capped at 65%
- Past patterns do not guarantee future results
- Trading forex carries substantial risk of loss
- Always conduct your own research

See DISCLAIMERS section in UI for full terms.

---

## Support

For issues or questions:
1. Check the interactive docs: `/docs`
2. Review examples below
3. Open an issue on GitHub

---

## Examples

### Python

```python
import requests

url = "http://localhost:8000/api/analyze-chart"
files = {"file": open("chart.png", "rb")}
data = {"pair": "EUR/USD", "timeframe": "4H"}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"Trend: {result['trend']}")
print(f"Confidence: {result['confidence_score']}%")
```

### JavaScript/TypeScript

```typescript
const formData = new FormData()
formData.append("file", chartImage)
formData.append("pair", "EUR/USD")

const response = await fetch("http://localhost:8000/api/analyze-chart", {
  method: "POST",
  body: formData,
})

const result = await response.json()
console.log(`Trend: ${result.trend}`)
```

### cURL

```bash
curl -X POST http://localhost:8000/api/analyze-chart \
  -F "file=@chart.png" \
  -F "pair=EUR/USD" \
  -F "timeframe=4H"
```

---

**API Version:** 0.1.0  
**Last Updated:** 2025-05-19
