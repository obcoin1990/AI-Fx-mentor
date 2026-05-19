# AI Chart Mentor: Scaling & Advanced Patterns

## Section 1: Caching Implementation

### Image Hash-Based Caching

```typescript
// lib/cache/analysis.cache.ts

import crypto from 'crypto';

interface CacheEntry {
  analysis: AnalysisResponse;
  timestamp: number;
  ttl: number; // seconds
}

const CACHE_TTL = 7 * 24 * 60 * 60; // 7 days

class AnalysisCache {
  private cache = new Map<string, CacheEntry>();
  
  getHash(buffer: Buffer): string {
    return crypto.createHash('sha256')
      .update(buffer)
      .digest('hex');
  }
  
  get(hash: string): AnalysisResponse | null {
    const entry = this.cache.get(hash);
    if (!entry) return null;
    
    // Check if expired
    if (Date.now() - entry.timestamp > entry.ttl * 1000) {
      this.cache.delete(hash);
      return null;
    }
    
    return entry.analysis;
  }
  
  set(hash: string, analysis: AnalysisResponse): void {
    this.cache.set(hash, {
      analysis,
      timestamp: Date.now(),
      ttl: CACHE_TTL
    });
  }
}

export const analysisCache = new AnalysisCache();
```

### Using Cache in API Route

```typescript
// In /api/analyze-chart:

const imageHash = analysisCache.getHash(buffer);

// Check cache first
const cached = analysisCache.get(imageHash);
if (cached) {
  console.log('Cache hit:', imageHash);
  return Response.json(cached);
}

// Run full pipeline
const extraction = await visionService.extractChart(buffer);
const analysis = await reasoningService.generateAnalysis(extraction);

// Cache result
analysisCache.set(imageHash, analysis);

return Response.json(analysis);
```

### Phase 2: Redis-Based Caching

```typescript
// lib/cache/redis.cache.ts

import { Redis } from '@upstash/redis';

const redis = Redis.fromEnv();
const CACHE_KEY_PREFIX = 'chart-analysis:';
const CACHE_TTL = 7 * 24 * 60 * 60; // 7 days

async function getCachedAnalysis(
  imageHash: string
): Promise<AnalysisResponse | null> {
  try {
    const cached = await redis.get(
      `${CACHE_KEY_PREFIX}${imageHash}`
    );
    return cached as AnalysisResponse | null;
  } catch (error) {
    console.warn('Cache read error:', error);
    return null;
  }
}

async function setCachedAnalysis(
  imageHash: string,
  analysis: AnalysisResponse
): Promise<void> {
  try {
    await redis.setex(
      `${CACHE_KEY_PREFIX}${imageHash}`,
      CACHE_TTL,
      JSON.stringify(analysis)
    );
  } catch (error) {
    console.warn('Cache write error:', error);
    // Continue without cache
  }
}
```

---

## Section 2: Rate Limiting

### Per-User Rate Limiting

```typescript
// lib/services/rate-limiter.ts

import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const redis = Redis.fromEnv();

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(
    20, // 20 requests
    '1 m'  // per 1 minute
  )
});

export async function checkRateLimit(
  identifier: string
): Promise<{ allowed: boolean; remaining: number; resetIn: number }> {
  const { success, limit, reset, remaining } = await ratelimit.limit(
    identifier
  );
  
  return {
    allowed: success,
    remaining: Math.max(0, remaining),
    resetIn: Math.max(0, Math.ceil((reset - Date.now()) / 1000))
  };
}
```

### In API Route

```typescript
export async function POST(request: Request) {
  // Get identifier (IP for anonymous, user_id for logged-in)
  const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
  
  // Check rate limit
  const rateLimit = await checkRateLimit(identifier);
  if (!rateLimit.allowed) {
    return Response.json(
      {
        error: 'Too many requests',
        retry_after: rateLimit.resetIn
      },
      { 
        status: 429,
        headers: { 'Retry-After': rateLimit.resetIn.toString() }
      }
    );
  }
  
  // Continue with analysis...
}
```

### Tiered Rate Limits (Phase 2)

```typescript
interface RateLimitConfig {
  tier: 'free' | 'pro' | 'enterprise';
  requestsPerHour: number;
  requestsPerDay: number;
  maxConcurrent: number;
}

const RATE_LIMITS: Record<string, RateLimitConfig> = {
  free: {
    tier: 'free',
    requestsPerHour: 5,
    requestsPerDay: 20,
    maxConcurrent: 1
  },
  pro: {
    tier: 'pro',
    requestsPerHour: 100,
    requestsPerDay: 500,
    maxConcurrent: 3
  },
  enterprise: {
    tier: 'enterprise',
    requestsPerHour: -1, // unlimited
    requestsPerDay: -1,
    maxConcurrent: 10
  }
};
```

