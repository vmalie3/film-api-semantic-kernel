"""
Film plugin for Semantic Kernel.
"""

import time
from typing import Annotated, Optional
from semantic_kernel.functions import kernel_function

from domain.models.responses.film import FilmResponse
from domain.services.film_service import FilmService
from domain.repositories.film_repository import FilmRepository
from core.db import get_film_db
from core.logging import get_logger

logger = get_logger(__name__)

class FilmPlugin:
    def __init__(self, film_service: FilmService):
        self.film_service = film_service

    @kernel_function(name="get_film_details", description="Get data about a film")
    async def get_film_details(
        self, film_id: Annotated[int, "The ID of the film to get details for"]
    ) -> Optional[FilmResponse]:
        # Use real data if film_service is not provided
        if self.film_service is None:
            async with get_film_db() as session:
                film_service = FilmService(session)
                try:
                    film = await film_service.get_film(film_id)
                    return film
                except Exception as e:
                    # Return None if there's an error - Semantic Kernel will handle this
                    return None
        
        # Use injected film_service
        try:
            film = await self.film_service.get_film(film_id)
            return film  # film_service.get_film already returns FilmResponse or None
        except Exception as e:
            # Return None if there's an error
            return None
    