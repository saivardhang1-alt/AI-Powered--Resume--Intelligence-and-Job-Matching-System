from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import shutil
from uuid import uuid4

from resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)
from job_matcher import match_resume_with_job

app = FastAPI(
    title="AI Powered Resume Intelligence",
    description="Resume Analysis, ATS Scoring and Job Matching",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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

    filename = file.filename.lower()

    if not filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    extension = os.path.splitext(filename)[1]
    file_path = os.path.join(
        UPLOAD_DIR, f"{uuid4().hex}{extension}"
    )

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if extension == ".pdf":
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_docx(file_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in resume"
            )

        return {
            "filename": file.filename,
            "message": "Resume uploaded successfully",
            "extracted_text": text
        }

    finally:
        await file.close()
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/analyze-resume/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    filename = file.filename.lower()

    if not filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    extension = os.path.splitext(filename)[1]
    file_path = os.path.join(
        UPLOAD_DIR, f"{uuid4().hex}{extension}"
    )

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if extension == ".pdf":
            resume_text = extract_text_from_pdf(file_path)
        else:
            resume_text = extract_text_from_docx(file_path)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in resume"
            )

        if not job_description.strip():
            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty"
            )

        result = match_resume_with_job(
            resume_text,
            job_description
        )

        return {
            "message": "Resume analysis completed",
            "filename": file.filename,
            "analysis": result
        }

    finally:
        await file.close()
        if os.path.exists(file_path):
            os.remove(file_path)
