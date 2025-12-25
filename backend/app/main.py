from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import engine
from .models import form_models  # ensure models are imported so metadata is ready
from .routes import upload, status

app = FastAPI(title="GenAI Banking Forms Automation")

# Serve static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Include routers
app.include_router(upload.router)
app.include_router(status.router)


@app.get("/", include_in_schema=False)
async def serve_root():
    # Redirect root to main upload page
    return FileResponse("frontend/index.html")


@app.get("/index.html", include_in_schema=False)
async def serve_index():
    # Explicit route so http://localhost:8000/index.html works
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
