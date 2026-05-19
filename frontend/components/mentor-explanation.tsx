'use client'

import React from 'react'

interface MentorExplanationProps {
  explanation: string
  pair?: string
  timeframe?: string
}

export default function MentorExplanation({
  explanation,
  pair,
  timeframe,
}: MentorExplanationProps) {
  return (
    <div className="rounded-lg border border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 p-5">
      <div className="flex items-start gap-3">
        <div className="text-2xl flex-shrink-0">👨‍🏫</div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
            Mentor Analysis
          </h3>
          <p className="text-slate-700 dark:text-slate-300 text-sm leading-relaxed mb-3">
            {explanation}
          </p>

          {(pair || timeframe) && (
            <div className="text-xs text-slate-500 dark:text-slate-400 space-y-1 pt-3 border-t border-blue-200 dark:border-blue-800">
              {pair && (
                <p>
                  <span className="font-medium">Pair:</span> {pair}
                </p>
              )}
              {timeframe && (
                <p>
                  <span className="font-medium">Timeframe:</span> {timeframe}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
