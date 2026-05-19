# AI Chart Mentor: Implementation Reference

## API Contract & Response Shapes

### POST /api/analyze-chart

**Request:**
```
Content-Type: multipart/form-data

{
  "image": <File: PNG or JPG, 1KB-10MB>
}
```

**Success Response (200 OK):**
```json
{
  "trend": "bullish|bearish|ranging",
  
  "support": [
    {
      "level_min": 1.0820,
      "level_max": 1.0830,
      "strength": "weak|medium|strong"
    }
  ],
  
  "resistance": [
    {
      "level_min": 1.0910,
      "level_max": 1.0920,
      "strength": "medium"
    }
  ],
  
  "idea": {
    "direction": "buy|sell",
    "entry": "1.0835",
    "stop_loss": 1.0800,
    "take_profit": 1.0920,
    "risk_reward": "1:3",
    "rationale": "Price has bounced off support zone..."
  },
  
  "mentor_note": "Clear bullish trend with strong support...",
  
  "metadata": {
    "processing_time_ms": 12500,
    "confidence": 0.85,
    "chart_pattern": "Higher Highs & Higher Lows",
    "market_context": "Uptrend with pullback opportunity"
  }
}
```

**Error Responses:**

400 Bad Request - Input validation failed
```json
{
  "error": "Chart image invalid: File too large",
  "details": {
    "field": "image",
    "reason": "max_size_exceeded"
  }
}
```

502 Bad Gateway - Vision extraction failed
```json
{
  "error": "Analysis service unavailable, please retry"
}
```

429 Too Many Requests - Rate limited
```json
{
  "error": "Too many requests",
  "retry_after": 45
}
```

---

## Service Implementation Guide

### Vision Service Skeleton

```typescript
// lib/services/vision.service.ts

interface ChartExtraction {
  trend: 'bullish' | 'bearish' | 'ranging';
  swing_highs: number[];
  swing_lows: number[];
  support_zones: Array<{
    level_min: number;
    level_max: number;
    strength: 'weak' | 'medium' | 'strong';
  }>;
  resistance_zones: Array<{
    level_min: number;
    level_max: number;
    strength: 'weak' | 'medium' | 'strong';
  }>;
  chart_patterns?: string[];
  current_price?: number;
  confidence: number;
}

class VisionService {
  async extractChart(imageBuffer: Buffer): Promise<ChartExtraction> {
    // 1. Convert buffer to base64
    const base64 = imageBuffer.toString('base64');
    
    // 2. Call Claude Vision API
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        system: 'You are an expert forex chart analyst...',
        messages: [{
          role: 'user',
          content: [
            {
              type: 'image',
              source: {
                type: 'base64',
                media_type: 'image/jpeg',
                data: base64
              }
            },
            {
              type: 'text',
              text: 'Extract chart data as JSON: ...'
            }
          ]
        }]
      })
    });
    
    // 3. Parse response
    const json = JSON.parse(response.content[0].text);
    
    // 4. Validate with schema
    const validated = chartExtractionSchema.parse(json);
    
    return validated;
  }
}

export const visionService = new VisionService();
```

### Reasoning Service Skeleton

```typescript
// lib/services/reasoning.service.ts

interface TradeAnalysis {
  trend: string;
  market_context: string;
  ideas: Array<{
    direction: 'buy' | 'sell';
    entry_zone: string;
    stop_loss: number;
    take_profit: number;
    risk_reward: string;
    rationale: string;
  }>;
  mentor_note: string;
}

class ReasoningService {
  async generateAnalysis(
    extraction: ChartExtraction,
    options?: { timeframe?: string }
  ): Promise<TradeAnalysis> {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        system: 'You are a professional forex trading mentor...',
        messages: [{
          role: 'user',
          content: `Analyze this chart extraction and generate trade ideas:
${JSON.stringify(extraction, null, 2)}

Provide exactly 1-2 trade scenarios with:
- Direction (buy/sell)
- Entry zone
- Stop loss level
- Take profit level
- Risk-reward ratio
- Clear rationale

Also write a 100-150 word mentor explanation.`
        }]
      })
    });
    
    const analysisText = response.content[0].text;
    const analysis = parseTradeAnalysis(analysisText);
    
    return analysis;
  }
}

export const reasoningService = new ReasoningService();
```

### Validation Schema

```typescript
// lib/validation/extraction.schema.ts

import { z } from 'zod';

const zoneSchema = z.object({
  level_min: z.number().positive(),
  level_max: z.number().positive(),
  strength: z.enum(['weak', 'medium', 'strong'])
});

export const chartExtractionSchema = z.object({
  trend: z.enum(['bullish', 'bearish', 'ranging']),
  swing_highs: z.array(z.number().positive()),
  swing_lows: z.array(z.number().positive()),
  support_zones: z.array(zoneSchema),
  resistance_zones: z.array(zoneSchema),
  chart_patterns: z.array(z.string()).optional(),
  current_price: z.number().positive().optional(),
  confidence: z.number().min(0).max(100)
});
```

