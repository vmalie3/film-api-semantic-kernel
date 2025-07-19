"""
Utility functions for converting between SQLModel models and Pydantic schemas.
"""

from typing import TypeVar, Generic, Type, List, Dict, Any, Callable
from pydantic import BaseModel
from decimal import Decimal
from sqlmodel import SQLModel
import asyncio

T = TypeVar('T', bound=BaseModel)


class ModelConverter(Generic[T]):
    """Generic model converter for efficient SQLModel to Pydantic conversion."""
    
    def __init__(self, pydantic_model: Type[T]):
        self.pydantic_model = pydantic_model
        # Cache field names for better performance
        self._field_names = set(pydantic_model.model_fields.keys())
    
    def convert_single(self, sqlmodel_obj: Any, **extra_fields) -> T:
        """
        Convert a single SQLModel object to Pydantic model.
        
        Args:
            sqlmodel_obj: SQLModel instance
            **extra_fields: Additional computed fields to include
            
        Returns:
            Pydantic model instance
        """
        # Get all model fields as dict, handling type conversions
        model_data = {}
        
        # Copy all attributes from SQLModel object (optimized with cached field names)
        for field_name in self._field_names:
            if hasattr(sqlmodel_obj, field_name):
                value = getattr(sqlmodel_obj, field_name)
                
                # Handle Decimal to float conversion automatically
                if isinstance(value, Decimal):
                    value = float(value)
                
                # Handle SQLModel relationship objects
                if hasattr(value, '__class__') and hasattr(value.__class__, '__tablename__'):
                    # This is a SQLModel relationship object, skip it
                    continue
                
                model_data[field_name] = value
        
        # Add any extra computed fields
        model_data.update(extra_fields)
        
        return self.pydantic_model.model_validate(model_data)
    
    def convert_many(self, sqlmodel_objects: List[Any], extra_fields_func: Callable = None) -> List[T]:
        """
        Convert multiple SQLModel objects to Pydantic models efficiently.
        
        Args:
            sqlmodel_objects: List of SQLModel instances
            extra_fields_func: Optional function to compute extra fields for each object
            
        Returns:
            List of Pydantic model instances
        """
        if not sqlmodel_objects:
            return []
        
        # Use list comprehension for better performance than map()
        return [
            self.convert_single(
                obj, 
                **(extra_fields_func(obj) if extra_fields_func else {})
            )
            for obj in sqlmodel_objects
        ]
    
    async def convert_many_async(self, sqlmodel_objects: List[Any], extra_fields_func: Callable = None) -> List[T]:
        """
        Convert multiple SQLModel objects asynchronously for very large datasets.
        
        Args:
            sqlmodel_objects: List of SQLModel instances
            extra_fields_func: Optional function to compute extra fields for each object
            
        Returns:
            List of Pydantic model instances
        """
        if not sqlmodel_objects:
            return []
        
        # For very large datasets, process in chunks
        chunk_size = 1000
        if len(sqlmodel_objects) <= chunk_size:
            return self.convert_many(sqlmodel_objects, extra_fields_func)
        
        # Process in chunks asynchronously
        tasks = []
        for i in range(0, len(sqlmodel_objects), chunk_size):
            chunk = sqlmodel_objects[i:i + chunk_size]
            task = asyncio.create_task(
                asyncio.to_thread(self.convert_many, chunk, extra_fields_func)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        return [item for sublist in results for item in sublist]


# Pre-configured converters for common models
from domain.entities.film import Film
from domain.models.responses.film import FilmResponse

film_converter = ModelConverter(FilmResponse)


def convert_film_to_response(film: SQLModel) -> FilmResponse:
    """Convert Film model to FilmResponse efficiently."""
    return film_converter.convert_single(
        film,
        extra_fields_func=lambda film: {
            'language_name': film.language.name if film.language else None
        }
    )


def convert_films_to_responses(films: List[Film]) -> List[FilmResponse]:
    """Convert multiple Film models to FilmResponse list efficiently."""
    return film_converter.convert_many(
        films,
        extra_fields_func=lambda film: {
            'language_name': film.language.name if film.language else None
        }
    )


async def convert_films_to_responses_async(films: List[Film]) -> List[FilmResponse]:
    """Convert multiple Film models to FilmResponse list asynchronously (for large datasets)."""
    return await film_converter.convert_many_async(
        films,
        extra_fields_func=lambda film: {
            'language_name': film.language.name if film.language else None
        }
    )


# Utility for creating converters for other models
def create_converter(pydantic_model: Type[T]) -> ModelConverter[T]:
    """Factory function to create model converters."""
    return ModelConverter(pydantic_model) 