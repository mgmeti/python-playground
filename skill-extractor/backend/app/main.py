from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.services.file_readers import extract_text_from_file
from app.services.llm_service import extract_skills_experience
from app.models.response_model import ExtractionResponse

app = FastAPI(title="Job Skill Extractor API")

# Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract", response_model=ExtractionResponse)
async def extract_job_info(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    if file:
        content = extract_text_from_file(file)
    elif text:
        content = text
    else:
        return {"skills": [], "experience": ""}

    result = extract_skills_experience(content)
    return result
