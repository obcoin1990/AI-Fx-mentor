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
    <div className="card-dark p-lg border-2 border-info border-opacity-30 bg-info bg-opacity-5">
      {/* Header */}
      <div className="flex items-start gap-lg mb-lg">
        <div className="text-4xl flex-shrink-0">👨‍🏫</div>
        <div className="flex-1">
          <h3 className="typo-title-md text-on-dark font-bold mb-md">
            Mentor's Analysis
          </h3>
          <p className="typo-body-md text-body leading-relaxed">
            {explanation}
          </p>
        </div>
      </div>

      {/* Context Footer */}
      {(pair || timeframe) && (
        <div className="pt-lg mt-lg border-t border-hairline-dark">
          <div className="grid grid-cols-2 gap-lg">
            {pair && (
              <div>
                <p className="typo-caption text-muted mb-xs">Trading Pair</p>
                <p className="typo-body-md text-primary font-bold font-plex">
                  {pair}
                </p>
              </div>
            )}
            {timeframe && (
              <div>
                <p className="typo-caption text-muted mb-xs">Timeframe</p>
                <p className="typo-body-md text-primary font-bold font-plex">
                  {timeframe}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Educational Note */}
      <div className="mt-lg pt-lg border-t border-hairline-dark bg-surface-card-dark bg-opacity-50 rounded-lg p-md">
        <p className="typo-caption text-muted-strong text-center">
          💡 This is educational analysis, not financial advice. Always do your own research.
        </p>
      </div>
    </div>
  )
}
