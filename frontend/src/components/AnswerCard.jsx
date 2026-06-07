function AnswerCard({ answer, loading, score, feedback, mode }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 min-h-[180px]">
      <div className="flex items-center gap-2 mb-4">
        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 font-semibold">
          3
        </span>
        <h2 className="text-xl font-semibold text-slate-800">AI Answer</h2>
        {mode === "agent" && !loading && answer && (
          <span className="ml-auto text-xs px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full font-medium">
            🤖 Multi-Agent
          </span>
        )}
      </div>

      {loading ? (
        <div className="flex items-center gap-3 text-slate-500">
          <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <span>
            {mode === "agent"
              ? "Agents collaborating... (Researcher → Writer → Critic)"
              : "Crafting your answer..."}
          </span>
        </div>
      ) : answer ? (
        <>
          <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
            {answer}
          </p>

          {/* Score and feedback - only for multi-agent mode */}
          {mode === "agent" && score && (
            <div className="mt-5 pt-4 border-t border-slate-200 space-y-3">
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-slate-700">
                  Critic Score:
                </span>
                <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm font-bold">
                  {score}
                </span>
              </div>
              {feedback && (
                <div>
                  <span className="text-sm font-semibold text-slate-700">
                    Feedback:
                  </span>
                  <p className="text-sm text-slate-600 mt-1 italic">
                    {feedback}
                  </p>
                </div>
              )}
            </div>
          )}
        </>
      ) : (
        <p className="text-slate-400 italic">
          Your AI-generated interview answer will appear here.
        </p>
      )}
    </div>
  )
}

export default AnswerCard