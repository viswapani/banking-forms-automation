from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.form_models import FormSubmission
from ..utils.file_handler import save_upload_file
from ..utils.id_generator import generate_ack_id
from ..services.form_classifier import classify_form
from ..services.ocr_service import extract_text_from_image
from ..services.llm_parser import parse_form_to_json
from ..services.validation import validate_extracted_data

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload")
async def upload_form(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Basic file type check
    allowed_types = {"application/pdf", "image/jpeg", "image/png"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 1) Save file to disk
    saved_path = await save_upload_file(file)

    # 2) Generate unique ACK ID
    ack_id = generate_ack_id()

    # 3) Run AI pipeline
    # 3a) Classify form type using the uploaded image
    classification = await classify_form(saved_path)
    form_type = classification["form_type"]

    # 3b) Extract text from the image
    ocr_result = await extract_text_from_image(saved_path)
    if not ocr_result.get("success"):
        raise HTTPException(status_code=500, detail="OCR failed (stub)")
    extracted_text = ocr_result["text"]

    # 3c) Parse to JSON using LLM
    parse_result = await parse_form_to_json(extracted_text, form_type)
    if not parse_result.get("success"):
        raise HTTPException(status_code=500, detail="Parsing failed (stub)")
    structured_data = parse_result["data"]

    # 3d) Validate extracted data
    validation = validate_extracted_data(structured_data, form_type)

    # 4) Create a DB record with populated fields
    submission = FormSubmission(
        acknowledgment_id=ack_id,
        form_type=form_type,
        customer_email=structured_data.get("email"),
        customer_name=structured_data.get("customer_name"),
        uploaded_file_path=saved_path,
        extracted_text=extracted_text,
        structured_data=structured_data,
        missing_fields=validation["missing_fields"],
        status=validation["status"],
        confidence_score=classification.get("confidence"),
        branch_code=structured_data.get("branch_code"),
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "success": True,
        "id": submission.id,
        "acknowledgment_id": submission.acknowledgment_id,
        "uploaded_file_path": submission.uploaded_file_path,
        "form_type": submission.form_type,
        "status": submission.status,
        "missing_fields": submission.missing_fields,
        "message": "File processed via OpenAI pipeline and saved to database",
    }