---

## Section 3: Error Recovery & Fallbacks

### Fallback Analysis

```typescript
// lib/services/fallback.ts

const FALLBACK_ANALYSIS: AnalysisResponse = {
  trend: 'ranging',
  support: [],
  resistance: [],
  idea: {
    direction: 'buy',
    entry: 'Current price',
    stop_loss: 0,
    take_profit: 0,
    risk_reward: '1:1',
    rationale: 'Chart analysis temporarily unavailable'
  },
  mentor_note: 'Our AI service is currently overloaded. Please try again in a few minutes.'
};

export function getFallbackAnalysis(): AnalysisResponse {
  return FALLBACK_ANALYSIS;
}
```

### Circuit Breaker Pattern

```typescript
// lib/services/circuit-breaker.ts

enum CircuitState {
  CLOSED = 'CLOSED',     // Normal operation
  OPEN = 'OPEN',         // Failing, reject requests
  HALF_OPEN = 'HALF_OPEN' // Testing if recovered
}

class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime = 0;
  
  private readonly failureThreshold = 5;
  private readonly successThreshold = 2;
  private readonly timeout = 60 * 1000; // 1 minute
  
  async execute<T>(
    fn: () => Promise<T>,
    fallback: T
  ): Promise<T> {
    // Check if we should try to recover
    if (this.state === CircuitState.OPEN) {
      const elapsed = Date.now() - this.lastFailureTime;
      if (elapsed > this.timeout) {
        this.state = CircuitState.HALF_OPEN;
        this.successCount = 0;
      } else {
        // Still open, return fallback
        return fallback;
      }
    }
    
    try {
      const result = await fn();
      
      if (this.state === CircuitState.HALF_OPEN) {
        this.successCount++;
        if (this.successCount >= this.successThreshold) {
          this.state = CircuitState.CLOSED;
          this.failureCount = 0;
          this.successCount = 0;
        }
      }
      
      return result;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();
      
      if (this.failureCount >= this.failureThreshold) {
        this.state = CircuitState.OPEN;
        console.warn('Circuit breaker opened');
      }
      
      if (this.state === CircuitState.HALF_OPEN) {
        this.state = CircuitState.OPEN;
      }
      
      throw error;
    }
  }
}
```

---

## Section 4: Async/Queue Processing (Phase 2+)

### Bull Queue Setup

```typescript
// lib/queue/analysis.queue.ts

import Queue from 'bull';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

export const analysisQueue = new Queue('chart-analysis', {
  redis,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000
    },
    removeOnComplete: true
  }
});

// Job data shape
export interface AnalysisJob {
  jobId: string;
  imageBuffer: Buffer;
  userId?: string;
  createdAt: number;
}

export interface JobResult {
  jobId: string;
  analysis: AnalysisResponse;
  completedAt: number;
}
```

### Queue Worker

```typescript
// lib/queue/analysis.worker.ts

analysisQueue.process(async (job) => {
  const { imageBuffer } = job.data as AnalysisJob;
  
  // Track progress
  job.progress(10); // 10% - started
  
  // Vision extraction
  const extraction = await visionService.extractChart(imageBuffer);
  job.progress(50); // 50% - extraction done
  
  // Reasoning
  const analysis = await reasoningService.generateAnalysis(extraction);
  job.progress(90); // 90% - reasoning done
  
  // Store result (in cache or DB)
  const result: JobResult = {
    jobId: job.id.toString(),
    analysis,
    completedAt: Date.now()
  };
  
  // Store in Redis for 1 hour
  await redis.setex(
    `job-result:${job.id}`,
    3600,
    JSON.stringify(result)
  );
  
  return result;
});

// Handle failures
analysisQueue.on('failed', (job, error) => {
  console.error(`Job ${job.id} failed:`, error);
});

// Handle completion
analysisQueue.on('completed', (job) => {
  console.log(`Job ${job.id} completed`);
});
```

### Async API Endpoint

