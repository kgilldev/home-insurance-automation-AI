from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import and_
from app.db.database import AsyncSessionLocal
from sqlalchemy.future import select
from app.db.schema import Claims
from app.enum.enums import DecisionStatus
from app.pydantic.model import UpdateStructuredClaim 

async def create_claim(session, file_name:str, parsed_text:str, structured_claim:dict, decision:DecisionStatus):
        
    claim = Claims(
        file_name = file_name,
        parsed_text = parsed_text,
        structured_claim = structured_claim,
        decision = decision)

    session.add(claim)
    return claim

async def get_claims(session):
    result = await session.execute(select(Claims))
    claims = result.scalars().all()

    return claims

async def get_claim_id(session, claim_id: int):
    result = await session.execute(select(Claims).where(Claims.id == claim_id))
    claim = result.scalar_one_or_none()

    return claim

async def get_claims_escalated(session):
    result = await session.execute(select(Claims).where(Claims.decision == DecisionStatus.ESCALATED))
    claims = result.scalars().all()

    return claims

async def update_escalated_claim_status(session, claim_id: int):
    result = await session.execute(select(Claims).where(and_(Claims.id == claim_id and Claims.decision == DecisionStatus.ESCALATED )))
    claim = result.scalar_one_or_none()

    return claim

async def change_decision_status(claim, payload: UpdateStructuredClaim):
    claim.decision = payload.decision
    claim.structured_claim["decision"] = payload.decision
    claim.structured_claim["decision_reasoning"] = payload.decision_reasoning
    return claim

async def delete_claim_with_id(session, claim_id: int):
    result = await session.execute(select(Claims).where(Claims.id == claim_id))
    claim = result.scalar_one_or_none()

    return claim