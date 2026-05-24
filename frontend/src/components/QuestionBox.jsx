import { useState } from "react";
import api from "../services/api";

export default function QuestionInput({ setResult }) {
  const [question, setQuestion] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) return;

    const res = await api.post("/interview/ask", {
      question,
    });

    setResult(res.data);
  };

  return (
    <div className="bg-white p-5 rounded-xl shadow mt-4">
      <h2 className="text-xl font-bold mb-3">Ask Interview Question</h2>

      <textarea
        className="w-full border p-3 rounded-lg"
        rows="4"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Example: Tell me about yourself"
      />

      <button
        onClick={handleAsk}
        className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg"
      >
        Generate Answer
      </button>
    </div>
  );
}