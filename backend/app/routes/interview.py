from fastapi import APIRouter, HTTPException
from app.services.rag_service import generate_answer

router = APIRouter()

@router.post("/ask")
def ask_question(data: dict):
    question = data.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")

    try:
        answer = generate_answer(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

    return {
        "question": question,
        "answer": answer
    }