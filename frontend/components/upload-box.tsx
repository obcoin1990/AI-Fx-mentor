'use client'

import { useState, useRef } from 'react'
import { validateImage } from '@/lib/image-validation'

interface UploadBoxProps {
  onUpload: (file: File) => void
}

export default function UploadBox({ onUpload }: UploadBoxProps) {
  const [isDragActive, setIsDragActive] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFile = async (file: File) => {
    setError(null)

    const validation = await validateImage(file)
    if (!validation.valid) {
      setError(validation.error || 'Invalid image')
      return
    }

    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target?.result as string)
    }
    reader.readAsDataURL(file)

    onUpload(file)
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true)
    } else if (e.type === 'dragleave') {
      setIsDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  return (
    <div className="w-full">
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors cursor-pointer ${
          isDragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
            : 'border-slate-300 dark:border-slate-600 hover:border-blue-400 dark:hover:border-blue-400'
        }`}
        onClick={() => fileInputRef.current?.click()}
      >
        {!preview ? (
          <>
            <div className="text-5xl mb-4">📈</div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
              Upload Your Forex Chart
            </h2>
            <p className="text-slate-600 dark:text-slate-400 mb-4">
              Drag and drop your chart image (PNG or JPG), or click to select
            </p>
            <div className="text-sm text-slate-500 dark:text-slate-500">
              Minimum 200x200px • Maximum 5MB
            </div>
          </>
        ) : (
          <>
            <div className="mb-4">
              <img
                src={preview}
                alt="Preview"
                className="max-h-64 mx-auto rounded-lg"
              />
            </div>
            <p className="text-slate-600 dark:text-slate-400">
              Click to select a different chart
            </p>
          </>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg"
          onChange={handleInputChange}
          className="hidden"
          aria-label="Upload chart image"
        />
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900 rounded-lg">
          <p className="text-red-700 dark:text-red-200 text-sm">{error}</p>
        </div>
      )}

      {/* Mobile camera upload */}
      <div className="mt-6 text-center">
        <label className="inline-block cursor-pointer">
          <input
            type="file"
            accept="image/*"
            capture="environment"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                handleFile(e.target.files[0])
              }
            }}
            className="hidden"
            aria-label="Capture chart with camera"
          />
          <span className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm">
            📷 Or take a photo with your camera
          </span>
        </label>
      </div>
    </div>
  )
}
