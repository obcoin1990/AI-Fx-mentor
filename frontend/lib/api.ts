/**
 * API client for backend communication via Vercel serverless functions
 */

const REQUEST_TIMEOUT = 30000 // 30 seconds for analysis

export interface VisionAnalysisResult {
  success: boolean
  trend: string
  trend_confidence: number
  support_zones: Array<{
    zone_type: 'support' | 'resistance'
    price_level: number
    touch_count: number
    strength: 'weak' | 'moderate' | 'strong'
  }>
  resistance_zones: Array<{
    zone_type: 'support' | 'resistance'
    price_level: number
    touch_count: number
    strength: 'weak' | 'moderate' | 'strong'
  }>
  patterns_detected: string[]
  swing_highs?: number[]
  swing_lows?: number[]
  volatility_warning?: string | null
  analysis_id: string
  timestamp: string
  pair?: string
  timeframe?: string
}

export interface TradeScenario {
  direction: 'bullish' | 'bearish'
  entry_price: number
  stop_loss: number
  take_profit: number
  risk_reward_ratio: number
  confidence_score: number
}

export interface ReasoningResult {
  success: boolean
  scenarios: TradeScenario[]
  mentor_explanation: string
  overall_confidence: number
  pair?: string
  timeframe?: string
  analysis_id: string
  timestamp: string
}

export interface AnalysisResult extends VisionAnalysisResult {
  scenarios: TradeScenario[]
  mentor_explanation: string
  overall_confidence: number
}

/**
 * Upload a chart image and get vision analysis
 */
export async function uploadChart(
  file: File,
  pair?: string,
  timeframe?: string,
  onProgress?: (percent: number) => void
): Promise<VisionAnalysisResult> {
  const formData = new FormData()
  formData.append('image', file)
  if (pair) formData.append('pair', pair)
  if (timeframe) formData.append('timeframe', timeframe)

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()

    // Setup timeout
    const timeoutId = setTimeout(() => {
      xhr.abort()
      reject(new Error('Analysis request timed out. Please try again.'))
    }, REQUEST_TIMEOUT)

    // Progress tracking
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percent = Math.round((e.loaded / e.total) * 100)
        onProgress?.(percent)
      }
    })

    // Handle completion
    xhr.addEventListener('load', () => {
      clearTimeout(timeoutId)

      if (xhr.status === 200) {
        try {
          const result = JSON.parse(xhr.responseText) as VisionAnalysisResult
          resolve(result)
        } catch (error) {
          reject(new Error('Invalid response from server'))
        }
      } else if (xhr.status === 400) {
        try {
          const errorData = JSON.parse(xhr.responseText)
          reject(new Error(errorData.error || 'Invalid chart image. Please try another.'))
        } catch {
          reject(new Error('Invalid chart image. Please try another.'))
        }
      } else if (xhr.status === 429) {
        reject(new Error('Too many requests. Please wait a moment and try again.'))
      } else if (xhr.status === 503) {
        reject(new Error('Analysis service is temporarily unavailable. Please try again.'))
      } else {
        reject(new Error(`Server error: ${xhr.status}`))
      }
    })

    // Handle errors
    xhr.addEventListener('error', () => {
      clearTimeout(timeoutId)
      reject(new Error('Failed to connect to analysis server'))
    })

    xhr.addEventListener('abort', () => {
      clearTimeout(timeoutId)
      reject(new Error('Request cancelled'))
    })

    // Send request to Vercel API route
    xhr.open('POST', '/api/analyze-chart')
    xhr.send(formData)
  })
}

/**
 * Generate trade scenarios from vision analysis results
 */
export async function generateScenarios(
  visionData: VisionAnalysisResult,
  pair?: string,
  timeframe?: string
): Promise<ReasoningResult> {
  try {
    const response = await fetch('/api/reason', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        analysis: {
          trend: visionData.trend,
          trend_confidence: visionData.trend_confidence,
          support_zones: visionData.support_zones,
          resistance_zones: visionData.resistance_zones,
          patterns_detected: visionData.patterns_detected,
          swing_highs: visionData.swing_highs,
          swing_lows: visionData.swing_lows,
          volatility_warning: visionData.volatility_warning,
        },
        pair: pair || visionData.pair,
        timeframe: timeframe || visionData.timeframe,
      }),
      signal: AbortSignal.timeout(REQUEST_TIMEOUT),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.error || `Reasoning service error: ${response.status}`
      )
    }

    const result = (await response.json()) as ReasoningResult
    return result
  } catch (error) {
    if (error instanceof Error) {
      throw error
    }
    throw new Error('Failed to generate scenarios')
  }
}

/**
 * Check if API is available
 */
export async function isApiAvailable(): Promise<boolean> {
  try {
    const response = await fetch('/api/analyze-chart', {
      method: 'HEAD',
      signal: AbortSignal.timeout(5000),
    })
    return response.ok || response.status === 405 // 405 = Method Not Allowed (but endpoint exists)
  } catch {
    return false
  }
}
