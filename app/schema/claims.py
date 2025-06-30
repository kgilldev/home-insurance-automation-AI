from pydantic import BaseModel

class StructuredClaim(BaseModel):
    claimant_name: str
    claimant_date: str 
    claim_summary: str
    claim_amount: float
    claim_decision: str
    decision_reasoning: str
