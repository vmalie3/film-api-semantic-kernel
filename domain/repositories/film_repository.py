"""
Film repository for film-related database operations using SQLModel.
"""

from typing import Optional, List, Tuple
from sqlmodel import select, Session, col
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.film import Film, Category, FilmCategory
from .base_repository import BaseRepository


class FilmRepository(BaseRepository[Film]):
    """Repository for Film entity with specialized queries using SQLModel."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Film)
    
    async def get_films_paginated(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        category: Optional[str] = None
    ) -> Tuple[List[Film], int]:
        # Build base query with eager loading
        base_query = select(Film).options(selectinload(Film.language))
        base_count_query = select(Film)
        
        # Add category filter if provided
        if category:
            base_query = (
                base_query
                .join(FilmCategory)
                .join(Category)
                .where(col(Category.name).contains(category))
            )
            
            base_count_query = (
                base_count_query
                .join(FilmCategory)
                .join(Category)
                .where(col(Category.name).contains(category))
            )
        
        # Get total count first
        count_result = await self.db.execute(base_count_query)
        total_count = len(count_result.all())
        
        # Get films with pagination
        query = base_query.offset(skip).limit(limit).order_by(col(Film.film_id))
        
        result = await self.db.execute(query)
        films = result.scalars().all()
        
        return list(films), total_count
    
    async def get_film_by_id(self, film_id: int) -> Optional[Film]:
        return await self.get_by_id(film_id, load_relationships=["language"])
    
    async def get_films_by_language(self, language_id: int) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(Film.language_id == language_id)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_films_by_rating(self, rating: str) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(Film.rating == rating)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_films_by_category(self, category_name: str) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .join(FilmCategory)
            .join(Category)
            .where(Category.name == category_name)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_streaming_films(self) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(Film.streaming_available == True)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def search_films_by_title(self, title: str) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(col(Film.title).contains(title))
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create_film(self, film: Film) -> Film:
        return await self.create(film)
    
    async def update_film(self, film: Film) -> Film:
        return await self.update(film)
    
    async def delete_film(self, film_id: int) -> bool:
        return await self.delete_by_id(film_id)
    
    async def get_film_by_title_search(self, title: str) -> Optional[Film]:
        """
        Get the first film that matches the title search criteria.
        
        Args:
            title: Title to search for
            
        Returns:
            First matching film or None if not found
        """
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(col(Film.title).contains(title))
            .order_by(Film.title)
            .limit(1)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_available_categories(self) -> List[str]:
        query = select(Category.name).order_by(Category.name)
        
        result = await self.db.execute(query)
        return list(result.scalars().all()) 