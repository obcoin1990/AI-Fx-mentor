'use client'

import React from 'react'

interface Zone {
  zone_type: 'support' | 'resistance'
  price_level: number
  touch_count: number
  strength?: 'weak' | 'moderate' | 'strong'
}

interface ZoneCardProps {
  zone: Zone
}

export default function ZoneCard({ zone }: ZoneCardProps) {
  const isSupport = zone.zone_type === 'support'
  const zoneColor = isSupport ? 'trading-up' : 'trading-down'
  const zoneLabel = isSupport ? 'Support' : 'Resistance'

  const getStrengthConfig = (strength?: string) => {
    switch (strength) {
      case 'weak':
        return { label: 'Weak', indicator: '●', color: 'text-muted' }
      case 'moderate':
        return { label: 'Moderate', indicator: '●●', color: 'text-primary' }
      case 'strong':
        return { label: 'Strong', indicator: '●●●', color: `text-${zoneColor}` }
      default:
        return { label: 'Moderate', indicator: '●●', color: 'text-primary' }
    }
  }

  const strength = getStrengthConfig(zone.strength)

  return (
    <div className={`card-dark p-lg border-2 border-${zoneColor} border-opacity-30`}>
      {/* Header: Label & Strength */}
      <div className="flex items-center justify-between mb-lg">
        <div className="flex items-center gap-md">
          <div className={`w-3 h-3 rounded-full bg-${zoneColor}`} />
          <h3 className="typo-title-md text-on-dark font-bold">
            {zoneLabel}
          </h3>
        </div>
        <div className="flex items-center gap-xs">
          <span className={strength.color}>{strength.indicator}</span>
          <span className="typo-caption text-muted-strong">
            {strength.label}
          </span>
        </div>
      </div>

      {/* Zone Details */}
      <div className="space-y-md">
        {/* Price Level */}
        <div className="flex items-center justify-between pb-md border-b border-hairline-dark">
          <span className="typo-body-sm text-muted">Price Level</span>
          <span className="typo-number-md text-on-dark font-bold font-plex">
            {zone.price_level.toFixed(4)}
          </span>
        </div>

        {/* Touch Count */}
        <div className="flex items-center justify-between">
          <span className="typo-body-sm text-muted">Touched {zone.touch_count}x</span>
          <div className="flex gap-xs">
            {Array.from({ length: Math.min(zone.touch_count, 5) }).map((_, i) => (
              <div
                key={i}
                className={`w-2 h-2 rounded-full bg-${zoneColor}`}
              />
            ))}
            {zone.touch_count > 5 && (
              <span className="typo-caption text-muted">+{zone.touch_count - 5}</span>
            )}
          </div>
        </div>
      </div>

      {/* Confidence Note */}
      <div className="mt-lg pt-md border-t border-hairline-dark">
        <p className="typo-caption text-muted">
          {isSupport ? '↑' : '↓'} Zone identified from {zone.touch_count} price touches
        </p>
      </div>
    </div>
  )
}
