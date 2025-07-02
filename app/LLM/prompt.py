import requests
import json
from app.LLM.rules import validation_rules
from app.pydantic.model import StructuredClaim

def format_parsed_text_to_json(raw_text: str) -> StructuredClaim:
    mistral = "http://localhost:11434/api/generate"
    prompt = f"""
    Please fix all typos and ensure that all fields are populated with 100% certainty.
    If you are not 100% certain, then do it to the best of your ability.

    Use the following rules to help make your decision: {validation_rules}

    Extract the following fields from the raw_text you received:
    1. claimant_name
    2. claimant_date (in MM-DD-YYYY format)
    3. claim_summary (Keep the summary to 1-3 sentences)
    4. claim_amount (return as a float for a USD amount)
    5. claim_decision (ACCEPTED, REJECTED, ESCALATED)
    6. decision_reasoning (1-3 sentences on how you made your decision, use the validation_rules to support your argument)

    Text:
    {raw_text}

    Return the required fields in JSON format.
    """

    response = requests.post(mistral, json={"model":"mistral", "prompt":prompt, "stream":False})
    response.raise_for_status()

    output = response.json()
    json_text = output.get("response", "").strip()

    if not json_text:
        raise ValueError("json_text is empty")

    try:
        parsed = json.loads(json_text)
        structured_claim = StructuredClaim(**parsed)
        return structured_claim
    except Exception as e:
        raise ValueError(f"JSON can not be parsed: {e}")
