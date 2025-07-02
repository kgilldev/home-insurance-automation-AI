from fastapi import FastAPI, UploadFile, File, HTTPException
from app.db.crud import write_to_db
from app.parsing.parse import extract_text_from_pdf, extract_text_from_docx
from app.LLM.prompt import format_parsed_text_to_json
from app.routes.claims_api import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


