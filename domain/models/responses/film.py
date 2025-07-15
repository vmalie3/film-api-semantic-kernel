"""
Film response schemas for API outputs.
"""

from typing import List, Optional, Annotated
from datetime import datetime
from pydantic import BaseModel
from semantic_kernel.kernel_pydantic import KernelBaseModel
from domain.entities.base import MPAARating


class FilmResponse(BaseModel):
    """Film response schema."""
    film_id: int
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    language_id: int
    language_name: Optional[str] = None
    rental_duration: int
    rental_rate: float
    length: Optional[int] = None
    replacement_cost: float
    rating: Optional[MPAARating] = None
    special_features: Optional[List[str]] = None
    last_update: datetime
    streaming_available: Optional[bool] = False

    class Config:
        from_attributes = True


class FilmCreateResponse(BaseModel):
    """Response for film creation."""
    film_id: int
    message: str


class FilmListResponse(BaseModel):
    """Paginated film list response."""
    films: List[FilmResponse]
    total: int
    page: int
    page_size: int 

class FilmSummaryResponse(KernelBaseModel):
    """Response for film summary."""
    title: Annotated[str, "The title of the film"]
    rating: Annotated[str, "The rating of the film"]
    recommended: Annotated[bool, "True if the rating is higher than PG-13 and the rental rate is less than 3.00"]
    summary: Annotated[str, "A summary of the film based on details available"]