from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.crew_service import run_crew

router = APIRouter()

class CrewRequest(BaseModel):
    question: str

@router.post("/answer")
def crew_answer(request: CrewRequest):
    try:
        result = run_crew(request.question, resume_text="")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

