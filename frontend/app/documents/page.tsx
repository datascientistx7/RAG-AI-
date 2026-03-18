"use client"
import { useState } from "react"
import { motion } from "framer-motion"
import { Upload, File, CheckCircle2, AlertCircle } from "lucide-react"
import { apiUrl } from "@/lib/api"

export default function DocumentsPage() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle")
  const [message, setMessage] = useState("")

  const handleUpload = async () => {
    if (!file) return
    setStatus("uploading")
    
    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch(apiUrl("/upload"), {
        method: "POST",
        body: formData,
      })
      const data = await res.json()
      if (res.ok) {
        setStatus("success")
        setMessage(`Successfully processed ${data.chunks} chunks.`)
      } else {
        setStatus("error")
        setMessage(data.detail || "Upload failed")
      }
    } catch (err) {
      setStatus("error")
      setMessage("Connection error. Is backend running?")
    }
  }

  return (
    <div className="flex-1 overflow-y-auto p-8 flex flex-col items-center">
      <div className="max-w-3xl w-full pt-10">
        <h1 className="text-3xl font-bold mb-2">Documents</h1>
        <p className="text-slate-400 mb-8">Upload PDFs to augment the AI's knowledge base.</p>

        <motion.div 
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900 border border-slate-800 rounded-2xl p-8 flex flex-col items-center justify-center gap-4"
        >
          <div className="w-20 h-20 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500 mb-4">
            <Upload size={32} />
          </div>
          
          <input 
            type="file" 
            accept=".pdf"
            className="hidden" 
            id="file-upload"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
              if (e.target.files?.[0]) {
                setFile(e.target.files[0])
                setStatus("idle")
              }
            }}
          />
          <label htmlFor="file-upload" className="cursor-pointer bg-slate-800 hover:bg-slate-700 transition px-6 py-3 rounded-lg font-medium">
            Select PDF File
          </label>

          {file && (
            <div className="flex items-center gap-3 mt-4 text-slate-300 bg-slate-950 px-4 py-2 rounded-lg border border-slate-800 w-full max-w-md">
              <File size={20} className="text-blue-400" />
              <span className="flex-1 truncate">{file.name}</span>
              <span className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
            </div>
          )}

          {file && status === "idle" && (
            <button 
              onClick={handleUpload}
              className="mt-4 bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-lg font-medium transition-all shadow-lg shadow-blue-500/20 w-full max-w-md"
            >
              Upload & Process
            </button>
          )}

          {status === "uploading" && (
            <div className="mt-4 text-blue-400 flex items-center gap-2">
              <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                <Upload size={20} />
              </motion.div>
              Processing document...
            </div>
          )}

          {status === "success" && (
            <div className="mt-4 text-emerald-400 flex items-center gap-2 bg-emerald-500/10 px-4 py-2 rounded-lg">
              <CheckCircle2 size={20} />
              {message}
            </div>
          )}

          {status === "error" && (
            <div className="mt-4 text-red-400 flex items-center gap-2 bg-red-500/10 px-4 py-2 rounded-lg">
              <AlertCircle size={20} />
              {message}
            </div>
          )}

        </motion.div>
      </div>
    </div>
  )
}
