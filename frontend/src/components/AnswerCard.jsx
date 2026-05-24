function AnswerCard({ answer, loading }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 min-h-[180px]">
      <div className="flex items-center gap-2 mb-4">
        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 font-semibold">
          3
        </span>
        <h2 className="text-xl font-semibold text-slate-800">AI Answer</h2>
      </div>

      {loading ? (
        <div className="flex items-center gap-3 text-slate-500">
          <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <span>Crafting your answer...</span>
        </div>
      ) : answer ? (
        <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
          {answer}
        </p>
      ) : (
        <p className="text-slate-400 italic">
          Your AI-generated interview answer will appear here.
        </p>
      )}
    </div>
  )
}

export default AnswerCard