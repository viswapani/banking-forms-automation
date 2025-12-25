from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Float, JSON, ForeignKey
from sqlalchemy.sql import func

from ..database import Base


class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer, primary_key=True, index=True)
    acknowledgment_id = Column(String(50), unique=True, nullable=False)
    form_type = Column(String(100))
    customer_email = Column(String(255))
    customer_name = Column(String(255))
    uploaded_file_path = Column(Text)
    extracted_text = Column(Text)
    structured_data = Column(JSON)
    missing_fields = Column(JSON)
    status = Column(String(50), default="pending")
    confidence_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )
    branch_code = Column(String(20))


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("form_submissions.id"), nullable=False)
    email_type = Column(String(50))  # acknowledgment / followup
    recipient = Column(String(255))
    subject = Column(Text)
    body = Column(Text)
    sent_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(String(20))  # sent / failed