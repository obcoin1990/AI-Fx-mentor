'use client'

import { useState } from 'react'

export default function Disclaimers() {
  const [isAccepted, setIsAccepted] = useState(false)

  return (
    <div className="mb-8">
      {/* Legal Disclaimers - QUALITY-01, QUALITY-02 */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500 dark:border-yellow-600 rounded p-4 mb-6">
        <h3 className="font-bold text-yellow-900 dark:text-yellow-200 mb-3">
          ⚠️ Important Disclaimers
        </h3>
        <ul className="space-y-2 text-sm text-yellow-800 dark:text-yellow-100">
          <li>
            <strong>Educational Analysis Only:</strong> This tool provides educational analysis
            of forex charts. It is NOT financial advice, and should not be construed as such.
          </li>
          <li>
            <strong>Do Not Trade Based Solely on This Tool:</strong> Always conduct your own research,
            consult with a licensed financial advisor, and consider multiple sources of analysis
            before making trading decisions.
          </li>
          <li>
            <strong>No Guarantees:</strong> Past patterns do not guarantee future results. Trading
            forex carries substantial risk of loss.
          </li>
          <li>
            <strong>Confidence Limits:</strong> Analysis confidence scores are capped at 65% to
            prevent overconfidence. No analysis should be treated as highly reliable.
          </li>
          <li>
            <strong>Unstable Markets:</strong> Analysis may fail in highly volatile or gap-prone
            markets. Watch for unusual market conditions.
          </li>
        </ul>
      </div>

      {/* Acceptance Checkbox */}
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          id="disclaimer-accept"
          checked={isAccepted}
          onChange={(e) => setIsAccepted(e.target.checked)}
          className="mt-1"
        />
        <label htmlFor="disclaimer-accept" className="text-sm text-slate-600 dark:text-slate-400">
          I acknowledge and accept the disclaimers above. I understand this is educational
          analysis only and not financial advice.
        </label>
      </div>

      {isAccepted && (
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded text-sm text-blue-700 dark:text-blue-200">
          ✓ You can now analyze charts. Remember: trade responsibly!
        </div>
      )}
    </div>
  )
}
