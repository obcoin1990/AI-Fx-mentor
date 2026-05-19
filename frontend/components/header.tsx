'use client'

import ThemeToggle from './theme-toggle'
import LanguageSwitcher from './language-switcher'

export default function Header() {
  return (
    <header className="bg-canvas-dark dark:bg-canvas-dark border-b border-hairline-dark sticky top-0 z-50 h-16 flex items-center">
      <div className="w-full max-w-7xl mx-auto px-lg flex justify-between items-center">
        {/* Logo & Branding */}
        <div className="flex items-center gap-2">
          <div className="flex items-baseline gap-1">
            <span className="typo-title-lg text-on-dark font-bold">AI</span>
            <span className="typo-title-lg text-primary font-bold">Chart</span>
            <span className="typo-title-lg text-on-dark font-bold">Mentor</span>
          </div>
          <div className="text-xs typo-caption text-muted ml-3 border-l border-hairline-dark pl-3">
            Forex Analysis AI
          </div>
        </div>
        
        {/* Right Side: Theme & Language Controls */}
        <div className="flex items-center gap-md">
          <LanguageSwitcher />
          <ThemeToggle />
        </div>
      </div>
    </header>
  )
}
