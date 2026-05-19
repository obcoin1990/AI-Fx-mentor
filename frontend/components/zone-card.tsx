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
  const getZoneColor = (type: string) => {
    return type === 'support'
      ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
      : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
  }

  const getZoneLabel = (type: string) => {
    return type === 'support' ? 'Support' : 'Resistance'
  }

  const getStrengthColor = (strength?: string) => {
    switch (strength) {
      case 'weak':
        return 'text-yellow-600 dark:text-yellow-400'
      case 'moderate':
        return 'text-orange-600 dark:text-orange-400'
      case 'strong':
        return 'text-green-600 dark:text-green-400'
      default:
        return 'text-slate-600 dark:text-slate-400'
    }
  }

  const getStrengthLabel = (strength?: string) => {
    return strength ? strength.charAt(0).toUpperCase() + strength.slice(1) : 'Moderate'
  }

  return (
    <div className={`rounded-lg border p-4 ${getZoneColor(zone.zone_type)}`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-slate-900 dark:text-white">
          {getZoneLabel(zone.zone_type)}
        </h3>
        <span className={`text-xs font-medium ${getStrengthColor(zone.strength)}`}>
          {getStrengthLabel(zone.strength)}
        </span>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-600 dark:text-slate-400">Price Level</span>
          <span className="font-mono font-bold text-slate-900 dark:text-white">
            {zone.price_level.toFixed(4)}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-600 dark:text-slate-400">Touches</span>
          <span className="font-semibold text-slate-900 dark:text-white">
            {zone.touch_count}
          </span>
        </div>
      </div>
    </div>
  )
}
