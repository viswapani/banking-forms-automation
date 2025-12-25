GenAI Banking Forms Automation
Step-by-Step Implementation Specifications
Table of Contents
Section Page
1. Project Overview
2. Technology Stack
3. Project Structure
4. Database Schema
5. System Workflow
6. Implementation Phases
7. Testing & Deployment 
8. Success Metrics 
9. Project Overview
This project focuses on automating the processing of frequently used banking request forms using Generative
AI. The system will detect the form type, extract relevant details using OCR and LLM-based parsing, convert
them into structured JSON, and send an acknowledgment email with a unique Acknowledgement ID.
What We're Building
An AI-powered system that automatically processes banking forms, extracts information, and sends
acknowledgment emails to customers. The system handles 7 different types of banking forms.
Key Features:
• Automatic form type detection using AI
• OCR and intelligent text extraction
• Structured JSON data generation
• Email acknowledgment with unique ID
• Follow-up for missing information
• Admin dashboard for tracking
2. Technology Stack
Component Technology Purpose
Backend Python + FastAPI RESTful API server
AI/ML OpenAI GPT-4 Vision OCR + data extraction
Database PostgreSQL Data persistence
Email SMTP (Gmail/SendGrid) Email delivery
Frontend HTML/CSS/JavaScript User interface
Containerization Docker Deployment
3. Complete Project Structure
banking-forms-automation/
■
■■■ backend/
■ ■■■ app/
■ ■ ■■■ **init**.py
■ ■ ■■■ main.py # FastAPI entry point
■ ■ ■■■ config.py # Configuration
■ ■ ■■■ database.py # Database setup
■ ■ ■
■ ■ ■■■ models/
■ ■ ■ ■■■ **init**.py
■ ■ ■ ■■■ form_models.py # SQLAlchemy models
■ ■ ■
■ ■ ■■■ schemas/
■ ■ ■ ■■■ **init**.py
■ ■ ■ ■■■ form_schemas.py # Pydantic schemas
■ ■ ■ ■■■ json_templates.py # JSON templates
■ ■ ■
■ ■ ■■■ services/
■ ■ ■ ■■■ **init**.py
■ ■ ■ ■■■ form_classifier.py # Detect form type
■ ■ ■ ■■■ ocr_service.py # Extract text
■ ■ ■ ■■■ llm_parser.py # Parse with LLM
■ ■ ■ ■■■ email_service.py # Send emails
■ ■ ■ ■■■ validation.py # Validate data
■ ■ ■
■ ■ ■■■ routes/
■ ■ ■ ■■■ **init**.py
■ ■ ■ ■■■ upload.py # Upload endpoint
■ ■ ■ ■■■ status.py # Status check
■ ■ ■ ■■■ admin.py # Admin APIs
■ ■ ■
■ ■ ■■■ utils/
■ ■ ■■■ **init**.py
■ ■ ■■■ file_handler.py # File utilities
■ ■ ■■■ id_generator.py # ACK ID generator
■ ■
■ ■■■ tests/
■ ■■■ uploads/
■ ■■■ requirements.txt
■ ■■■ Dockerfile
■
■■■ frontend/
■ ■■■ index.html
■ ■■■ status.html
■ ■■■ admin.html
■ ■■■ css/
■ ■ ■■■ style.css
■ ■■■ js/
■ ■■■ upload.js
■ ■■■ status.js
■ ■■■ admin.js
■
■■■ database/
■ ■■■ init.sql
■
■■■ docker-compose.yml
■■■ .env.example
■■■ README.md
4. Database Schema
Table: form_submissions
Column Type Description
id SERIAL PRIMARY KEY Auto-increment ID
acknowledgment_id VARCHAR(50) UNIQUE Unique ACK ID
form_type VARCHAR(100) Type of form
customer_email VARCHAR(255) Customer email
customer_name VARCHAR(255) Customer name
uploaded_file_path TEXT File location
extracted_text TEXT OCR output
structured_data JSONB Parsed JSON data
missing_fields JSONB Missing fields list
status VARCHAR(50) pending/ready
confidence_score FLOAT AI confidence
created_at TIMESTAMP Creation time
updated_at TIMESTAMP Last update
branch_code VARCHAR(20) Branch identifier
Table: email_logs
Column Type Description
id SERIAL PRIMARY KEY Auto-increment ID
submission_id INTEGER Foreign key to submissions
email_type VARCHAR(50) acknowledgment/followup
recipient VARCHAR(255) Email address
subject TEXT Email subject
body TEXT Email HTML content
sent_at TIMESTAMP Send time
status VARCHAR(20) sent/failed
5. Complete System Workflow
Step 1: File Upload
User uploads scanned PDF or image through web interface
Step 2: Form Detection
AI classifies form type (Account Opening, Cheque Request, etc.)
Step 3: OCR Extraction
Vision AI extracts all text from the document
Step 4: LLM Parsing
Extract fields into structured JSON based on form template
Step 5: Validation
Check for missing/unclear fields, calculate confidence
Step 6: ACK ID Generation
Generate unique acknowledgment ID
Step 7: Database Save
Store all extracted data and metadata
Step 8: Email Notification
Send acknowledgment or follow-up email
Step 9: User Response
Display ACK ID and status to user
Decision Flow:
1. Is form type identified? 
 → No: Return error "Unknown form type"
 → Yes: Proceed to extraction
