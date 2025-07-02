from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.db.database import AsyncSessionLocal
from app.db.schema import Claims
from app.parsing.parse import extract_text_from_docx, extract_text_from_pdf
from app.LLM.prompt import format_parsed_text_to_json
from app.db.crud import write_to_db

router = APIRouter()

@router.post("/upload-file")
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

@router.get("/claims")
async def get_all_claims():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Claims))
        claims = result.scalars().all()

        if not claims:
            raise HTTPException(404, f"No claims found in claims table") 
        return claims

@router.get("/claims/{claim_id}")
async def get_claim(claim_id: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Claims).where(Claims.id == claim_id))
            claim = result.scalar_one_or_none()
            
            if not claim:
                raise HTTPException(404, f"Claim with {claim_id} NOT FOUND")
            return claim

        except SQLAlchemyError as e:
            raise HTTPException(500, f"Error retrieving claim with claim_id: {claim_id} {e}")

@router.delete("/claims/{claim_id}")
async def delete_claim(claim_id: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Claims).where(Claims.id == claim_id))
            claim = result.scalar_one_or_none()

            if not claim:
                raise HTTPException(404, f"Claim with {claim_id} NOT FOUND")
            return claim
            
        except SQLAlchemyError as e:
            raise HTTPException(500, f"Error deleting claim with claim_id: {claim_id} {e}")