"use client"
import { motion } from "framer-motion"
import Link from "next/link"
import { FileUp, MessageCircle } from "lucide-react"

export default function HomePage() {
  return (
    <div className="flex-1 overflow-y-auto p-8 flex items-center justify-center relative">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#0a0a0a] to-black -z-10" />
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-2xl text-center space-y-8"
      >
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight">
          Interact with your <br/>
          <span className="bg-gradient-to-r from-blue-500 to-indigo-500 bg-clip-text text-transparent">Documents</span> 
          Using AI.
        </h1>
        <p className="text-lg text-slate-400">
          A secure, high-performance RAG-based AI application that lets you upload your PDFs and instantly retrieve answers with accurate citations.
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/documents" className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium flex items-center gap-2 shadow-lg shadow-blue-900/20 transition-all">
            <FileUp size={20} />
            Upload PDF
          </Link>
          <Link href="/chat" className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-medium flex items-center gap-2 transition-all">
            <MessageCircle size={20} />
            Start Chat
          </Link>
        </div>
      </motion.div>
    </div>
  )
}
