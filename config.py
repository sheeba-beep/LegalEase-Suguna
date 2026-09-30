import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "on"}

def _parse_origins(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]

class Settings(BaseModel):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    backend_url: str = "http://127.0.0.1:8000"
    request_timeout_seconds: int = 120
    cors_origins: list[str] = ["http://localhost:8501", "http://127.0.0.1:8501"]
    max_document_chars: int = 30000
    mock_mode: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        backend_url=os.getenv("BACKEND_URL", "http://127.0.0.1:8000"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "120")),
        cors_origins=_parse_origins(os.getenv("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501")),
        max_document_chars=int(os.getenv("MAX_DOCUMENT_CHARS", "30000")),
        mock_mode=_parse_bool(os.getenv("MOCK_MODE", "false")),
    )
