import requests
import json

def format_parsed_text_to_json(raw_text: str) -> dict:
    mistral = "http://localhost:11434/api/generate"
    prompt = f"""
    Please fix all typos and ensure that all fields are populated with 100% certainty.
    If you are not 100% certain, then do it to the best of your ability.

    Extract the following fields from the raw_text you received:
    1. Claimant Name
    2. Claimant Date (in MM-DD-YYYY format)
    3. Claim Summary (Keep the summary to 1-3 sentences)
    4. Claim Amount (return as a float for a USD amount)

    Text:
    {raw_text}

    Return the required fields in JSON format.
    """

    response = requests.post(mistral, json={"model":"mistral", "prompt":prompt, "stream":False})
    response.raise_for_status()

    output = response.json()
    json_text = output.get("response", "").strip()

    return json.loads(json_text)
