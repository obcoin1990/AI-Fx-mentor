import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bullish: '#10b981',
        bearish: '#ef4444',
        neutral: '#6b7280',
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}
export default config
