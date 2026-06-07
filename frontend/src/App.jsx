import { useState } from "react"
import ResumeUpload from "./components/ResumeUpload"
import QuestionInput from "./components/QuestionInput"
import AnswerCard from "./components/AnswerCard"

function App() {
  const [answerState, setAnswerState] = useState({
    answer: "",
    loading: false,
    score: null,
    feedback: null,
    mode: "quick",
  })
  const [resumeUploaded, setResumeUploaded] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="max-w-3xl mx-auto px-4 py-12">
        {/* Header */}
        <header className="text-center mb-10">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-3">
            InterviewIQ
          </h1>
          <p className="text-slate-600 text-lg">
            Your AI-powered interview copilot — tailored to your resume
          </p>
        </header>

        {/* Main content */}
        <div className="space-y-6">
          <ResumeUpload onUploadSuccess={() => setResumeUploaded(true)} />
          <QuestionInput
            onAnswer={setAnswerState}
            disabled={!resumeUploaded}
          />
          <AnswerCard
            answer={answerState.answer}
            loading={answerState.loading}
            score={answerState.score}
            feedback={answerState.feedback}
            mode={answerState.mode}
          />
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-slate-500 text-sm">
          Built with FastAPI, React, LangChain &amp; Groq · Powered by Llama 3.3
        </footer>
      </div>
    </div>
  )
}

export default App