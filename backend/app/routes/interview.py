from fastapi import APIRouter

router = APIRouter()

@router.post("/ask")
def ask_question(data: dict):
    question = data.get("question")

    return {
        "question": question,
        "answer": "This is a dummy answer for now"
    }