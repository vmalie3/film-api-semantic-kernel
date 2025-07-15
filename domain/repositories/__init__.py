"""
Repository layer for data access operations.
"""

from .base_repository import BaseRepository
from .film_repository import FilmRepository
from .rental_repository import RentalRepository
from .customer_repository import CustomerRepository
from .deps import get_film_repository, get_customer_repository, get_rental_repository

__all__ = [
    "BaseRepository",
    "FilmRepository", 
    "RentalRepository",
    "CustomerRepository",
    "get_film_repository",
    "get_customer_repository", 
    "get_rental_repository",
] 