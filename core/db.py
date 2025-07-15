"""
Database configuration and session management for multiple databases.
"""

from typing import AsyncGenerator, Dict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

# Database configurations
DATABASES = {
    "film": {
        "echo": False,
        "pool_size": 10,
        "max_overflow": 20
    }
}

# Lazy-loaded engines and session factories
engines: Dict[str, any] = {}
session_factories: Dict[str, any] = {}

def create_engine(db_key: str):
    logger.info(f"Creating engine for {db_key}")
    
    if db_key not in DATABASES:
        logger.error(f"Database '{db_key}' not configured")
        raise ValueError(f"Database '{db_key}' not configured")
    
    config = DATABASES[db_key]

    url_key = f"{db_key.lower()}_database_url"
    db_url = getattr(settings, url_key, None)

    if not db_url:
        logger.error(f"Database URL for {db_key} not found")
        raise ValueError(f"Database URL for {db_key} not found")
    
    # Convert to async URL if needed
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(
        url=db_url,
        echo=config["echo"],
        future=True,
        pool_size=config["pool_size"],
        max_overflow=config["max_overflow"]
    )
    
    session_factory = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    
    return engine, session_factory

def get_engine_and_session_factory(db_key: str):
    """Get or create engine and session factory for a database."""
    if db_key not in engines:
        engines[db_key], session_factories[db_key] = create_engine(db_key)
    
    return engines[db_key], session_factories[db_key]

# Default database
DEFAULT_DB = "film"

async def get_db(db_key: str = DEFAULT_DB) -> AsyncGenerator[AsyncSession, None]:
    """Get database session for specified database."""
    _, session_factory = get_engine_and_session_factory(db_key)
    
    async with session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e

async def get_film_db() -> AsyncGenerator[AsyncSession, None]:
    """Get film database session (for convenience)."""
    _, session_factory = get_engine_and_session_factory("film")
    
    async with session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
