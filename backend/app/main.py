from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume import router as resume_router

app = FastAPI(title="InterviewIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, tags=["Resume"])


@app.get("/")
def root():
    return {"message": "InterviewIQ API is running"}