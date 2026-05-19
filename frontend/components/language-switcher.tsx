'use client'

import { useEffect, useState } from 'react'

const LANGUAGES = {
  en: { label: 'English', flag: '🇬🇧' },
  ar: { label: 'العربية', flag: '🇸🇦', dir: 'rtl' },
  zh: { label: '中文', flag: '🇨🇳' },
}

export default function LanguageSwitcher() {
  const [currentLang, setCurrentLang] = useState('en')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const savedLang = localStorage.getItem('language') || 'en'
    setCurrentLang(savedLang)
    applyLanguage(savedLang)
  }, [])

  const applyLanguage = (lang: string) => {
    const langConfig = LANGUAGES[lang as keyof typeof LANGUAGES]
    if (langConfig) {
      document.documentElement.lang = lang
      document.documentElement.dir = (langConfig as any).dir || 'ltr'
      localStorage.setItem('language', lang)
    }
  }

  const handleLanguageChange = (lang: string) => {
    setCurrentLang(lang)
    applyLanguage(lang)
  }

  if (!mounted) return null

  return (
    <div className="relative group">
      <button className="px-lg py-md rounded-lg bg-surface-card-dark hover:bg-surface-elevated-dark text-primary transition-colors flex items-center gap-xs group-hover:shadow-lg">
        <span className="text-lg">{LANGUAGES[currentLang as keyof typeof LANGUAGES].flag}</span>
        <span className="typo-caption font-bold text-primary">{currentLang.toUpperCase()}</span>
      </button>

      <div className="absolute right-0 mt-md w-48 bg-surface-card-dark border border-hairline-dark rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
        {Object.entries(LANGUAGES).map(([code, { label, flag }]) => (
          <button
            key={code}
            onClick={() => handleLanguageChange(code)}
            className={`w-full text-left px-lg py-md hover:bg-surface-elevated-dark flex items-center gap-md typo-nav-link transition-colors ${
              currentLang === code ? 'bg-surface-elevated-dark text-primary' : 'text-body'
            }`}
          >
            <span className="text-lg">{flag}</span>
            <span>{label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
