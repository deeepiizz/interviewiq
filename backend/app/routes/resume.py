from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.services.rag_service import build_index_from_pdf

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Build FAISS index from the uploaded resume
    try:
        chunk_count = build_index_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return {
        "message": "Resume uploaded and indexed successfully",
        "filename": file.filename,
        "chunks_indexed": chunk_count
    }