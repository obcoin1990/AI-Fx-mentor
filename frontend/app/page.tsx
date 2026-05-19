'use client'

import { useState } from 'react'
import UploadBox from '@/components/upload-box'
import ResultDisplay from '@/components/result-display'
import Header from '@/components/header'
import Disclaimers from '@/components/disclaimers'

export default function Home() {
  const [uploadedImage, setUploadedImage] = useState<File | null>(null)
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleImageUpload = async (file: File) => {
    setUploadedImage(file)
    setLoading(true)
    setError(null)

    try {
      // TODO: Implement API call to backend
      // const response = await uploadChart(file)
      // setResults(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze chart')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setUploadedImage(null)
    setResults(null)
    setError(null)
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
            <div className="flex justify-center items-center py-16">
              <div className="animate-spin">
                <div className="h-12 w-12 rounded-full border-4 border-slate-300 dark:border-slate-600 border-t-blue-500"></div>
              </div>
              <span className="ml-4 text-slate-600 dark:text-slate-400">Analyzing chart...</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900 rounded-lg p-4 mb-4">
              <p className="text-red-700 dark:text-red-200">{error}</p>
              <button
                onClick={handleReset}
                className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
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
                className="mt-8 w-full px-4 py-3 bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100 rounded-lg hover:bg-slate-300 dark:hover:bg-slate-600 font-medium"
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
