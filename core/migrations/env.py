import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from core.config import settings
from core.logging import get_logger

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
logger = get_logger(__name__)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all your models here for autogenerate to work
from domain.entities import Base  # This imports all models through __init__.py
from domain.entities import *  # This ensures all models are imported

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def get_url():
    db_key = settings.db_key
    if not db_key:
        logger.error("DB_KEY environment variable is required")
        raise ValueError("DB_KEY environment variable is required")
    
    url_key = f"{db_key.lower()}_database_url"
    db_url = getattr(settings, url_key, None)
    if not db_url:
        logger.error(f"Database URL for {db_key} not found")
        raise ValueError(f"Database URL for {db_key} not found")
    
    return db_url


def include_object(object, name, type_, reflected, compare_to):
    """
    Should you include this object in autogenerate?
    
    Return False for any tables we don't want Alembic to manage.
    """
    if type_ == "table":
        # Ignore partitioned payment tables
        if name.startswith("payment_p2022_"):
            return False
        
        # Ignore package management tables
        if name.startswith("packages_"):
            return False
            
        # Ignore any other tables you don't want to manage
        # Add more patterns here as needed
        
    return True

def run_migrations_online() -> None:
    logger.info("Starting database migrations")
    
    try:
        configuration = config.get_section(config.config_ini_section)
        configuration["sqlalchemy.url"] = get_url()
        
        logger.info("Connecting to database")

        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            logger.info("Database connection established")

            context.configure(
                connection=connection, 
                target_metadata=target_metadata,
                include_object=include_object,
            )

            with context.begin_transaction():
                logger.info("Running migrations")
                context.run_migrations()
                logger.info("Migrations completed")
                
    except Exception as e:
        logger.error("Error running migrations: %s", e)
        raise e

run_migrations_online()
