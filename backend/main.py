from fastapi import FastAPI

app = FastAPI(
    title="AI Powered Resume Analyzer",
    description="Resume analysis and ATS scoring API"
)

@app.get("/")
def home():
    return {"message": "Welcome to AI Resume Analyzer"}
