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
      <div className="space-y-6 animate-fade-in">
        <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Analyzing Chart...
          </h2>
          <div className="space-y-4">
            <div className="h-24 bg-slate-200 dark:bg-slate-600 rounded animate-pulse" />
            <div className="h-32 bg-slate-200 dark:bg-slate-600 rounded animate-pulse" />
            <div className="h-40 bg-slate-200 dark:bg-slate-600 rounded animate-pulse" />
          </div>
        </div>
      </div>
    )
  }

  if (!results || !results.success) {
    return (
      <div className="space-y-6 animate-fade-in">
        <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 border border-red-200 dark:border-red-800">
          <h2 className="text-xl font-bold text-red-900 dark:text-red-200 mb-2">
            ⚠️ Analysis Failed
          </h2>
          <p className="text-red-700 dark:text-red-300">
            Could not analyze the chart. Please try again with a different image.
          </p>
        </div>
      </div>
    )
  }

  const zones = [
    ...(results.support_zones || []),
    ...(results.resistance_zones || []),
  ]

  return (
    <div className="space-y-6 animate-fade-in">
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
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 uppercase tracking-wide">
            Support & Resistance Zones
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {zones.map((zone, idx) => (
              <ZoneCard key={idx} zone={zone} />
            ))}
          </div>
        </div>
      )}

      {/* Chart Patterns */}
      {results.patterns_detected && results.patterns_detected.length > 0 && (
        <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800 p-4">
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 uppercase tracking-wide">
            Patterns Detected
          </h3>
          <div className="flex flex-wrap gap-2">
            {results.patterns_detected.map((pattern, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-white dark:bg-slate-700 rounded-full text-xs font-medium text-slate-700 dark:text-slate-300 border border-purple-200 dark:border-purple-700"
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
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 uppercase tracking-wide">
            Trade Scenarios
          </h3>
          <div className="space-y-3">
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

      {/* Disclaimers */}
      <Disclaimers />

      {/* Analysis Metadata */}
      {results.analysis_id && (
        <div className="text-xs text-slate-500 dark:text-slate-400 pt-4 border-t border-slate-200 dark:border-slate-700">
          <p>Analysis ID: {results.analysis_id}</p>
          {results.timestamp && (
            <p>
              Time: {new Date(results.timestamp).toLocaleString()}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
