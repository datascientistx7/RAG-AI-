import "./globals.css"
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import { FileText, MessageSquare, Home } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'RAG AI Assistant',
  description: 'AI document querying system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} flex h-screen bg-slate-950 text-slate-50`}>
        <aside className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 hidden md:flex flex-col gap-4">
          <div className="font-bold text-xl mb-8 tracking-tight bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            RAG AI App
          </div>
          <nav className="flex flex-col gap-2">
            <Link href="/" className="flex flex-row items-center gap-2 p-2 rounded-md hover:bg-slate-800 transition-colors">
              <Home size={18} /> Home
            </Link>
            <Link href="/chat" className="flex flex-row items-center gap-2 p-2 rounded-md hover:bg-slate-800 transition-colors">
              <MessageSquare size={18} /> Chat
            </Link>
            <Link href="/documents" className="flex flex-row items-center gap-2 p-2 rounded-md hover:bg-slate-800 transition-colors">
              <FileText size={18} /> Documents
            </Link>
          </nav>
        </aside>
        <main className="flex-1 flex flex-col h-screen overflow-hidden">
          {children}
        </main>
      </body>
    </html>
  )
}
