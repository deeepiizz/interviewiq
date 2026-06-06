from datetime import datetime
from pathlib import Path

_mlflow = None
_initialized = False


def _get_mlflow():
    """Import and init mlflow only when first needed (avoids slow import at startup)."""
    global _mlflow, _initialized
    if _initialized:
        return _mlflow
    _initialized = True
    try:
        import mlflow
        MLFLOW_DIR = Path(__file__).parent.parent.parent / "mlruns"
        MLFLOW_DIR.mkdir(exist_ok=True)
        mlflow.set_tracking_uri(f"file:///{MLFLOW_DIR.as_posix()}")
        mlflow.set_experiment("InterviewIQ-RAG")
        _mlflow = mlflow
        print("[MLflow] Initialized successfully")
    except Exception as e:
        print(f"[MLflow] Unavailable, skipping tracking: {e}")
        _mlflow = None
    return _mlflow


def log_rag_run(question, retrieved_chunks, context_length, answer,
                model_name, temperature, max_tokens, response_time_seconds):
    """Log a single RAG run to MLflow. No-op if MLflow can't load."""
    mlflow = _get_mlflow()
    if mlflow is None:
        return
    try:
        with mlflow.start_run(run_name=f"rag-{datetime.now().strftime('%Y%m%d-%H%M%S')}"):
            mlflow.log_param("model", model_name)
            mlflow.log_param("temperature", temperature)
            mlflow.log_param("max_tokens", max_tokens)
            mlflow.log_param("retriever_top_k", 3)
            mlflow.log_param("chunk_size", 1000)
            mlflow.log_param("chunk_overlap", 200)
            mlflow.log_metric("chunks_retrieved", len(retrieved_chunks))
            mlflow.log_metric("context_length_chars", context_length)
            mlflow.log_metric("answer_length_chars", len(answer))
            mlflow.log_metric("response_time_seconds", response_time_seconds)
            mlflow.set_tag("question_type", _classify_question(question))
            mlflow.log_text(question, "question.txt")
            mlflow.log_text(answer, "answer.txt")
            for i, chunk in enumerate(retrieved_chunks):
                mlflow.log_text(chunk, f"chunk_{i+1}.txt")
            print(f"[MLflow] Logged run for question: {question[:50]}...")
    except Exception as e:
        print(f"[MLflow] Logging failed: {e}")


def _classify_question(question: str) -> str:
    q = question.lower()
    if any(w in q for w in ["salary", "compensation", "pay", "expect"]):
        return "salary"
    if any(w in q for w in ["weakness", "fail", "mistake", "challenge"]):
        return "behavioral"
    if any(w in q for w in ["strength", "good at", "skill"]):
        return "strengths"
    if any(w in q for w in ["tell me about yourself", "introduce"]):
        return "intro"
    return "general"