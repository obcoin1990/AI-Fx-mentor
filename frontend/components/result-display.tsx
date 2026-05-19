'use client'

import React from 'react'
import TrendBadge from './trend-badge'
import ZoneCard from './zone-card'
import TradeIdeaCard from './trade-idea-card'
import MentorExplanation from './mentor-explanation'
import Disclaimers from './disclaimers'

interface AnalysisResult {
  success: boolean
  trend?: string
  trend_confidence?: number
  support_zones?: any[]
  resistance_zones?: any[]
  patterns_detected?: string[]
  scenarios?: any[]
  mentor_explanation?: string
  overall_confidence?: number
  pair?: string
  timeframe?: string
  analysis_id?: string
  timestamp?: string
}

interface ResultDisplayProps {
  results: AnalysisResult | null
  isLoading?: boolean
}

export default function ResultDisplay({ results, isLoading = false }: ResultDisplayProps) {
  if (isLoading) {
    return (
      <div className="space-y-lg animate-fade-in">
        <div className="card-elevated p-lg">
          <div className="flex items-center gap-lg mb-lg">
            <div className="animate-spin text-3xl">⚙️</div>
            <div>
              <h2 className="typo-title-lg text-on-dark font-bold">
                Analyzing Chart...
              </h2>
              <p className="typo-body-sm text-muted mt-xs">
                Processing image with vision AI
              </p>
            </div>
          </div>
          <div className="space-y-md">
            <div className="h-20 bg-surface-card-dark rounded-lg animate-pulse" />
            <div className="h-24 bg-surface-card-dark rounded-lg animate-pulse" />
            <div className="h-28 bg-surface-card-dark rounded-lg animate-pulse" />
          </div>
        </div>
      </div>
    )
  }

  if (!results || !results.success) {
    return (
      <div className="space-y-lg animate-fade-in">
        <div className="card-dark p-lg border-2 border-trading-down bg-trading-down bg-opacity-5">
          <div className="flex items-start gap-lg">
            <div className="text-3xl flex-shrink-0">⚠️</div>
            <div>
              <h2 className="typo-title-lg text-trading-down font-bold mb-md">
                Analysis Failed
              </h2>
              <p className="typo-body-md text-body">
                Could not analyze the chart. Please verify the image is a valid forex chart and try again.
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const zones = [
    ...(results.support_zones || []),
    ...(results.resistance_zones || []),
  ]

  return (
    <div className="space-y-section animate-fade-in">
      {/* Trend Badge */}
      {results.trend && (
        <TrendBadge
          trend={results.trend as 'bullish' | 'bearish' | 'consolidating'}
          confidence={results.trend_confidence || 0}
        />
      )}

      {/* Support & Resistance Zones */}
      {zones.length > 0 && (
        <div>
          <div className="mb-lg">
            <h3 className="typo-title-md text-primary font-bold uppercase tracking-wide">
              📍 Support & Resistance Zones
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-lg">
            {zones.map((zone, idx) => (
              <ZoneCard key={idx} zone={zone} />
            ))}
          </div>
        </div>
      )}

      {/* Chart Patterns */}
      {results.patterns_detected && results.patterns_detected.length > 0 && (
        <div className="card-dark p-lg border-2 border-primary border-opacity-30">
          <h3 className="typo-title-md text-primary font-bold uppercase tracking-wide mb-lg">
            🔍 Patterns Detected
          </h3>
          <div className="flex flex-wrap gap-md">
            {results.patterns_detected.map((pattern, idx) => (
              <span
                key={idx}
                className="px-lg py-md bg-primary text-on-primary rounded-pill typo-button font-bold transition-transform hover:scale-105"
              >
                {pattern}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Trade Scenarios */}
      {results.scenarios && results.scenarios.length > 0 && (
        <div>
          <div className="mb-lg">
            <h3 className="typo-title-md text-primary font-bold uppercase tracking-wide">
              💡 Trade Scenarios
            </h3>
          </div>
          <div className="space-y-lg">
            {results.scenarios.map((scenario, idx) => (
              <TradeIdeaCard key={idx} scenario={scenario} index={idx + 1} />
            ))}
          </div>
        </div>
      )}

      {/* Mentor Explanation */}
      {results.mentor_explanation && (
        <MentorExplanation
          explanation={results.mentor_explanation}
          pair={results.pair}
          timeframe={results.timeframe}
        />
      )}

      {/* Disclaimers - Critical */}
      <Disclaimers />

      {/* Analysis Metadata Footer */}
      {results.analysis_id && (
        <div className="pt-lg mt-lg border-t border-hairline-dark text-center">
          <p className="typo-caption text-muted">
            📊 Analysis ID: <code className="font-plex text-xs">{results.analysis_id}</code>
          </p>
          {results.timestamp && (
            <p className="typo-caption text-muted mt-xs">
              {new Date(results.timestamp).toLocaleString()}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
