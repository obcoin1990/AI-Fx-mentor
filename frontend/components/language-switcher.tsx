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
      document.documentElement.dir = langConfig.dir || 'ltr'
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
      <button className="px-3 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors flex items-center gap-2">
        <span>{LANGUAGES[currentLang as keyof typeof LANGUAGES].flag}</span>
        <span className="text-sm">{currentLang.toUpperCase()}</span>
      </button>

      <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
        {Object.entries(LANGUAGES).map(([code, { label, flag }]) => (
          <button
            key={code}
            onClick={() => handleLanguageChange(code)}
            className={`w-full text-left px-4 py-2 hover:bg-slate-100 dark:hover:bg-slate-700 flex items-center gap-2 ${
              currentLang === code ? 'bg-slate-50 dark:bg-slate-700' : ''
            }`}
          >
            <span>{flag}</span>
            <span>{label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
