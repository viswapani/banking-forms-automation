import os
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

from ..config import get_settings

settings = get_settings()


def ensure_upload_folder() -> Path:
    upload_dir = Path(settings.upload_folder)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


async def save_upload_file(file: UploadFile) -> str:
    """
    Save the uploaded file to the UPLOAD_FOLDER and return its filesystem path.
    """
    upload_dir = ensure_upload_folder()

    # Use original filename; later we can randomize if needed
    dest_path = upload_dir / file.filename

    # Save file contents asynchronously
    contents = await file.read()
    with open(dest_path, "wb") as f:
        f.write(contents)

    return str(dest_path)