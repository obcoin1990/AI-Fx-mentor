import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Chart Mentor - Instant Forex Analysis',
  description: 'Get instant, AI-powered analysis of your forex charts with mentor-style guidance and trade scenarios.',
  keywords: ['forex', 'chart analysis', 'trading', 'AI'],
  openGraph: {
    title: 'AI Chart Mentor',
    description: 'Instant forex chart analysis powered by AI',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100">
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
