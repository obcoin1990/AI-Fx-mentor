'use client'

import React from 'react'

interface TrendBadgeProps {
  trend: 'bullish' | 'bearish' | 'consolidating'
  confidence: number
}

export default function TrendBadge({ trend, confidence }: TrendBadgeProps) {
  const getTrendConfig = (t: string) => {
    switch (t) {
      case 'bullish':
        return {
          color: 'trading-up',
          bg: 'bg-trading-up',
          bgAlt: 'bg-opacity-10',
          border: 'border-trading-up',
          label: 'Bullish',
          icon: '↗',
        }
      case 'bearish':
        return {
          color: 'trading-down',
          bg: 'bg-trading-down',
          bgAlt: 'bg-opacity-10',
          border: 'border-trading-down',
          label: 'Bearish',
          icon: '↘',
        }
      case 'consolidating':
        return {
          color: 'accent-turquoise',
          bg: 'bg-accent-turquoise',
          bgAlt: 'bg-opacity-10',
          border: 'border-accent-turquoise',
          label: 'Consolidating',
          icon: '↔',
        }
      default:
        return {
          color: 'muted',
          bg: 'bg-muted',
          bgAlt: 'bg-opacity-10',
          border: 'border-muted',
          label: 'Unknown',
          icon: '•',
        }
    }
  }

  const config = getTrendConfig(trend)

  return (
    <div className={`card-dark p-lg border-2 ${config.border} ${config.bg} ${config.bgAlt}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-lg">
          {/* Icon Bubble */}
          <div className={`w-12 h-12 rounded-lg ${config.bg} flex items-center justify-center text-on-dark text-2xl`}>
            {config.icon}
          </div>
          
          {/* Trend Info */}
          <div>
            <p className="typo-caption text-muted">Market Trend</p>
            <p className={`typo-title-md text-${config.color} font-bold`}>
              {config.label}
            </p>
          </div>
        </div>
        
        {/* Confidence Score */}
        <div className="text-right">
          <p className="typo-caption text-muted">Confidence</p>
          <div className={`typo-number-display text-${config.color} font-bold`}>
            {Math.min(confidence, 65).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Confidence Warning if close to cap */}
      {confidence > 60 && (
        <div className="mt-md pt-md border-t border-hairline-dark">
          <p className="typo-body-sm text-muted-strong">
            ⚠️ High confidence - analysis is reliable but not guaranteed
          </p>
        </div>
      )}
    </div>
  )
}
