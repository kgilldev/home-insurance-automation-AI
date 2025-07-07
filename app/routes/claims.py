from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import AsyncSessionLocal
from app.parsing.parse import extract_text_from_docx, extract_text_from_pdf
from app.LLM.prompt import format_parsed_text_to_json
from app.db.crud import change_decision_status, create_claim, delete_claim_with_id, get_claim_id, get_claims, get_claims_escalated, update_escalated_claim_status
from app.pydantic.model import ClaimResponse, StructuredClaim, UpdateStructuredClaim

router = APIRouter()

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(400, detail=f"File type not supported {file.filename}, must be a PDF or DOCX")
    
    try:
        file_content = await file.read()

        if file.filename.lower().endswith(".pdf"):
            parsed_text = extract_text_from_pdf(file_content)
        elif file.filename.lower().endswith(".docx"):
            parsed_text = extract_text_from_docx(file_content)
        
        structured_claim = format_parsed_text_to_json(parsed_text)
        decision = structured_claim.claim_decision

        async with AsyncSessionLocal() as session:
            try:
                claim = await create_claim(
                    session, file.filename, parsed_text, structured_claim.model_dump(), decision)
                await session.commit()
                await session.refresh(claim)

                return ClaimResponse(
                    file_name= claim.file_name, 
                    structured_claim= StructuredClaim(**claim.structured_claim), 
                    decision= claim.decision, 
                    decision_reasoning= claim.structured_claim["decision_reasoning"])

            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(500, detail=f"Unable to write claim into DB: {claim}-{e}")

    except RuntimeError as e:
        raise HTTPException(500, detail=f"Error reading file: {file.filename} {e}")
    
    finally:
        await file.close()

@router.get("/claims")
async def get_all_claims():
    async with AsyncSessionLocal() as session:
        claims = await get_claims(session)

        if not claims:
            raise HTTPException(404, f"No claims found in claims table") 
        return claims

@router.get("/claims/escalated")
async def get_escalated_claims():
    async with AsyncSessionLocal() as session:
        escalated_claims = await get_claims_escalated(session)

        if not escalated_claims:
            raise HTTPException(500, f"No escalated claims found") 
        return escalated_claims

@router.get("/claims/{claim_id}")
async def get_claim(claim_id: int):
    async with AsyncSessionLocal() as session:
        try:
            claim = await get_claim_id(session, claim_id)
            
            if not claim:
                raise HTTPException(404, f"Claim with {claim_id} NOT FOUND")
            return claim

        except SQLAlchemyError as e:
            raise HTTPException(500, f"Error retrieving claim with claim_id: {claim_id} {e}")

@router.patch("/claims/escalated/{claim_id}")
async def update_escalated_claim(claim_id: int, payload: UpdateStructuredClaim):
    async with AsyncSessionLocal() as session:
        try:
            claim = await update_escalated_claim_status(session, claim_id)

            if not claim:
                raise HTTPException(404, f"No escalated claims found with id: {claim_id}") 

            await change_decision_status(claim, payload) 

            await session.commit()
            await session.refresh(claim)
            return claim

        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(500, f"No claim found with claim id: {claim_id} when searching for escalated claims")

@router.delete("/claims/{claim_id}")
async def delete_claim(claim_id: int):
    async with AsyncSessionLocal() as session:
        try:
            claim = await delete_claim_with_id(session, claim_id)

            if not claim:
                raise HTTPException(404, f"Claim with {claim_id} NOT FOUND")
            
            await session.delete(claim)
            await session.commit()
            return {"message": f"Claim with id {claim_id} deleted successfully."}

        except SQLAlchemyError as e:
            raise HTTPException(500, f"Error deleting claim with claim_id: {claim_id} {e}")
    