---

## Error Handling Patterns

### Create Error Types

```typescript
// lib/types/errors.ts

export class AnalysisError extends Error {
  constructor(
    public statusCode: number,
    public userMessage: string,
    public details?: Record<string, unknown>
  ) {
    super(userMessage);
    this.name = 'AnalysisError';
  }
}

export class ImageValidationError extends AnalysisError {
  constructor(reason: string) {
    super(400, `Chart image invalid: ${reason}`);
  }
}

export class VisionServiceError extends AnalysisError {
  constructor(reason: string) {
    super(502, 'Chart analysis service unavailable');
  }
}

export class TimeoutError extends AnalysisError {
  constructor() {
    super(504, 'Analysis took too long, please try again');
  }
}

export class RateLimitError extends AnalysisError {
  constructor(retryAfter: number) {
    super(429, 'Too many requests', { retry_after: retryAfter });
  }
}
```

### API Route Error Handling

```typescript
// app/api/analyze-chart/route.ts

export async function POST(request: Request) {
  try {
    // 1. Parse form data
    const formData = await request.formData();
    const file = formData.get('image') as File;
    
    // 2. Validate input
    if (!file) throw new ImageValidationError('No image file');
    if (file.size > 10 * 1024 * 1024) {
      throw new ImageValidationError('File too large (max 10MB)');
    }
    if (!['image/png', 'image/jpeg'].includes(file.type)) {
      throw new ImageValidationError('Only PNG/JPG supported');
    }
    
    // 3. Preprocess
    const buffer = await file.arrayBuffer();
    const processedBuffer = await preprocessImage(Buffer.from(buffer));
    
    // 4. Vision extraction with timeout & retry
    const extraction = await withRetry(
      () => withTimeout(
        visionService.extractChart(processedBuffer),
        30_000,
        'Vision extraction timeout'
      ),
      3
    );
    
    // 5. Validate extraction
    const validated = chartExtractionSchema.parse(extraction);
    if (validated.confidence < 40) {
      console.warn('Low confidence extraction:', validated.confidence);
    }
    
    // 6. Reasoning with timeout
    const analysis = await withTimeout(
      reasoningService.generateAnalysis(validated),
      15_000,
      'Trade idea generation timeout'
    );
    
    // 7. Format response
    return Response.json(analysis);
    
  } catch (error) {
    if (error instanceof AnalysisError) {
      return Response.json(
        {
          error: error.userMessage,
          details: error.details
        },
        { status: error.statusCode }
      );
    }
    
    console.error('Unexpected error:', error);
    return Response.json(
      { error: 'Analysis failed. Please try again.' },
      { status: 500 }
    );
  }
}

async function withTimeout<T>(
  promise: Promise<T>,
  ms: number,
  message: string
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new TimeoutError()), ms)
    )
  ]);
}

async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, baseDelay * Math.pow(2, attempt)));
    }
  }
}
```

---

## Frontend Integration

### ChartUpload Component

```typescript
// components/ChartUpload.tsx

'use client';

import { useState } from 'react';

export function ChartUpload() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState<string | null>(null);
  
  async function handleUpload(file: File) {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
      const response = await fetch('/api/analyze-chart', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Analysis failed');
      }
      
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }
  
  return (
    <div>
      {loading && <div>Analyzing chart...</div>}
      {error && <div className="text-red-500">{error}</div>}
      {result && <AnalysisDisplay result={result} />}
      {!loading && !result && <FileUploadInput onUpload={handleUpload} />}
    </div>
  );
}
```

---

## Testing Checklist

**Unit Tests:**
- [ ] Validation schemas parse valid extraction JSON
- [ ] Validation schemas reject malformed data
- [ ] Error types have correct status codes
- [ ] Retry logic backs off exponentially
- [ ] Timeout throws at correct duration

**Integration Tests:**
- [ ] API endpoint accepts multipart form data
- [ ] API endpoint validates file type/size
- [ ] API endpoint calls vision service
- [ ] API endpoint validates extraction
- [ ] API endpoint calls reasoning service
- [ ] API endpoint returns correct JSON shape

**E2E Tests:**
- [ ] User can upload chart image
- [ ] Result displays trend badge
- [ ] Result displays support/resistance
- [ ] Result displays trade idea
- [ ] Result displays mentor note
- [ ] Error message shows for bad image

**Performance Tests:**
- [ ] End-to-end latency < 20 seconds
- [ ] Vision extraction < 10 seconds
- [ ] Reasoning < 5 seconds
- [ ] Image preprocessing < 1 second