2. Did OCR succeed?
 → No: Return error "OCR failed"
 → Yes: Proceed to parsing
3. Did LLM parsing succeed?
 → No: Return error "Parsing failed" 
 → Yes: Validate data
4. Are all required fields present?
 → Yes: Status = "ready", send acknowledgment
 → No: Status = "pending", send follow-up email
6. Step-by-Step Implementation
PHASE 1: Setup & Infrastructure (Week 1)
Step 1.1: Environment Setup
Create .env file with all configuration:
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/banking_forms
# OpenAI API
OPENAI_API_KEY=your_api_key_here
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
# Application Settings
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png
Step 1.2: Install Dependencies
Create requirements.txt:
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
openai==1.3.7
Pillow==10.1.0
pdf2image==1.16.3
aiofiles==23.2.1
jinja2==3.1.2
Install with: pip install -r requirements.txt
PHASE 2: Core Backend (Week 2)
Step 2.1: Configuration Module
File: backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
 database_url: str
 openai_api_key: str
 smtp_server: str
 smtp_port: int
 smtp_username: str
 smtp_password: str
 upload_folder: str = "./uploads"
 max_file_size: int = 10485760

 class Config:
 env_file = ".env"
@lru_cache()
def get_settings():
 return Settings()
Step 2.2: Database Models
File: backend/app/models/form_models.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Float, JSON
from sqlalchemy.sql import func
from ..database import Base
class FormSubmission(Base):
 **tablename** = "form_submissions"

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
 updated_at = Column(TIMESTAMP, server_default=func.now(), 
 onupdate=func.now())
 branch_code = Column(String(20))
PHASE 3: JSON Templates & Schemas (Week 2)
Supported Form Types:
• Account Opening
• Cheque Book Request
• ATM Card Block/Replacement
• Address Change Request
• RTGS/NEFT Transfer
• KYC Update
• Locker Access/Surrender
Example JSON Template (Cheque Book Request):
{
 "form_type": "Cheque Book Request",
 "customer_name": "",
 "account_number": "",
 "number_of_leaves": "",
 "branch_code": "",
 "delivery_address": "",
 "mobile": "",
 "email": ""
}
Required Fields: 
* customer_name
* account_number
* number_of_leaves
* email
PHASE 4: AI Services (Week 2-3)
Step 4.1: Form Classifier
Uses GPT-4 Vision to identify form type from image.
async def classify_form(image_path: str) -> dict:
 with open(image_path, "rb") as image_file:
 image_data = base64.b64encode(image_file.read()).decode('utf-8')

 response = openai.chat.completions.create(
 model="gpt-4-vision-preview",
 messages=[{
 "role": "user",
 "content": [{
 "type": "text",
 "text": f"Classify this banking form into: {FORM_TYPES}"
 }, {
 "type": "image_url",
 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
 }]
 }],
 max_tokens=50
 )

 return {"form_type": response.choices[0].message.content.strip()}
Step 4.2: OCR Service
Extracts all text including handwritten content.
async def extract_text_from_image(image_path: str) -> dict:
 response = openai.chat.completions.create(
 model="gpt-4-vision-preview",
 messages=[{
 "role": "user",
 "content": [{
 "type": "text",
 "text": "Extract ALL text from this banking form"
 }, {
 "type": "image_url",
 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
 }]
 }],
 max_tokens=2000
 )

 return {"text": response.choices[0].message.content, "success": True}
Step 4.3: LLM Parser
Converts extracted text into structured JSON.
async def parse_form_to_json(extracted_text: str, form_type: str) -> dict:
 template = FORM_TEMPLATES[form_type]

 prompt = f'''Extract information from this {form_type} and return JSON.
Template: {json.dumps(template, indent=2)}
Text: {extracted_text}
Return ONLY valid JSON, no additional text.'''

 response = openai.chat.completions.create(
 model="gpt-4-turbo-preview",
 messages=[
 {"role": "system", "content": "Return only valid JSON"},
 {"role": "user", "content": prompt}
 ],
 temperature=0.1
 )

 parsed_data = json.loads(response.choices[0].message.content)
 return {"data": parsed_data, "success": True}
