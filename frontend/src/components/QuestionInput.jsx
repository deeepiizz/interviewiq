import { useState } from "react"
import axios from "axios"

function QuestionInput({ onAnswer, disabled }) {
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState("quick") // "quick" or "agent"

  const handleAsk = async () => {
    if (!question.trim()) return

    setLoading(true)
    onAnswer({ answer: "", loading: true, score: null, feedback: null, mode })

    const endpoint = mode === "agent" ? "/crew/answer" : "/interview/ask"

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}${endpoint}`,
        { question },
        { headers: { "Content-Type": "application/json" } }
      )
      onAnswer({
        answer: res.data.answer,
        score: res.data.score || null,
        feedback: res.data.feedback || null,
        loading: false,
        mode,
      })
    } catch (err) {
      onAnswer({ answer: `Error: ${err.message}`, loading: false, mode })
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) handleAsk()
  }

  const exampleQuestions = [
    "Tell me about yourself",
    "What are your strengths?",
    "Why this role?",
  ]

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 font-semibold">
          2
        </span>
        <h2 className="text-xl font-semibold text-slate-800">Ask a Question</h2>
      </div>

      {/* Mode toggle */}
      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setMode("quick")}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition ${
            mode === "quick"
              ? "bg-indigo-600 text-white"
              : "bg-slate-100 text-slate-600 hover:bg-slate-200"
          }`}
        >
          ⚡ Quick Answer
        </button>
        <button
          onClick={() => setMode("agent")}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition ${
            mode === "agent"
              ? "bg-indigo-600 text-white"
              : "bg-slate-100 text-slate-600 hover:bg-slate-200"
          }`}
        >
          🤖 Multi-Agent (with scoring)
        </button>
      </div>

      <p className="text-xs text-slate-500 mb-3">
        {mode === "quick"
          ? "Fast single-LLM answer using RAG retrieval."
          : "Three agents collaborate: Researcher → Writer → Critic. Slower but scored."}
      </p>

      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            disabled
              ? "Upload your resume first..."
              : "e.g. Tell me about a challenging project"
          }
          disabled={disabled}
          className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-slate-100 disabled:cursor-not-allowed"
        />
        <button
          onClick={handleAsk}
          disabled={loading || disabled || !question.trim()}
          className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white font-medium rounded-lg transition disabled:bg-slate-300 disabled:cursor-not-allowed"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {!disabled && (
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="text-xs text-slate-500 self-center">Try:</span>
          {exampleQuestions.map((q) => (
            <button
              key={q}
              onClick={() => setQuestion(q)}
              className="text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-full transition"
            >
              {q}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default QuestionInput