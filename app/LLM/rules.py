
acceptable_case = ["fire", "water damage", "flood", "natural disaster"]
unacceptable_case = ["wear and tear", "accidental damage", "old age", "clients own mistake"]


validation_rules = f"""
    If the Claim Amount is greater than or equal to 10000 then the decision should be to immediately escalate a manager.
    
    If the Claim Summary contains verbage from this list: {acceptable_case} and the Claim Amount is less than 10000 then we can accept the claim.
    Unless, the Claim Summary contains verbage that associates with the following reasons in: {unacceptable_case} then we can reject the claim
"""



