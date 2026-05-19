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
        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all cursor-pointer ${
          isDragActive
            ? 'border-primary bg-surface-elevated-dark shadow-lg scale-105'
            : 'border-hairline-dark hover:border-primary bg-surface-card-dark hover:bg-surface-elevated-dark'
        }`}
        onClick={() => fileInputRef.current?.click()}
      >
        {!preview ? (
          <>
            <div className="text-6xl mb-lg">📈</div>
            <h2 className="typo-title-lg text-on-dark mb-md">
              Upload Your Forex Chart
            </h2>
            <p className="typo-body-md text-muted mb-lg">
              Drag and drop your chart image (PNG or JPG), or click to select
            </p>
            <div className="text-xs typo-caption text-muted-strong">
              Minimum 200×200px • Maximum 5MB • PNG, JPG supported
            </div>
          </>
        ) : (
          <>
            <div className="mb-lg">
              <img
                src={preview}
                alt="Preview"
                className="max-h-96 mx-auto rounded-lg border border-hairline-dark"
              />
            </div>
            <p className="typo-body-md text-muted">
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

      {/* Error Message */}
      {error && (
        <div className="mt-lg p-md bg-trading-down bg-opacity-10 border border-trading-down rounded-lg">
          <p className="typo-body-sm text-trading-down font-medium">{error}</p>
        </div>
      )}

      {/* Mobile Camera Upload */}
      <div className="mt-xl text-center">
        <label className="inline-flex items-center gap-xs cursor-pointer group">
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
          <span className="typo-nav-link text-muted group-hover:text-primary transition-colors">
            📷 Take a photo with your camera
          </span>
        </label>
      </div>
    </div>
  )
}
