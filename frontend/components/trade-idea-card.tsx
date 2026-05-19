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
  const isBullish = scenario.direction === 'bullish'
  const directionColor = isBullish ? 'trading-up' : 'trading-down'
  const directionLabel = isBullish ? 'BUY' : 'SELL'
  const confidenceCapped = Math.min(scenario.confidence_score, 65)
  const isLowConfidence = confidenceCapped < 50

  return (
    <div className="card-elevated p-lg border-2 border-hairline-dark">
      {/* Header: Scenario Number & Direction Badge */}
      <div className="flex items-center justify-between mb-lg">
        <div className="flex items-center gap-md">
          <span className="typo-caption text-muted-strong bg-surface-card-dark px-md py-xs rounded-md">
            Scenario {index}
          </span>
          <button
            className={`btn-trading-${isBullish ? 'up' : 'down'} px-lg py-md rounded-md font-bold typo-button`}
            disabled
          >
            {directionLabel}
          </button>
        </div>
        <div className="text-right">
          <p className="typo-caption text-muted mb-xs">Confidence</p>
          <p className={`typo-number-md text-${directionColor} font-bold`}>
            {confidenceCapped.toFixed(0)}%
          </p>
        </div>
      </div>

      {/* Low Confidence Warning */}
      {isLowConfidence && (
        <div className="mb-lg p-md bg-trading-down bg-opacity-10 border border-trading-down rounded-lg">
          <p className="typo-body-sm text-trading-down font-medium">
            ⚠️ Low Confidence ({confidenceCapped.toFixed(0)}%) - Analysis may be unreliable
          </p>
        </div>
      )}

      {/* Trade Levels Grid */}
      <div className="grid grid-cols-2 gap-lg mb-lg">
        {/* Entry Price */}
        <div className="p-md bg-surface-card-dark rounded-lg border border-hairline-dark">
          <p className="typo-caption text-muted mb-xs">Entry</p>
          <p className="typo-number-md text-on-dark font-plex font-bold">
            {scenario.entry_price.toFixed(4)}
          </p>
        </div>

        {/* Stop Loss */}
        <div className="p-md bg-surface-card-dark rounded-lg border border-hairline-dark">
          <p className="typo-caption text-muted mb-xs">Stop Loss</p>
          <p className="typo-number-md text-trading-down font-plex font-bold">
            {scenario.stop_loss.toFixed(4)}
          </p>
        </div>

        {/* Take Profit */}
        <div className="p-md bg-surface-card-dark rounded-lg border border-hairline-dark">
          <p className="typo-caption text-muted mb-xs">Take Profit</p>
          <p className="typo-number-md text-trading-up font-plex font-bold">
            {scenario.take_profit.toFixed(4)}
          </p>
        </div>

        {/* Risk:Reward Ratio */}
        <div className="p-md bg-surface-card-dark rounded-lg border border-hairline-dark">
          <p className="typo-caption text-muted mb-xs">R:R Ratio</p>
          <p className="typo-number-md text-primary font-plex font-bold">
            1:{scenario.risk_reward_ratio.toFixed(1)}
          </p>
        </div>
      </div>

      {/* Risk/Reward Summary */}
      <div className="pt-lg border-t border-hairline-dark">
        <div className="flex items-center justify-between">
          <p className="typo-body-sm text-muted">
            📊 Risk: 1 unit
          </p>
          <p className="typo-body-sm text-primary font-bold">
            Reward: {scenario.risk_reward_ratio.toFixed(1)} units
          </p>
        </div>
      </div>

      {/* Confidence Cap Note */}
      <div className="mt-lg pt-lg border-t border-hairline-dark">
        <p className="typo-caption text-muted-strong text-center">
          Max confidence shown: 65% (capped for safety)
        </p>
      </div>
    </div>
  )
}
