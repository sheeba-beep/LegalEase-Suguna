# LegalEase

AI-assisted legal document drafting application using Streamlit, FastAPI, and Gemini.

## Quick start

1. `py -3 -m venv .venv`
2. `.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`
5. Keep `MOCK_MODE=true` for the first end-to-end test
6. Terminal 1: `uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000`
7. Terminal 2: `streamlit run frontend/app.py`
8. After testing, set `MOCK_MODE=false` and add `GEMINI_API_KEY`.

API docs: http://127.0.0.1:8000/docs
