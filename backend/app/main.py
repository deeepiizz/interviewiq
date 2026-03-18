from fastapi import FastAPI

app = FastAPI(title="InterviewIQ API")


@app.get("/")
def root():
    return {"message": "InterviewIQ backend is running"}
