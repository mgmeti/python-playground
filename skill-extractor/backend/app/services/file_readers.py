import os
import tempfile
from docx import Document
from PyPDF2 import PdfReader
from fastapi import UploadFile

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def extract_text_from_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    if ext == ".docx":
        return extract_text_from_docx(tmp_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(tmp_path)
    else:
        return open(tmp_path, "r", encoding="utf-8").read()
