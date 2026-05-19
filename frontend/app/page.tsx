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
    <div className="min-h-screen bg-white dark:bg-slate-950">
      <Header />

      <div className="container mx-auto px-4 py-8">
        <Disclaimers />

        <div className="max-w-2xl mx-auto">
          {!results && !loading && (
            <UploadBox onUpload={handleImageUpload} />
          )}

          {loading && (
            <div className="space-y-4">
              <div className="flex justify-center items-center py-16">
                <div className="text-center">
                  <div className="inline-block animate-spin mb-4">
                    <div className="h-12 w-12 rounded-full border-4 border-slate-300 dark:border-slate-600 border-t-blue-500"></div>
                  </div>
                  <p className="text-slate-600 dark:text-slate-400 font-medium mb-3">
                    Analyzing your chart...
                  </p>
                  {uploadProgress > 0 && uploadProgress < 100 && (
                    <div className="w-48 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden mx-auto">
                      <div
                        className="h-full bg-blue-500 transition-all"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                  )}
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
                    Step 1: Extracting chart features...
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                    Step 2: Generating trade scenarios...
                  </p>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900 rounded-lg p-4 mb-4">
              <h3 className="font-semibold text-red-900 dark:text-red-100 mb-2">
                ⚠️ Analysis Failed
              </h3>
              <p className="text-red-700 dark:text-red-200 mb-3">{error}</p>
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm font-medium"
              >
                Try Again
              </button>
            </div>
          )}

          {results && !loading && (
            <>
              <ResultDisplay results={results} />
              <button
                onClick={handleReset}
                className="mt-8 w-full px-4 py-3 bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100 rounded-lg hover:bg-slate-300 dark:hover:bg-slate-600 font-medium transition-colors"
              >
                Analyze Another Chart
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
