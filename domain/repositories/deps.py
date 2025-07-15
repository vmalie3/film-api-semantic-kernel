"""
Repository dependency injection utilities.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.db import get_film_db
from .film_repository import FilmRepository
from .customer_repository import CustomerRepository
from .rental_repository import RentalRepository


def get_film_repository(db: AsyncSession = Depends(get_film_db)) -> FilmRepository:
    return FilmRepository(db)


def get_customer_repository(db: AsyncSession = Depends(get_film_db)) -> CustomerRepository:
    return CustomerRepository(db)


def get_rental_repository(db: AsyncSession = Depends(get_film_db)) -> RentalRepository:
    return RentalRepository(db) 