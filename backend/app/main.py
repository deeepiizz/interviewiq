from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume, interview

app = FastAPI(title="InterviewIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])

@app.get("/")
def root():
    return {"message": "InterviewIQ API is running"}