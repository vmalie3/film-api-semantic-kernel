"""
Semantic Kernel Chat API endpoints.
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional

from domain.services import AIService
from domain.services.deps import get_ai_service
from domain.models.requests import FilmSummaryRequest
from domain.models.responses import FilmSummaryResponse

router = APIRouter(
    prefix="/ai",
    tags=["ai"],  # Swagger grouping
)

@router.get("/ask", response_model=str)
async def ask(
    question: Optional[str] = Query(None, description="Prompt to ask the AI"),
    ai_service: AIService = Depends(get_ai_service)
) -> str:
    return await ai_service.ask(question)

@router.post("/summary", response_model=FilmSummaryResponse)
async def summary(
    film_summary_request: FilmSummaryRequest,
    ai_service: AIService = Depends(get_ai_service)
) -> FilmSummaryResponse:
    return await ai_service.film_summary(film_summary_request)