from typing import Dict, Any
import json

import openai

from ..config import get_settings


settings = get_settings()
openai.api_key = settings.openai_api_key


async def parse_form_to_json(extracted_text: str, form_type: str) -> Dict[str, Any]:
    """Use GPT‑4 Turbo to convert extracted text into structured JSON.

    Returns dict with keys: data (dict), success (bool).
    """
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")

    # Example template for Cheque Book Request; you can expand for other types.
    template = {
        "form_type": form_type,
        "customer_name": "",
        "account_number": "",
        "number_of_leaves": "",
        "branch_code": "",
        "delivery_address": "",
        "mobile": "",
        "email": "",
    }

    prompt = f"""Extract information from this {form_type} banking form and fill the following JSON template.
Template (keys and types must be preserved):
{json.dumps(template, indent=2)}

Source text:
{extracted_text}

Return ONLY valid JSON, no explanations.
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a JSON API. Always return ONLY valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError("LLM returned invalid JSON")

    return {"data": parsed, "success": True}
