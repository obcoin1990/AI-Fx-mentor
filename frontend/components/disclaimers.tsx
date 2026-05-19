'use client'

import { useState } from 'react'

export default function Disclaimers() {
  const [isAccepted, setIsAccepted] = useState(false)

  return (
    <div className="mb-section">
      {/* Legal Disclaimers Banner */}
      <div className="card-dark p-lg border-2 border-trading-down border-opacity-50 bg-trading-down bg-opacity-5 mb-lg">
        <div className="flex items-start gap-lg">
          <div className="text-3xl flex-shrink-0">⚠️</div>
          <div className="flex-1">
            <h3 className="typo-title-md text-trading-down font-bold mb-md">
              Important Legal Disclaimers
            </h3>
            <ul className="space-y-md">
              <li className="flex gap-md">
                <span className="text-trading-down flex-shrink-0 mt-xs">•</span>
                <div>
                  <p className="typo-body-md text-body">
                    <strong className="text-on-dark">Educational Analysis Only:</strong>
                    {' '}This tool provides educational analysis of forex charts.
                    It is <strong>NOT</strong> financial advice.
                  </p>
                </div>
              </li>
              <li className="flex gap-md">
                <span className="text-trading-down flex-shrink-0 mt-xs">•</span>
                <div>
                  <p className="typo-body-md text-body">
                    <strong className="text-on-dark">Do Not Trade Solely Based on This Tool:</strong>
                    {' '}Always conduct your own research and consult with a licensed financial advisor.
                  </p>
                </div>
              </li>
              <li className="flex gap-md">
                <span className="text-trading-down flex-shrink-0 mt-xs">•</span>
                <div>
                  <p className="typo-body-md text-body">
                    <strong className="text-on-dark">No Guarantees:</strong>
                    {' '}Past patterns do not guarantee future results. Trading forex carries substantial risk of loss.
                  </p>
                </div>
              </li>
              <li className="flex gap-md">
                <span className="text-trading-down flex-shrink-0 mt-xs">•</span>
                <div>
                  <p className="typo-body-md text-body">
                    <strong className="text-on-dark">Confidence Limits:</strong>
                    {' '}Confidence scores are capped at 65% to prevent overconfidence.
                  </p>
                </div>
              </li>
              <li className="flex gap-md">
                <span className="text-trading-down flex-shrink-0 mt-xs">•</span>
                <div>
                  <p className="typo-body-md text-body">
                    <strong className="text-on-dark">Volatile Markets:</strong>
                    {' '}Analysis may fail during high volatility or gap-prone conditions.
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Acceptance Checkbox */}
      <div className="flex items-start gap-md p-md bg-surface-card-dark rounded-lg border border-hairline-dark">
        <input
          type="checkbox"
          id="disclaimer-accept"
          checked={isAccepted}
          onChange={(e) => setIsAccepted(e.target.checked)}
          className="mt-xs w-4 h-4 accent-primary rounded cursor-pointer"
        />
        <label htmlFor="disclaimer-accept" className="typo-body-md text-body cursor-pointer flex-1">
          I acknowledge the disclaimers above. I understand this is educational analysis only,
          <strong className="text-primary"> not financial advice</strong>, and I trade at my own risk.
        </label>
      </div>

      {/* Success Message */}
      {isAccepted && (
        <div className="mt-lg p-lg bg-trading-up bg-opacity-10 border border-trading-up rounded-lg animate-fade-in">
          <p className="typo-body-md text-trading-up font-bold flex items-center gap-md">
            <span>✓</span> You can now analyze charts. Trade responsibly!
          </p>
        </div>
      )}

      {/* Footer Note */}
      <div className="mt-lg pt-lg border-t border-hairline-dark">
        <p className="typo-caption text-muted text-center">
          This analysis is provided as-is for educational purposes. The creators assume no liability for trading losses.
        </p>
      </div>
    </div>
  )
}
