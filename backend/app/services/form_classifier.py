from typing import Literal
import base64

import openai

from ..config import get_settings

# Supported form types (from specification)
FormType = Literal[
    "Account Opening",
    "Cheque Book Request",
    "ATM Card Block/Replacement",
    "Address Change Request",
    "RTGS/NEFT Transfer",
    "KYC Update",
    "Locker Access/Surrender",
]


settings = get_settings()
openai.api_key = settings.openai_api_key


async def classify_form(image_path: str) -> dict:
    """Use GPT‑4 Vision to classify the banking form type.

    Returns a dict with keys: form_type (str) and confidence (float, best‑effort).
    """
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    form_types = [
        "Account Opening",
        "Cheque Book Request",
        "ATM Card Block/Replacement",
        "Address Change Request",
        "RTGS/NEFT Transfer",
        "KYC Update",
        "Locker Access/Surrender",
    ]
    prompt = (
        "Classify this banking form into one of the following types: "
        + ", ".join(form_types)
        + ". Return ONLY the form type name."
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ],
            }
        ],
        max_tokens=50,
    )

    raw = response.choices[0].message.content.strip()
    # Best effort: assume the model outputs exactly the form type name.
    return {"form_type": raw, "confidence": 0.9}
