from fastapi import APIRouter, HTTPException
from backend.schemas import DocumentRequest, DocumentResponse
from backend.services.document_generator import generate_document

router = APIRouter(tags=["Documents"])

@router.post("/generate", response_model=DocumentResponse)
def generate_legal_document(request: DocumentRequest) -> DocumentResponse:
    try:
        document = generate_document(
            document_type=request.document_type,
            party_a=request.party_a,
            party_b=request.party_b,
            effective_date=request.effective_date,
            terms=request.terms,
        )
        return DocumentResponse(document=document)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Document generation failed: {exc}") from exc
