from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import AsyncSessionLocal
from app.db.models import Claims 

async def write_to_db(file_name:str, parsed_text:str, structured_claim:dict, decision:str):
    async with AsyncSessionLocal() as session:
        try:
            claim = Claims(
                file_name = file_name,
                parsed_text = parsed_text,
                structured_claim = structured_claim,
                decision = decision
            )
            session.add(claim)
            await session.commit()
            await session.refresh(claim)

            return f"Claim has been added to claims table: {claim}"

        except SQLAlchemyError as e:
            await session.rollback()
            raise RuntimeError(f"Error with submitted payload: {e}")
        