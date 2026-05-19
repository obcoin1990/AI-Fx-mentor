'use client'

import React from 'react'

interface TrendBadgeProps {
  trend: 'bullish' | 'bearish' | 'consolidating'
  confidence: number
}

export default function TrendBadge({ trend, confidence }: TrendBadgeProps) {
  const getTrendColor = (t: string) => {
    switch (t) {
      case 'bullish':
        return 'bg-green-100 dark:bg-green-900/30 border-green-300 dark:border-green-700'
      case 'bearish':
        return 'bg-red-100 dark:bg-red-900/30 border-red-300 dark:border-red-700'
      case 'consolidating':
        return 'bg-blue-100 dark:bg-blue-900/30 border-blue-300 dark:border-blue-700'
      default:
        return 'bg-slate-100 dark:bg-slate-700 border-slate-300 dark:border-slate-600'
    }
  }

  const getTrendTextColor = (t: string) => {
    switch (t) {
      case 'bullish':
        return 'text-green-800 dark:text-green-200'
      case 'bearish':
        return 'text-red-800 dark:text-red-200'
      case 'consolidating':
        return 'text-blue-800 dark:text-blue-200'
      default:
        return 'text-slate-800 dark:text-slate-200'
    }
  }

  const getTrendIcon = (t: string) => {
    switch (t) {
      case 'bullish':
        return '↗'
      case 'bearish':
        return '↘'
      case 'consolidating':
        return '↔'
      default:
        return '•'
    }
  }

  const getTrendLabel = (t: string) => {
    switch (t) {
      case 'bullish':
        return 'Bullish'
      case 'bearish':
        return 'Bearish'
      case 'consolidating':
        return 'Consolidating'
      default:
        return 'Unknown'
    }
  }

  return (
    <div className={`rounded-lg border p-4 ${getTrendColor(trend)}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{getTrendIcon(trend)}</span>
          <div>
            <p className={`text-sm font-medium ${getTrendTextColor(trend)}`}>
              Market Trend
            </p>
            <p className={`text-xl font-bold ${getTrendTextColor(trend)}`}>
              {getTrendLabel(trend)}
            </p>
          </div>
        </div>
        <div className="text-right">
          <p className={`text-xs font-medium ${getTrendTextColor(trend)}`}>
            Confidence
          </p>
          <p className={`text-lg font-bold ${getTrendTextColor(trend)}`}>
            {confidence.toFixed(0)}%
          </p>
        </div>
      </div>
    </div>
  )
}
