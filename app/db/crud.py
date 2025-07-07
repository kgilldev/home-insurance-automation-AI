from sqlalchemy.exc import SQLAlchemyError
from app.db.database import AsyncSessionLocal
from sqlalchemy.future import select
from app.db.schema import Claims
from app.enum.enums import DecisionStatus 

async def create_claim(session, file_name:str, parsed_text:str, structured_claim:dict, decision:DecisionStatus):
        
        claim = Claims(
            file_name = file_name,
            parsed_text = parsed_text,
            structured_claim = structured_claim,
            decision = decision
            )
        session.add(claim)
        return claim