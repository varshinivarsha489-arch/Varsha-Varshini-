from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    dates: str = Field(..., min_length=1)


@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return {"document": document}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
