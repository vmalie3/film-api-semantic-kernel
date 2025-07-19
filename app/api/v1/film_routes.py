"""
Films API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from core.security import RequireAdminToken
from domain.services.film_service import FilmService
from domain.models.requests.film import CreateFilmRequest, UpdateFilmRequest
from domain.models.responses.film import FilmResponse, FilmListResponse, FilmCreateResponse
from domain.services.deps import get_film_service

router = APIRouter(prefix="/films", tags=["Films"])

@router.get("/", response_model=FilmListResponse)
async def get_films(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
    category: Optional[str] = Query(None, description="Filter by category name (case-insensitive partial match)"),
    service: FilmService = Depends(get_film_service)
) -> FilmListResponse:
    """Get paginated list of films with optional category filter."""
    response = await service.get_films(page=page, page_size=page_size, category=category)
    
    return response


@router.get("/{film_id}", response_model=FilmResponse)
async def get_film(
    film_id: int,
    service: FilmService = Depends(get_film_service)
) -> FilmResponse:
    """Get a film by ID."""
    film = await service.get_film(film_id)
    
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Film with ID {film_id} not found"
        )
    
    return film

@router.get("/search/{film_search_title}", response_model=FilmResponse | None)
async def get_film_by_title(
    film_search_title: str,
    service: FilmService = Depends(get_film_service)
) -> FilmResponse | None:
    """Get a film by title."""
    film = await service.get_film_by_title_search(film_search_title.upper())
    return film
