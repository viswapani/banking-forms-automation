import base64

import openai

from ..config import get_settings


settings = get_settings()
openai.api_key = settings.openai_api_key


async def extract_text_from_image(image_path: str) -> dict:
    """Use GPT‑4 Vision to extract all text from the form image.

    Returns dict with keys: text (str), success (bool).
    """
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract ALL readable text (including handwriting) from this banking form.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ],
            }
        ],
        max_tokens=2000,
    )

    text = response.choices[0].message.content
    return {"text": text, "success": True}
