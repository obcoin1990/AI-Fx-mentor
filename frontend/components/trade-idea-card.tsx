'use client'

import React from 'react'

interface TradeScenario {
  direction: 'bullish' | 'bearish'
  entry_price: number
  stop_loss: number
  take_profit: number
  risk_reward_ratio: number
  confidence_score: number
}

interface TradeIdeaCardProps {
  scenario: TradeScenario
  index?: number
}

export default function TradeIdeaCard({ scenario, index = 1 }: TradeIdeaCardProps) {
  const getDirectionColor = (direction: string) => {
    return direction === 'bullish'
      ? 'bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 border-green-200 dark:border-green-800'
      : 'bg-gradient-to-r from-red-50 to-rose-50 dark:from-red-900/30 dark:to-rose-900/30 border-red-200 dark:border-red-800'
  }

  const getDirectionLabel = (direction: string) => {
    return direction === 'bullish' ? 'Buy' : 'Sell'
  }

  const getDirectionTextColor = (direction: string) => {
    return direction === 'bullish'
      ? 'text-green-700 dark:text-green-300'
      : 'text-red-700 dark:text-red-300'
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence < 30) return 'text-red-600 dark:text-red-400'
    if (confidence < 50) return 'text-orange-600 dark:text-orange-400'
    return 'text-green-600 dark:text-green-400'
  }

  const getConfidenceLabel = (confidence: number) => {
    if (confidence < 50) return '⚠️ Low Confidence - Unreliable'
    return 'Moderate Confidence'
  }

  const getConfidenceLabelClass = (confidence: number) => {
    if (confidence < 50) return 'text-orange-600 dark:text-orange-400'
    return 'text-slate-600 dark:text-slate-400'
  }

  return (
    <div className={`rounded-lg border p-5 ${getDirectionColor(scenario.direction)}`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">
            Trade Scenario {index}
          </p>
          <p className={`text-2xl font-bold ${getDirectionTextColor(scenario.direction)}`}>
            {getDirectionLabel(scenario.direction)}
          </p>
        </div>
        <div className="text-right">
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">
            Confidence
          </p>
          <p className={`text-xl font-bold ${getConfidenceColor(scenario.confidence_score)}`}>
            {scenario.confidence_score.toFixed(0)}%
          </p>
        </div>
      </div>

      {scenario.confidence_score < 50 && (
        <div className="mb-3 p-2 bg-orange-100 dark:bg-orange-900/40 rounded border border-orange-200 dark:border-orange-800">
          <p className={`text-xs font-medium ${getConfidenceLabelClass(scenario.confidence_score)}`}>
            {getConfidenceLabel(scenario.confidence_score)}
          </p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 mb-4">
        <div>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Entry</p>
          <p className="font-mono text-sm font-bold text-slate-900 dark:text-white">
            {scenario.entry_price.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Stop Loss</p>
          <p className="font-mono text-sm font-bold text-red-600 dark:text-red-400">
            {scenario.stop_loss.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Take Profit</p>
          <p className="font-mono text-sm font-bold text-green-600 dark:text-green-400">
            {scenario.take_profit.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">R:R Ratio</p>
          <p className="font-mono text-sm font-bold text-slate-900 dark:text-white">
            1:{scenario.risk_reward_ratio.toFixed(1)}
          </p>
        </div>
      </div>

      <div className="pt-3 border-t border-slate-200 dark:border-slate-700">
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Potential Risk: 1 unit | Potential Reward: {scenario.risk_reward_ratio.toFixed(1)} units
        </p>
      </div>
    </div>
  )
}
