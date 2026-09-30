from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=200)
    party_a: str = Field(..., min_length=1, max_length=500)
    party_b: str = Field(..., min_length=1, max_length=500)
    effective_date: str = Field(..., min_length=1, max_length=50)
    terms: str = Field(..., min_length=1, max_length=30000)

class DocumentResponse(BaseModel):
    document: str = Field(..., description="Generated legal document text.")
