from fastapi import HTTPException
import fitz
import docx
from io import BytesIO

def extract_text_from_pdf(fileBytes: bytes):
    parsed_text = ""
    pdf = fitz.open(stream=fileBytes, filetype="pdf")
    for page in pdf:
        # Without "# type: ignore" below, get_text will throw a linting error due to fitz being weird
        parsed_text += page.get_text() + "\n" # type: ignore
    return parsed_text.strip()
    

def extract_text_from_docx(fileBytes: bytes):
    parsed_text = ""
    try:
        doc = docx.Document(BytesIO(fileBytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse .docx extension: {e}")

    for paragraph in doc.paragraphs:
        parsed_text += paragraph.text + "\n"
    return parsed_text.strip()
