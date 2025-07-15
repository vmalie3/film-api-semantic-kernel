"""
Film repository for film-related database operations using SQLModel.
"""

from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

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
        base_count_query = select(func.count(Film.film_id))
        
        # Add category filter if provided
        if category:
            # Use explicit joins with proper aliasing
            base_query = (
                base_query
                .join(FilmCategory, Film.film_id == FilmCategory.film_id)
                .join(Category, FilmCategory.category_id == Category.category_id)
                .where(Category.name.ilike(f"%{category}%"))
            )
            
            base_count_query = (
                base_count_query
                .join(FilmCategory, Film.film_id == FilmCategory.film_id)
                .join(Category, FilmCategory.category_id == Category.category_id)
                .where(Category.name.ilike(f"%{category}%"))
            )
        
        # Get total count first
        count_result = await self.db.execute(base_count_query)
        total_count = count_result.scalar()
        
        # Get films with pagination
        query = base_query.offset(skip).limit(limit).order_by(Film.film_id)
        
        result = await self.db.execute(query)
        films = result.scalars().all()
        
        return films, total_count
    
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
        return result.scalars().all()
    
    async def get_films_by_rating(self, rating: str) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(Film.rating == rating)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_films_by_category(self, category_name: str) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .join(FilmCategory, Film.film_id == FilmCategory.film_id)
            .join(Category, FilmCategory.category_id == Category.category_id)
            .where(Category.name == category_name)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_streaming_films(self) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(Film.streaming_available == True)
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def search_films_by_title(self, title: str) -> List[Film]:
        query = (
            select(Film)
            .options(selectinload(Film.language))
            .where(Film.title.ilike(f"%{title}%"))
            .order_by(Film.title)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_film(self, film: Film) -> Film:
        return await self.create(film)
    
    async def update_film(self, film: Film) -> Film:
        return await self.update(film)
    
    async def delete_film(self, film_id: int) -> bool:
        return await self.delete_by_id(film_id)
    
    async def get_available_categories(self) -> List[str]:
        query = select(Category.name).order_by(Category.name)
        
        result = await self.db.execute(query)
        return result.scalars().all() 