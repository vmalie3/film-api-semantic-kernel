"""
Film-related models: Actor, Category, Language, Film, FilmActor, FilmCategory.
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped, RelationshipProperty
from sqlalchemy import Index, CheckConstraint, INTEGER, CHAR, TEXT, Column, TIMESTAMP, SMALLINT, NUMERIC, ForeignKey
from sqlalchemy.dialects.postgresql import TSVECTOR, ARRAY, DOMAIN, ENUM
from sqlalchemy.sql import func
from typing import Optional, List, TYPE_CHECKING, Any
from datetime import datetime

from .base import Base, MPAARating

if TYPE_CHECKING:
    from domain.entities.business import Inventory


class Actor(Base, table=True):
    __tablename__ = 'actor'
    
    actor_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=Column(TEXT, nullable=False))
    last_name: str = Field(sa_column=Column(TEXT, nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    film_actors: List["FilmActor"] = Relationship(back_populates="actor")
    
    # Index - matches pagila schema exactly
    __table_args__ = (
        Index('idx_actor_last_name', 'last_name'),
    )


class Category(Base, table=True):
    __tablename__ = 'category'
    
    category_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(TEXT, nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    film_categories: List["FilmCategory"] = Relationship(back_populates="category")


class Language(Base, table=True):
    __tablename__ = 'language'
    
    language_id: Optional[int] = Field(default=None, primary_key=True)
    # Original schema uses CHAR(20) - keeping as String for compatibility
    name: str = Field(sa_column=Column(CHAR(20), nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    


class Film(Base, table=True):
    __tablename__ = 'film'
    
    film_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(TEXT, nullable=False))
    description: Optional[str] = Field(sa_column=Column(TEXT))
    # Use Integer with constraint to match the year domain
    release_year: Optional[int] = Field(sa_column=Column(DOMAIN('year', INTEGER())))
    language_id: int = Field(sa_column=Column(INTEGER, ForeignKey("language.language_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    original_language_id: Optional[int] = Field(sa_column=Column(INTEGER, ForeignKey("language.language_id", onupdate='CASCADE', ondelete='RESTRICT')))
    rental_duration: int = Field(sa_column=Column(SMALLINT, server_default=func.text('3'), nullable=False))
    rental_rate: float = Field(sa_column=Column(NUMERIC(4, 2), server_default=func.text('4.99'), nullable=False))
    length: Optional[int] = Field(sa_column=Column(SMALLINT))
    replacement_cost: float = Field(sa_column=Column(NUMERIC(5, 2), server_default=func.text('19.99'), nullable=False))
    rating: Optional[MPAARating] = Field(sa_column=Column(ENUM('G', 'PG', 'PG-13', 'R', 'NC-17', name='mpaa_rating')))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    special_features: Optional[List[str]] = Field(sa_column=Column(ARRAY(TEXT)))
    fulltext: str = Field(sa_column=Column(TSVECTOR, nullable=False))
    streaming_available: bool = Field(default=False, nullable=False)
    
    # Relationships
    language: Mapped[Optional[Language]] = Relationship(
        back_populates="films",
        sa_relationship=RelationshipProperty("Language", primaryjoin="Film.language_id == Language.language_id"),
    )
    original_language: Optional[Language] = Relationship(
        back_populates="original_language_films",
        sa_relationship=RelationshipProperty("Language", primaryjoin="Film.original_language_id == Language.language_id")
    )
    film_actors: List["FilmActor"] = Relationship(back_populates="film")
    film_categories: List["FilmCategory"] = Relationship(back_populates="film")
    inventory: List["Inventory"] = Relationship(back_populates="film")
    
    # Indexes and constraints - match pagila schema exactly
    __table_args__ = (
        Index('film_fulltext_idx', 'fulltext'),  # GIST index
        Index('idx_title', 'title'),
        Index('idx_fk_language_id', 'language_id'),
        Index('idx_fk_original_language_id', 'original_language_id'),
        CheckConstraint('release_year >= 1901 AND release_year <= 2155', name='film_release_year_check'),
    )


class FilmActor(Base, table=True):
    __tablename__ = 'film_actor'
    
    actor_id: int = Field(sa_column=Column(INTEGER, ForeignKey("actor.actor_id", onupdate='CASCADE', ondelete='RESTRICT'), primary_key=True))
    film_id: int = Field(sa_column=Column(INTEGER, ForeignKey("film.film_id", onupdate='CASCADE', ondelete='RESTRICT'), primary_key=True))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    actor: Optional[Actor] = Relationship(back_populates="film_actors")
    film: Optional[Film] = Relationship(back_populates="film_actors")
    
    # Index - matches pagila schema
    __table_args__ = (
        Index('idx_fk_film_id', 'film_id'),
    )


class FilmCategory(Base, table=True):
    __tablename__ = 'film_category'
    
    film_id: int = Field(sa_column=Column(INTEGER, ForeignKey("film.film_id", onupdate='CASCADE', ondelete='RESTRICT'), primary_key=True))
    category_id: int = Field(sa_column=Column(INTEGER, ForeignKey("category.category_id", onupdate='CASCADE', ondelete='RESTRICT'), primary_key=True))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    film: Optional[Film] = Relationship(back_populates="film_categories")
    category: Optional[Category] = Relationship(back_populates="film_categories") 