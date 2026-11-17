from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil

from resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

app = FastAPI(
    title="AI Powered Resume Analyzer",
    description="Resume Analysis and ATS Scoring API",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer",
        "status": "Running successfully"
    }


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    file_path = os.path.join(UPLOAD_DIR, os.path.basename(file.filename))

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)

    return {
        "filename": file.filename,
        "message": "Resume uploaded successfully",
        "extracted_text": text
    }
