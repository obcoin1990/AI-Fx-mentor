import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Binance Brand Colors
        primary: '#FCD535',
        'primary-active': '#F0B90B',
        'primary-disabled': '#3A3A1F',
        
        // Text Colors
        ink: '#181A20',
        body: '#EAECEF',
        'body-on-light': '#181A20',
        muted: '#707A8A',
        'muted-strong': '#929AA5',
        
        // Canvas & Surfaces
        'canvas-dark': '#0B0E11',
        'canvas-light': '#FFFFFF',
        'surface-card-dark': '#1E2329',
        'surface-elevated-dark': '#2B3139',
        'surface-soft-light': '#FAFAFA',
        'surface-strong-light': '#F5F5F5',
        
        // Borders & Hairlines
        'hairline-light': '#EAECEF',
        'hairline-dark': '#2B3139',
        'border-strong': '#CDD1D6',
        
        // Semantic Colors
        'on-primary': '#181A20',
        'on-dark': '#FFFFFF',
        'trading-up': '#0ECB81',
        'trading-down': '#F6465D',
        'accent-turquoise': '#2DBDB6',
        'info': '#3B82F6',
        'info-ring': '#3B82F6',
      },
      fontFamily: {
        // Using Inter as substitute for BinanceNova
        nova: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        // Using JetBrains Mono as substitute for BinancePlex
        plex: ['JetBrains Mono', 'IBM Plex Sans', 'monospace'],
      },
      fontSize: {
        // Display Sizes
        'hero-display': ['64px', { lineHeight: '1.1', fontWeight: '700', letterSpacing: '-1px' }],
        'display-lg': ['48px', { lineHeight: '1.1', fontWeight: '700', letterSpacing: '-0.5px' }],
        'display-md': ['40px', { lineHeight: '1.15', fontWeight: '600', letterSpacing: '-0.3px' }],
        'display-sm': ['32px', { lineHeight: '1.2', fontWeight: '600', letterSpacing: '0' }],
        
        // Title Sizes
        'title-lg': ['24px', { lineHeight: '1.3', fontWeight: '600', letterSpacing: '0' }],
        'title-md': ['20px', { lineHeight: '1.35', fontWeight: '600', letterSpacing: '0' }],
        'title-sm': ['16px', { lineHeight: '1.4', fontWeight: '600', letterSpacing: '0' }],
        
        // Number Sizes (BinancePlex)
        'number-display': ['40px', { lineHeight: '1.1', fontWeight: '700', letterSpacing: '-0.3px' }],
        'number-md': ['16px', { lineHeight: '1.4', fontWeight: '500', letterSpacing: '0' }],
        'number-sm': ['14px', { lineHeight: '1.4', fontWeight: '500', letterSpacing: '0' }],
        
        // Body Sizes
        'body-md': ['14px', { lineHeight: '1.5', fontWeight: '400', letterSpacing: '0' }],
        'body-sm': ['13px', { lineHeight: '1.5', fontWeight: '400', letterSpacing: '0' }],
        
        // Utility Sizes
        'caption': ['12px', { lineHeight: '1.4', fontWeight: '500', letterSpacing: '0' }],
        'button': ['14px', { lineHeight: '1', fontWeight: '600', letterSpacing: '0' }],
        'nav-link': ['14px', { lineHeight: '1.4', fontWeight: '500', letterSpacing: '0' }],
      },
      spacing: {
        // 4px base unit
        'xxs': '4px',
        'xs': '8px',
        'sm': '12px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        'xxl': '48px',
        'section': '80px',
      },
      borderRadius: {
        'xs': '2px',
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
        'xl': '12px',
        'pill': '9999px',
      },
      boxShadow: {
        'focus-ring': '0 0 0 2px rgba(59, 130, 246, 0.5)',
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}
export default config
