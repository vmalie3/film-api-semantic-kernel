"""
Base configuration for SQLModel models.

This module contains the Base class and ensures all models are imported
so they're registered with Base.metadata for Alembic migrations.
"""

from sqlmodel import SQLModel
import enum

Base = SQLModel

# Custom Enums
class MPAARating(enum.Enum):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"

# Import all models to ensure they're registered with Base.metadata
# This is crucial for Alembic autogenerate to work properly
def _import_all_models():
    """Import all models to register them with Base.metadata"""
    # Import location models
    from . import location  # noqa: F401
    
    # Import film models  
    from . import film  # noqa: F401
    
    # Import business models
    from . import business  # noqa: F401
    
    # Import streaming subscription models
    from . import streaming_subscription  # noqa: F401

# Call the import function when this module is loaded
_import_all_models() 