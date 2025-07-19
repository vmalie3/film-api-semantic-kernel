"""
Service layer for film operations.
"""

import time
from typing import Optional

from domain.entities.film import Film
from domain.entities.base import MPAARating
from domain.models.requests.film import CreateFilmRequest, UpdateFilmRequest
from domain.models.responses.film import FilmResponse, FilmCreateResponse, FilmListResponse, FilmListResponse
from domain.repositories.film_repository import FilmRepository
from domain.utils.model_converter import convert_film_to_response, convert_films_to_responses, convert_films_to_responses_async
from core.logging import get_logger, log_service_operation

class FilmService:
    """Service class for film operations."""
    
    def __init__(self, film_repository: FilmRepository):
        self.film_repository = film_repository
        self.logger = get_logger(__name__)

    async def get_films(self, page: int = 1, page_size: int = 10, category: Optional[str] = None) -> FilmListResponse:
        """
        Get paginated films with optional category filter.
        
        Args:
            page: Page number (1-based)
            page_size: Number of records per page
            category: Optional category name to filter by
            
        Returns:
            Tuple of (films, total_count)
        """
        # Convert page-based pagination to skip/limit for repository
        skip = (page - 1) * page_size
        
        # Get films and total count from repository
        start_time = time.time()
        
        try:
            self.logger.debug("Getting films", skip=skip, limit=page_size)
            
            films, total_count = await self.film_repository.get_films_paginated(
                skip=skip, 
                limit=page_size, 
                category=category
            )
            
            # Convert to response models efficiently
            film_responses = convert_films_to_responses(films)
            
            duration = time.time() - start_time
            log_service_operation(
                logger=self.logger,
                service="FilmService",
                operation="get_films",
                duration=duration,
                skip=skip,
                limit=page_size,
                count=len(films),
                total_count=total_count
            )

            return FilmListResponse(
                films=film_responses,
                total=total_count,
                page=page,
                page_size=page_size
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Service operation failed",
                service="FilmService",
                operation="get_films",
                skip=skip,
                limit=page_size,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def get_film(self, film_id: int) -> Optional[FilmResponse]:
        """
        Get a film by ID.
        
        Args:
            film_id: Film ID
            
        Returns:
            Film if found, None otherwise
        """
        start_time = time.time()
        
        try:
            self.logger.debug("Getting film by ID", film_id=film_id)
            
            film = await self.film_repository.get_film_by_id(film_id)
            
            if not film:
                self.logger.warning("Film not found", film_id=film_id)
                return None
            
            response = convert_film_to_response(film)
            
            duration = time.time() - start_time
            log_service_operation(
                logger=self.logger,
                service="FilmService",
                operation="get_film_by_id",
                duration=duration,
                film_id=film_id,
                found=True
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Service operation failed",
                service="FilmService",
                operation="get_film_by_id",
                film_id=film_id,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def create_film(self, film_data: CreateFilmRequest) -> FilmCreateResponse:
        """
        Create a new film.
        
        Args:
            film_data: Film creation data
            
        Returns:
            Created film response
        """
        start_time = time.time()
        
        try:
            self.logger.debug("Creating film", title=film_data.title)
            
            # Convert rating string to enum if provided
            rating_enum = None
            if film_data.rating:
                rating_mapping = {
                    "G": MPAARating.G,
                    "PG": MPAARating.PG,
                    "PG-13": MPAARating.PG_13,
                    "R": MPAARating.R,
                    "NC-17": MPAARating.NC_17
                }
                rating_enum = rating_mapping.get(film_data.rating)
            
            # Create film instance
            film = Film(
                title=film_data.title,
                description=film_data.description,
                release_year=film_data.release_year,
                language_id=film_data.language_id,
                original_language_id=None,
                rental_duration=film_data.rental_duration,
                rental_rate=film_data.rental_rate,
                length=film_data.length,
                replacement_cost=film_data.replacement_cost,
                rating=rating_enum,
                last_update=None,
                special_features=film_data.special_features,
                fulltext="",
                streaming_available=film_data.streaming_available or False
            )
            
            # Create film through repository
            created_film = await self.film_repository.create_film(film)
            
            response = FilmCreateResponse(
                film_id=created_film.film_id or 0,
                message="Film created successfully"
            )
            
            duration = time.time() - start_time
            log_service_operation(
                logger=self.logger,
                service="FilmService",
                operation="create_film",
                duration=duration,
                film_id=created_film.film_id,
                title=film_data.title
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Service operation failed",
                service="FilmService",
                operation="create_film",
                title=film_data.title,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def update_film(self, film_id: int, film_data: UpdateFilmRequest) -> Optional[FilmResponse]:
        """
        Update an existing film.
        
        Args:
            film_id: Film ID to update
            film_data: Film update data
            
        Returns:
            Updated film if found, None otherwise
        """
        start_time = time.time()
        
        try:
            self.logger.debug("Updating film", film_id=film_id)
            
            # Get existing film
            film = await self.film_repository.get_film_by_id(film_id)
            
            if not film:
                self.logger.warning("Film not found for update", film_id=film_id)
                return None
            
            # Update fields that are provided
            update_data = film_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(film, field, value)
            
            # Update through repository
            updated_film = await self.film_repository.update_film(film)
            
            response = convert_film_to_response(updated_film)
            
            duration = time.time() - start_time
            log_service_operation(
                logger=self.logger,
                service="FilmService",
                operation="update_film",
                duration=duration,
                film_id=film_id
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Service operation failed",
                service="FilmService",
                operation="update_film",
                film_id=film_id,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def delete_film(self, film_id: int) -> bool:
        """
        Delete a film.
        
        Args:
            film_id: Film ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        start_time = time.time()
        
        try:
            self.logger.debug("Deleting film", film_id=film_id)
            
            deleted = await self.film_repository.delete_film(film_id)
            
            duration = time.time() - start_time
            log_service_operation(
                logger=self.logger,
                service="FilmService",
                operation="delete_film",
                duration=duration,
                film_id=film_id,
                deleted=deleted
            )
            
            return deleted
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Service operation failed",
                service="FilmService",
                operation="delete_film",
                film_id=film_id,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def get_films_by_language(self, language_id: int) -> list[FilmResponse]:
        """
        Get all films for a specific language.
        
        Args:
            language_id: Language ID
            
        Returns:
            List of films
        """
        films = await self.film_repository.get_films_by_language(language_id)
        return convert_films_to_responses(films)
    
    async def get_films_by_rating(self, rating: str) -> list[FilmResponse]:
        """
        Get all films with a specific rating.
        
        Args:
            rating: MPAA rating
            
        Returns:
            List of films
        """
        films = await self.film_repository.get_films_by_rating(rating)
        return convert_films_to_responses(films)
    
    async def get_streaming_films(self) -> list[FilmResponse]:
        """
        Get all films available for streaming.
        
        Returns:
            List of streaming films
        """
        films = await self.film_repository.get_streaming_films()
        return convert_films_to_responses(films)
    
    async def search_films_by_title(self, title: str) -> list[FilmResponse]:
        """
        Search films by title.
        
        Args:
            title: Title to search for
            
        Returns:
            List of matching films
        """
        films = await self.film_repository.search_films_by_title(title)
        return await convert_films_to_responses_async(films)
    
    async def get_film_by_title_search(self, title: str) -> Optional[FilmResponse]:
        """
        Get the first film that matches the title search criteria.
        
        Args:
            title: Title to search for
            
        Returns:
            First matching film response or None if not found
        """
        film = await self.film_repository.get_film_by_title_search(title)
        return convert_film_to_response(film) if film else None