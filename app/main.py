from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
import docx
from io import BytesIO

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail=f"File type not supported {file.filename}, must be a PDF or DOCX")
    
    try:
        file_content = await file.read()

        if file.filename.lower().endswith(".pdf"):
            parsed_text = extract_text_from_pdf(file_content)
        elif file.filename.lower().endswith(".docx"):
            parsed_text = extract_text_from_docx(file_content)
        return {
            "file_name": file.filename, 
            "file_size": len(file_content),
            "parsed_text": parsed_text
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {file.filename} {e}")
    
    finally:
        await file.close()


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

