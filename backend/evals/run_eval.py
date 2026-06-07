"""
InterviewIQ Evaluation Suite
"""

import time
import json
from pathlib import Path
import mlflow

from app.services.rag_service import generate_answer, build_index_from_pdf
from app.services.crew_service import run_crew

EVAL_QUESTIONS = [
    "Tell me about yourself",
    "What are your greatest strengths?",
    "Describe a challenging project you worked on",
    "Why are you interested in machine learning?",
    "How do you approach debugging a complex problem?",
    "Tell me about a time you had to learn something new quickly",
    "What's your experience with deep learning frameworks?",
    "Describe your most impactful piece of work",
]

RESUME_PATH = Path("data/sample_resume.pdf")
MLFLOW_EXPERIMENT = "interviewiq-eval"


def setup_resume():
    if not RESUME_PATH.exists():
        raise FileNotFoundError(f"Resume not found at {RESUME_PATH.resolve()}")
    print(f"[setup] Building FAISS index from {RESUME_PATH}...")
    n_chunks = build_index_from_pdf(str(RESUME_PATH))
    print(f"[setup] Indexed {n_chunks} chunks.")
    print()


def eval_baseline(question):
    start = time.time()
    answer = generate_answer(question)
    elapsed = time.time() - start
    return {"answer": answer, "response_time_s": round(elapsed, 2), "answer_length": len(answer)}


def eval_multi_agent(question):
    start = time.time()
    result = run_crew(question, resume_text="")
    elapsed = time.time() - start
    return {
        "answer": result["answer"],
        "score": result["score"],
        "feedback": result["feedback"],
        "response_time_s": round(elapsed, 2),
        "answer_length": len(result["answer"]),
    }


def parse_score(score_str):
    try:
        return float(score_str.split("/")[0].strip())
    except (ValueError, AttributeError, IndexError):
        return None


def run_eval():
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    print("=== InterviewIQ Eval Suite ===")
    print(f"Questions: {len(EVAL_QUESTIONS)}")
    print(f"MLflow experiment: {MLFLOW_EXPERIMENT}")
    print()

    setup_resume()
    results = []

    for i, question in enumerate(EVAL_QUESTIONS, 1):
        print(f"[{i}/{len(EVAL_QUESTIONS)}] Q: {question}")

        with mlflow.start_run(run_name=f"q{i}"):
            mlflow.log_param("question", question)
            mlflow.log_param("question_index", i)

            print("  -> baseline...", end=" ", flush=True)
            baseline = eval_baseline(question)
            print(f"{baseline['response_time_s']}s ({baseline['answer_length']} chars)")
            mlflow.log_metric("baseline_response_time_s", baseline["response_time_s"])
            mlflow.log_metric("baseline_answer_length", baseline["answer_length"])
            mlflow.log_text(baseline["answer"], "baseline_answer.txt")

            print("  -> multi-agent...", end=" ", flush=True)
            agent = eval_multi_agent(question)
            score = parse_score(agent["score"])
            print(f"{agent['response_time_s']}s, score: {agent['score']}")
            mlflow.log_metric("agent_response_time_s", agent["response_time_s"])
            mlflow.log_metric("agent_answer_length", agent["answer_length"])
            if score is not None:
                mlflow.log_metric("critic_score", score)
            mlflow.log_text(agent["answer"], "agent_answer.txt")
            mlflow.log_text(agent["feedback"], "agent_feedback.txt")

            results.append({
                "question": question,
                "baseline_time": baseline["response_time_s"],
                "agent_time": agent["response_time_s"],
                "critic_score": score,
                "feedback": agent["feedback"],
            })
        print()

    print("=" * 70)
    print("EVAL SUMMARY")
    print("=" * 70)

    scores = [r["critic_score"] for r in results if r["critic_score"] is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    avg_baseline_time = sum(r["baseline_time"] for r in results) / len(results)
    avg_agent_time = sum(r["agent_time"] for r in results) / len(results)

    print(f"Questions evaluated:       {len(results)}")
    print(f"Average critic score:      {avg_score:.2f}/10")
    print(f"Avg baseline response:     {avg_baseline_time:.2f}s")
    print(f"Avg multi-agent response:  {avg_agent_time:.2f}s")
    print(f"Multi-agent overhead:      +{(avg_agent_time / avg_baseline_time - 1) * 100:.0f}%")
    print()
    print("Per-question scores:")
    for r in results:
        score_str = f"{r['critic_score']:.0f}/10" if r['critic_score'] else "N/A"
        print(f"  {score_str}  {r['question']}")
    print()

    summary_path = Path("evals/results.json")
    summary_path.write_text(json.dumps({
        "n_questions": len(results),
        "avg_critic_score": avg_score,
        "avg_baseline_time_s": avg_baseline_time,
        "avg_agent_time_s": avg_agent_time,
        "per_question": results,
    }, indent=2))
    print(f"Summary written to {summary_path}")
    print()
    print("View full results: mlflow ui --backend-store-uri ./mlruns")


if __name__ == "__main__":
    run_eval()