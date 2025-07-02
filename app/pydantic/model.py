from pydantic import BaseModel

from app.enum.enums import DecisionStatus

class StructuredClaim(BaseModel):
    claimant_name: str
    claimant_date: str 
    claim_summary: str
    claim_amount: float
    claim_decision: DecisionStatus
    decision_reasoning: str

class UpdateStructuredClaim(BaseModel):
    decision: DecisionStatus
    decision_reasoning: str