'use client'

import { useState } from 'react'
import UploadBox from '@/components/upload-box'
import ResultDisplay from '@/components/result-display'
import Header from '@/components/header'
import Disclaimers from '@/components/disclaimers'
import { uploadChart, generateScenarios, VisionAnalysisResult, AnalysisResult } from '@/lib/api'

export default function Home() {
  const [uploadedImage, setUploadedImage] = useState<File | null>(null)
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)

  const handleImageUpload = async (file: File) => {
    setUploadedImage(file)
    setLoading(true)
    setError(null)
    setUploadProgress(0)

    try {
      // Step 1: Vision API - Analyze chart
      const visionResult = await uploadChart(
        file,
        undefined,
        undefined,
        (percent) => setUploadProgress(percent)
      )

      if (!visionResult.success) {
        throw new Error('Vision analysis failed')
      }

      // Step 2: Reasoning API - Generate scenarios
      const reasoningResult = await generateScenarios(
        visionResult,
        visionResult.pair,
        visionResult.timeframe
      )

      // Combine vision and reasoning results
      const combinedResults: AnalysisResult = {
        ...visionResult,
        scenarios: reasoningResult.scenarios,
        mentor_explanation: reasoningResult.mentor_explanation,
        overall_confidence: reasoningResult.overall_confidence,
      }

      setResults(combinedResults)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to analyze chart'
      setError(errorMessage)
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
      setUploadProgress(0)
    }
  }

  const handleReset = () => {
    setUploadedImage(null)
    setResults(null)
    setError(null)
    setUploadProgress(0)
  }

  return (
    <div className="min-h-screen bg-canvas-dark text-body">
      <Header />

      <div className="w-full max-w-7xl mx-auto px-lg py-section">
        {/* Initial Disclaimers */}
        {!results && !loading && <Disclaimers />}

        <div className="max-w-3xl mx-auto">
          {/* Upload Section */}
          {!results && !loading && (
            <div className="animate-fade-in">
              <UploadBox onUpload={handleImageUpload} />
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="animate-fade-in">
              <div className="card-elevated p-section text-center">
                <div className="inline-flex items-center justify-center mb-lg">
                  <div className="relative w-16 h-16">
                    <div className="absolute inset-0 rounded-full border-4 border-hairline-dark animate-spin border-t-primary" />
                    <div className="absolute inset-0 flex items-center justify-center text-2xl">
                      📊
                    </div>
                  </div>
                </div>

                <h3 className="typo-title-lg text-on-dark font-bold mb-md">
                  Analyzing Your Chart
                </h3>
                <p className="typo-body-md text-muted mb-lg">
                  Our AI is extracting trends, support/resistance zones, and generating trade scenarios...
                </p>

                {/* Progress Bar */}
                {uploadProgress > 0 && uploadProgress < 100 && (
                  <div className="mb-lg">
                    <div className="w-full h-2 bg-surface-card-dark rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                    <p className="typo-caption text-muted mt-md">
                      {uploadProgress}% Complete
                    </p>
                  </div>
                )}

                {/* Steps */}
                <div className="space-y-md pt-lg border-t border-hairline-dark">
                  <div className="flex items-center gap-md">
                    <div className="w-6 h-6 rounded-full bg-primary text-on-primary flex items-center justify-center typo-caption font-bold">
                      ✓
                    </div>
                    <p className="typo-body-sm text-muted">Vision API: Extracting chart features</p>
                  </div>
                  <div className="flex items-center gap-md">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center typo-caption font-bold ${
                      uploadProgress > 50 
                        ? 'bg-primary text-on-primary' 
                        : 'bg-surface-card-dark text-muted animate-pulse'
                    }`}>
                      {uploadProgress > 50 ? '✓' : '2'}
                    </div>
                    <p className="typo-body-sm text-muted">Reasoning API: Generating scenarios</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="card-dark p-lg border-2 border-trading-down bg-trading-down bg-opacity-5 animate-fade-in">
              <div className="flex items-start gap-lg mb-lg">
                <div className="text-3xl flex-shrink-0">⚠️</div>
                <div className="flex-1">
                  <h3 className="typo-title-lg text-trading-down font-bold mb-md">
                    Analysis Failed
                  </h3>
                  <p className="typo-body-md text-body mb-lg">
                    {error}
                  </p>
                  <button
                    onClick={handleReset}
                    className="btn-primary"
                  >
                    Try Another Chart
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Results Section */}
          {results && !loading && (
            <div className="animate-fade-in space-y-section">
              <ResultDisplay results={results} />

              {/* Action Button */}
              <button
                onClick={handleReset}
                className="w-full btn-secondary-dark py-lg typo-button font-bold text-on-dark text-lg"
              >
                ↻ Analyze Another Chart
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-surface-card-dark border-t border-hairline-dark mt-section">
        <div className="w-full max-w-7xl mx-auto px-lg py-lg">
          <p className="typo-body-sm text-muted text-center">
            AI Chart Mentor © 2025 • Educational Analysis Only • Not Financial Advice
          </p>
        </div>
      </footer>
    </div>
  )
}
