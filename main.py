from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from backend.routes import router

settings = get_settings()
app = FastAPI(title="LegalEase API", description="AI-assisted legal document drafting API.", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["System"])
def root():
    return {"name": "LegalEase API", "version": "1.0.0", "status": "running", "docs": "/docs"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy", "mock_mode": settings.mock_mode, "model": settings.gemini_model}

app.include_router(router)