Step 4.4: Validation Service
def validate_extracted_data(data: dict, form_type: str) -> dict:
 required = REQUIRED_FIELDS.get(form_type, [])
 missing_fields = []

 for field in required:
 value = data.get(field, "")
 if not value or value.strip() == "":
 missing_fields.append(field)

 is_complete = len(missing_fields) == 0

 return {
 "is_complete": is_complete,
 "missing_fields": missing_fields,
 "status": "ready" if is_complete else "pending"
 }
PHASE 5: Email Service (Week 3)
Two Types of Emails:
1. Acknowledgment Email (Complete submission)
2. Follow-up Email (Missing information)
async def send_email(to_email: str, subject: str, html_content: str):
 msg = MIMEMultipart('alternative')
 msg['From'] = settings.smtp_username
 msg['To'] = to_email
 msg['Subject'] = subject

 html_part = MIMEText(html_content, 'html')
 msg.attach(html_part)

 with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
 server.starttls()
 server.login(settings.smtp_username, settings.smtp_password)
 server.send_message(msg)

 return {"success": True}
Email includes:
• Acknowledgment ID
• Form type and customer name
• Status (Ready or Pending)
• List of missing fields (if any)
• Link to upload additional information
• Branch information
PHASE 6: API Routes (Week 3)
Main Upload Endpoint
POST /api/upload - Complete workflow in one endpoint
Workflow Steps:
1. Validate file type and size
2. Save file temporarily
3. Classify form type
4. Extract text via OCR
5. Parse to JSON using LLM
6. Validate extracted data
7. Generate ACK ID
8. Save to database
9. Send appropriate email
10. Return response to user
Status Check Endpoint
GET /api/status/{acknowledgment_id}
@router.get("/status/{acknowledgment_id}")
async def get_status(acknowledgment_id: str, db: Session = Depends(get_db)):
 submission = db.query(FormSubmission).filter(
 FormSubmission.acknowledgment_id == acknowledgment_id
 ).first()

 if not submission:
 raise HTTPException(status_code=404, detail="Not found")

 return {
 "acknowledgment_id": submission.acknowledgment_id,
 "form_type": submission.form_type,
 "status": submission.status,
 "missing_fields": submission.missing_fields
 }
PHASE 7: Frontend (Week 4)
User Interface Components:
index.html: Main upload page with drag-and-drop
status.html: Check submission status by ACK ID
admin.html: Admin dashboard for tracking all submissions
style.css: Professional banking-themed styling
upload.js: Handle file upload and API calls
Key Features:
• Drag and drop file upload
• File type and size validation
• Loading spinner during processing
• Success/error display with ACK ID
• Missing fields highlighted
• Responsive design for mobile
PHASE 8: Docker Deployment (Week 4)
docker-compose.yml Configuration:
version: '3.8'
services:
 db:
 image: postgres:15
 environment:
 POSTGRES_USER: banking_user
 POSTGRES_PASSWORD: banking_pass
 POSTGRES_DB: banking_forms
 volumes:
* postgres_data:/var/lib/postgresql/data
 ports:
* "5432:5432"
 app:
 build: .
 ports:
* "8000:8000"
 depends_on:
* db
 environment:
 DATABASE_URL: postgresql://banking_user:banking_pass@db/banking_forms
 OPENAI_API_KEY: ${OPENAI_API_KEY}
 volumes:
* ./uploads:/app/uploads
volumes:
 postgres_data:
Running the Application:
# 1. Set up environment
cp .env.example .env
# Edit .env with your API keys
# 2. Start with Docker
docker-compose up --build
# 3. Access application
Frontend: [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)
API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
# 4. Stop application
docker-compose down
7. Testing & Quality Assurance
Testing Checklist:
Test Case Expected Result Priority
Upload typed PDF form Successfully processed, ACK sent High
Upload handwritten form Extract 85%+ fields correctly High
Upload incomplete form Identify missing fields, send follow-up High
Upload wrong file type Show error message Medium
Upload oversized file Show size limit error Medium
Check status with valid ACK Display current status High
Check status with invalid ACK Show 404 error Medium
Test all 7 form types Correct classification High
Verify email delivery Emails sent successfully High
Test concurrent uploads Handle multiple users Medium
Unit Testing Example:
# tests/test_upload.py
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_upload_valid_form():
 with open("test_form.pdf", "rb") as f:
 response = client.post(
 "/api/upload",
 files={"file": ("test.pdf", f, "application/pdf")}
 )

 assert response.status_code == 200
 assert "acknowledgment_id" in response.json()
 assert response.json()["success"] == True
