from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.form_models import FormSubmission

router = APIRouter(prefix="/api", tags=["status"])


@router.get("/status/{acknowledgment_id}")
async def get_status(acknowledgment_id: str, db: Session = Depends(get_db)):
    submission = (
        db.query(FormSubmission)
        .filter(FormSubmission.acknowledgment_id == acknowledgment_id)
        .first()
    )

    if not submission:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "acknowledgment_id": submission.acknowledgment_id,
        "form_type": submission.form_type,
        "status": submission.status,
        "missing_fields": submission.missing_fields,
    }