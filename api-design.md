# API Design

## POST /api/analyze-chart
### Request
- image: file (PNG/JPG)

### Response
{
  \"trend\": \"bullish\",
  \"support\": [\"1.0820-1.0830\"],
  \"resistance\": [\"1.0910-1.0920\"],
  \"idea\": {
    \"direction\": \"buy\",
    \"entry\": \"1.0830\",
    \"stop_loss\": \"1.0800\",
    \"take_profit\": \"1.0915\",
    \"rr\": \"1:3\"
  },
  \"mentor_note\": \"Price is in an uptrend...\"
}