8. Success Metrics & KPIs
Metric Target Measurement Method
OCR Accuracy (Typed) 90%+ Field-level comparison
OCR Accuracy (Handwritten) 85%+ Field-level comparison
Form Classification Accuracy 95%+ Correct form type identified
Field-Level F1 Score 92%+ Precision & recall of fields
Email Delivery Success 98%+ Emails sent vs failed
Processing Latency <10 seconds Upload to email time
System Uptime 99.5%+ Availability monitoring
User Satisfaction 4.5/5 User feedback surveys
Monitoring Dashboard Queries:
-- Daily submission count
SELECT DATE(created_at), COUNT(*) 
FROM form_submissions 
GROUP BY DATE(created_at);
-- Success rate by form type
SELECT form_type, 
 COUNT(*) as total,
 SUM(CASE WHEN status='ready' THEN 1 ELSE 0 END) as complete,
 ROUND(100.0 * SUM(CASE WHEN status='ready' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM form_submissions
GROUP BY form_type;
-- Average processing time
SELECT AVG(EXTRACT(EPOCH FROM (processed_at - created_at))) as avg_seconds
FROM form_submissions
WHERE processed_at IS NOT NULL;
9. Project Timeline (8 Weeks)
Week Milestone Deliverables
1 Setup & Infrastructure Environment, DB, dependencies installed
2 OCR + AI Services Form classifier, OCR, LLM parser working
3 Email & Validation Email templates, validation logic complete
4 UI & Testing Frontend, testing, deployment ready
5-6 Integration Testing End-to-end testing, bug fixes
7 Performance Optimization Optimize queries, API response times
8 Documentation & Demo Final report, presentation, handover
10. Best Practices & Tips
Error Handling: Always wrap AI calls in try-except blocks. Log errors for debugging.
API Keys Security: Never commit .env file. Use environment variables in production.
Database Backups: Set up daily automated backups of PostgreSQL database.
Rate Limiting: Implement rate limiting on upload endpoint to prevent abuse.
Logging: Use Python logging module to track all operations.
Code Organization: Follow the modular structure - keep services separate.
Testing: Write tests as you develop, not at the end.
Documentation: Comment complex logic and maintain updated README.
Version Control: Use Git from day one. Commit frequently with clear messages.
Performance: Monitor API response times. Optimize database queries.
11. Common Issues & Solutions
Issue Solution
OpenAI API timeout Increase timeout, retry with exponential backoff
Database connection failed Check DATABASE_URL, ensure PostgreSQL is running
Email not sending Verify SMTP credentials, check app password for Gmail
OCR accuracy low Use higher quality images, preprocess with image enhancement
File upload fails Check file size limit, verify allowed extensions
Missing fields not detected Review required fields mapping in templates
Docker container won't start Check docker-compose.yml syntax, view logs
Frontend can't reach API Enable CORS, verify API URL in JavaScript
12. Future Enhancements
13. Add user authentication and role-based access control
14. Implement document versioning and audit trail
15. Add support for batch processing of multiple forms
16. Create mobile app for form submission
17. Integrate with core banking systems
18. Add OCR confidence visualization
19. Implement automated testing with form samples
20. Add support for multiple languages
21. Create analytics dashboard for managers
22. Implement webhook notifications for status updates
Appendix A: Quick Reference
API Endpoints:
Method Endpoint Description
POST /api/upload Upload and process form
GET /api/status/{ack_id} Check submission status
GET /api/admin/submissions List all submissions (admin)
GET /health Health check
GET /docs API documentation (Swagger)
Environment Variables:
Variable Example Purpose
DATABASE_URL postgresql://user:pass@host/dbDatabase connection
OPENAI_API_KEY sk-... OpenAI authentication
SMTP_SERVER smtp.gmail.com Email server
SMTP_PORT 587 Email port (TLS)
SMTP_USERNAME email@gmail.com Email account
SMTP_PASSWORD app_password Email password
Conclusion
This comprehensive guide provides everything needed to build a production-ready GenAI Banking Forms
Automation system. By following the step-by-step implementation phases, even beginner developers can
create a sophisticated AI-powered application.
Key Takeaways:
• Modular architecture makes the system maintainable and scalable
• AI services (GPT-4 Vision) handle form classification and data extraction
• Proper validation ensures data quality and user follow-up
• Email notifications keep users informed throughout the process
• Docker deployment ensures consistent environments
• Comprehensive testing validates functionality and performance
• Database design supports future enhancements and analytics
Remember: Start small, test frequently, and iterate based on feedback. The system is designed to be built
incrementally, with each phase building upon the previous one.
Happy Coding! ■