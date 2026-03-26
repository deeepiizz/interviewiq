from fastapi import APIRouter, UploadFile, File
import os

from app.services.pdf_parser import extract_text_from_pdf
from app.utils.text_chunker import chunk_text

router = APIRouter(prefix="/resume")


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "text_length": len(text),
        "chunks": len(chunks),
    }