```typescript
// app/api/analyze-chart-async/route.ts

export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get('image') as File;
  
  // Validate input
  if (!file || !isValidChart(file)) {
    return Response.json({ error: 'Invalid image' }, { status: 400 });
  }
  
  // Convert to buffer
  const buffer = Buffer.from(await file.arrayBuffer());
  
  // Add to queue
  const job = await analysisQueue.add({
    imageBuffer: buffer,
    userId: getUserId(request),
    createdAt: Date.now()
  });
  
  // Return job ID immediately
  return Response.json(
    {
      job_id: job.id,
      status: 'pending',
      check_status_url: `/api/analysis-status/${job.id}`
    },
    { status: 202 } // Accepted
  );
}

// Status check endpoint
export async function GET(request: Request) {
  const jobId = new URL(request.url).searchParams.get('job_id');
  
  const job = await analysisQueue.getJob(jobId);
  
  if (!job) {
    // Check if already completed
    const result = await redis.get(`job-result:${jobId}`);
    if (result) {
      return Response.json(JSON.parse(result));
    }
    return Response.json({ error: 'Job not found' }, { status: 404 });
  }
  
  return Response.json({
    job_id: jobId,
    status: job.getState(),
    progress: job.progress(),
    is_completed: job.isCompleted(),
    is_failed: job.isFailed()
  });
}
```

### Frontend Polling

```typescript
// Frontend: Poll for results

async function submitChartAsync(file: File) {
  const formData = new FormData();
  formData.append('image', file);
  
  const response = await fetch('/api/analyze-chart-async', {
    method: 'POST',
    body: formData
  });
  
  const { job_id } = await response.json();
  
  // Poll for result
  const maxAttempts = 60; // 2 minutes max
  for (let i = 0; i < maxAttempts; i++) {
    const statusResponse = await fetch(`/api/analysis-status?job_id=${job_id}`);
    const status = await statusResponse.json();
    
    if (status.analysis) {
      // Completed!
      return status;
    }
    
    // Wait 2 seconds before checking again
    await new Promise(r => setTimeout(r, 2000));
  }
  
  throw new Error('Analysis took too long');
}
```

---

## Section 5: Monitoring & Metrics

### Prometheus Metrics

```typescript
// lib/monitoring/metrics.ts

import client from 'prom-client';

// Counter: total analyses
const analysesTotal = new client.Counter({
  name: 'chart_analyses_total',
  help: 'Total chart analyses',
  labelNames: ['status'] // success, failure, timeout
});

// Histogram: latencies
const visionLatency = new client.Histogram({
  name: 'vision_extraction_duration_seconds',
  help: 'Vision extraction latency',
  buckets: [0.5, 1, 2, 5, 10, 30]
});

const reasoningLatency = new client.Histogram({
  name: 'reasoning_duration_seconds',
  help: 'Reasoning model latency',
  buckets: [0.5, 1, 2, 5, 10]
});

const totalLatency = new client.Histogram({
  name: 'analysis_total_duration_seconds',
  help: 'End-to-end analysis latency',
  buckets: [2, 5, 10, 15, 20, 30]
});

// Gauge: API key rate limits remaining
const rateLimitRemaining = new client.Gauge({
  name: 'api_rate_limit_remaining',
  help: 'Claude API rate limit remaining'
});

export const metrics = {
  analysesTotal,
  visionLatency,
  reasoningLatency,
  totalLatency,
  rateLimitRemaining
};
```

### Track Metrics in Route

```typescript
// In /api/analyze-chart:

const startTime = Date.now();

try {
  const extraction = await visionService.extractChart(buffer);
  metrics.visionLatency.observe((Date.now() - startTime) / 1000);
  
  const analysis = await reasoningService.generateAnalysis(extraction);
  metrics.reasoningLatency.observe((Date.now() - startTime) / 1000);
  
  metrics.analysesTotal.inc({ status: 'success' });
  metrics.totalLatency.observe((Date.now() - startTime) / 1000);
  
} catch (error) {
  metrics.analysesTotal.inc({ status: 'failure' });
  throw error;
}
```

---

## Section 6: Cost Optimization

### API Cost Tracking

```
Vision Model (Claude 3.5 Sonnet):
- Input: ~$0.0003 per 1K tokens
- Output: ~$0.0015 per 1K tokens
- Typical request: 1-2K input tokens
- Cost per image: ~$0.0003-0.0006

Reasoning Model (Claude 3.5 Sonnet):
- Input: ~$0.0003 per 1K tokens
- Output: ~$0.0015 per 1K tokens
- Typical request: 500-1K input tokens
- Cost per analysis: ~$0.0002-0.0005

Total per analysis: ~$0.0005-0.0011
At 100 analyses/day: $0.05-0.11/day
At 3000 analyses/day: $1.50-3.30/day

Cost Reduction Strategies:
1. Image caching (SHA256 hash)
   - Same image = same analysis
   - Save: ~40% for repeated charts
   
2. Batch processing
   - Queue-based (Phase 2+)
   - Process during off-peak hours
   
3. Model optimization
   - Use GPT-4o Mini for reasoning instead of Sonnet (70% cheaper)
   - Cache system prompts
   
4. Response compression
   - Gzip responses
   - Reduce transmission costs
```

