from fastapi import APIRouter, UploadFile, File
import os

from app.services.pdf_parser import extract_text_from_pdf
from app.utils.text_chunker import chunk_text
from app.services.embedder import get_embeddings
from app.services.vector_store import save_index

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    save_index(embeddings, chunks)

    return {
        "message": "Resume uploaded and indexed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }