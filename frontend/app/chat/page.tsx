"use client"
import { useState } from "react"
import { motion } from "framer-motion"
import { Send, Bot, User, Copy } from "lucide-react"
import ReactMarkdown from "react-markdown"

type Message = {
  role: string;
  content: string;
  sources?: string[];
}


export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello! Upload some PDFs in the documents tab, then ask me anything about them." }
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMsg = input.trim()
    setInput("")
    setMessages((prev: Message[]) => [...prev, { role: "user", content: userMsg }])
    setLoading(true)

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg })
      })
      const data = await res.json()
      if (res.ok) {
        setMessages((prev: Message[]) => [
          ...prev,
          { role: "assistant", content: data.answer, sources: data.sources }
        ])
      } else {
        setMessages((prev: Message[]) => [
          ...prev,
          { role: "assistant", content: data.detail || "Query failed." }
        ])
      }
    } catch (err) {
      setMessages((prev: Message[]) => [...prev, { role: "assistant", content: "Error connecting to backend." }])
    }
    setLoading(false)
  }

  return (
    <div className="flex-1 flex flex-col h-full items-center p-4">
      <div className="flex-1 w-full max-w-4xl overflow-y-auto space-y-6 pb-20 pr-4">
        {messages.map((m: Message, i: number) => (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            key={i} 
            className={`flex gap-4 group ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {m.role === 'assistant' && <div className="w-8 h-8 rounded-full bg-blue-600/20 text-blue-500 flex items-center justify-center shrink-0 border border-blue-500/20"><Bot size={18} /></div>}
            
            <div className={`p-4 rounded-xl max-w-[80%] ${m.role === 'user' ? 'bg-slate-800 text-white rounded-tr-sm' : 'bg-slate-900/80 border border-slate-800/50 text-slate-200 rounded-tl-sm'}`}>
              <div className="flex justify-between items-start gap-4">
                <div className="prose prose-invert max-w-none text-sm leading-relaxed">
                  <ReactMarkdown>{m.content}</ReactMarkdown>
                </div>
                <button 
                  onClick={() => navigator.clipboard.writeText(m.content)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-slate-700/50 rounded transition-all shrink-0 h-fit"
                  title="Copy to clipboard"
                >
                  <Copy size={14} className="text-slate-400" />
                </button>
              </div>
              {m.sources && m.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-700/50">
                  <p className="text-xs text-slate-500 font-semibold mb-1">Sources</p>
                  <div className="flex flex-wrap gap-2">
                    {m.sources.map((s: string, idx: number) => (
                      <span key={idx} className="bg-slate-800/50 px-2 py-1 rounded text-xs text-slate-400">{s}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {m.role === 'user' && <div className="w-8 h-8 rounded-full bg-slate-700 text-slate-300 flex items-center justify-center shrink-0"><User size={18} /></div>}
          </motion.div>
        ))}
        {loading && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-blue-600/20 text-blue-500 flex items-center justify-center shrink-0 border border-blue-500/20"><Bot size={18} /></div>
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800/50 text-slate-400">
               <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 1.5 }}>Analysis in progress...</motion.div>
            </div>
          </div>
        )}
      </div>
      
      <div className="w-full max-w-4xl p-4 bg-slate-950/80 backdrop-blur-md border-t border-slate-800/50">
        <form onSubmit={sendMessage} className="flex gap-2 relative">
          <input
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-slate-200"
          />
          <button 
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg px-4 flex items-center justify-center transition-all"
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  )
}
