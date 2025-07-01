from fastapi import FastAPI, UploadFile, File, HTTPException
from app.db.crud import write_to_db
from app.parsing.parse import extract_text_from_pdf, extract_text_from_docx
from app.LLM.prompt import format_parsed_text_to_json

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
        
        structured_claim = format_parsed_text_to_json(parsed_text)

        decision = structured_claim.claim_decision
        await write_to_db(file.filename, parsed_text, structured_claim.model_dump(), decision)

        return {
            "file_name": file.filename, 
            "structured_claim": structured_claim,
            "decision": structured_claim.claim_decision,
            "reason": structured_claim.decision_reasoning,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {file.filename} {e}")
    
    finally:
        await file.close()



