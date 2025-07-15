"""
Database models package for the mini-pagila API.

This package contains SQLAlchemy models representing database entities.
All models are automatically imported through base.py to ensure they're
registered with Base.metadata for Alembic migrations.
"""

# Import Base first - this automatically imports all models
from .base import Base, MPAARating

# Import individual model classes for convenience
from .location import Country, City, Address
from .film import Actor, Category, Language, Film, FilmActor, FilmCategory
from .business import Store, Staff, Customer, Inventory, Rental, Payment
from .streaming_subscription import StreamingSubscription

# Export all models for convenient imports
__all__ = [
    # Base
    "Base",
    "MPAARating",
    # Location
    "Country",
    "City", 
    "Address",
    # Film
    "Actor",
    "Category",
    "Language",
    "Film",
    "FilmActor",
    "FilmCategory",
    "Store",
    "Staff",
    "Customer",
    "Inventory",
    "Rental",
    "Payment",
    # Streaming
    "StreamingSubscription",
] 