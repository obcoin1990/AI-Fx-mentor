"""
Prompt templates for Claude Vision and Reasoning APIs
"""

VISION_PROMPT = """
Analyze this forex chart image and extract the following information in JSON format:

1. TREND: Identify the overall trend (bullish, bearish, or consolidating)
   - Confidence score (0-100%)
   - Reason for assessment

2. SUPPORT ZONES: Identify 2-3 significant support zones where price has bounced multiple times
   - Price level
   - Number of touches at this level
   - Zone strength (weak, moderate, strong)

3. RESISTANCE ZONES: Identify 2-3 significant resistance zones where price has been rejected
   - Price level
   - Number of touches at this level
   - Zone strength (weak, moderate, strong)

4. SWING HIGHS & LOWS: Mark 3-5 most recent significant highs and lows
   - Price levels
   - Approximate dates/candles if visible

5. CHART PATTERNS: Identify any recognizable patterns
   - Pattern type (double top/bottom, channel, triangle, flag, head & shoulders, etc.)
   - Pattern location on chart
   - Pattern reliability (weak, moderate, strong)

6. VOLATILITY WARNING: Flag if market shows unusual volatility or gaps

IMPORTANT CONSTRAINTS:
- FOREX ONLY: Analyze only forex pairs (EUR/USD, GBP/USD, etc.)
- NO HALLUCINATION: Every price level must be visible on the chart
- If you cannot clearly identify a requested element, mark as null/not_found
- Return ONLY valid JSON, no markdown formatting

Return response as valid JSON object.
"""

REASONING_PROMPT = """
Based on this vision analysis of a forex chart, generate trade scenarios:

INPUT (Vision Analysis):
{vision_data}

TASKS:
1. Generate 1-2 trade scenarios based on the identified trend and zones
   - Each scenario includes:
     - Direction (bullish or bearish)
     - Entry price (must be visible on chart from vision data)
     - Stop-loss placement (below support for bullish, above resistance for bearish)
     - Take-profit target (using 1:2 to 1:3 risk-reward)
     - Risk-reward ratio
     - Confidence score (0-65%, MUST be capped at 65%)

2. Write mentor-style explanation (3-5 sentences)
   - Plain English, educational tone
   - Explain WHY these scenarios make sense
   - Mention key support/resistance levels
   - Acknowledge risk and uncertainty
   - NO phrases like "You should", "I recommend", "Buy now" - stay neutral

3. Flag confidence < 50% as "unreliable"

CONSTRAINTS:
- Confidence MUST NOT exceed 65%
- Entry prices MUST match chart data from vision analysis
- Explanation must be educational, not financial advice
- If vision data is incomplete, explain limitations

Return ONLY valid JSON object with: scenarios, mentor_explanation, overall_confidence
"""

def get_vision_prompt() -> str:
    """Get the vision analysis prompt"""
    return VISION_PROMPT

def get_reasoning_prompt(vision_data: str) -> str:
    """Get the reasoning prompt with vision data"""
    return REASONING_PROMPT.format(vision_data=vision_data)
