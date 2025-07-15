"""
Film request schemas.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, validator


class CreateFilmRequest(BaseModel):
    """Request schema for creating a new film."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Film title")
    description: Optional[str] = Field(None, max_length=1000, description="Film description")
    release_year: Optional[int] = Field(None, ge=1901, le=2155, description="Release year")
    language_id: int = Field(..., gt=0, description="Language ID")
    original_language_id: Optional[int] = Field(None, gt=0, description="Original language ID")
    rental_duration: int = Field(3, ge=1, le=365, description="Rental duration in days")
    rental_rate: float = Field(4.99, ge=0, le=999.99, description="Rental rate")
    length: Optional[int] = Field(None, ge=1, le=1000, description="Film length in minutes")
    replacement_cost: float = Field(19.99, ge=0, le=999.99, description="Replacement cost")
    rating: Optional[str] = Field(None, description="MPAA rating")
    special_features: Optional[List[str]] = Field(None, description="Special features")
    streaming_available: bool = Field(False, description="Available for streaming")
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None:
            allowed_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
            if v not in allowed_ratings:
                raise ValueError(f'Rating must be one of: {allowed_ratings}')
        return v

class FilmSummaryRequest(BaseModel):
    """Request schema for summarizing a film."""
    film_id: int = Field(..., description="Film ID")


class UpdateFilmRequest(BaseModel):
    """Request schema for updating an existing film."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Film title")
    description: Optional[str] = Field(None, max_length=1000, description="Film description")
    release_year: Optional[int] = Field(None, ge=1901, le=2155, description="Release year")
    language_id: Optional[int] = Field(None, gt=0, description="Language ID")
    original_language_id: Optional[int] = Field(None, gt=0, description="Original language ID")
    rental_duration: Optional[int] = Field(None, ge=1, le=365, description="Rental duration in days")
    rental_rate: Optional[float] = Field(None, ge=0, le=999.99, description="Rental rate")
    length: Optional[int] = Field(None, ge=1, le=1000, description="Film length in minutes")
    replacement_cost: Optional[float] = Field(None, ge=0, le=999.99, description="Replacement cost")
    rating: Optional[str] = Field(None, description="MPAA rating")
    special_features: Optional[List[str]] = Field(None, description="Special features")
    streaming_available: Optional[bool] = Field(None, description="Available for streaming")
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None:
            allowed_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
            if v not in allowed_ratings:
                raise ValueError(f'Rating must be one of: {allowed_ratings}')
        return v 