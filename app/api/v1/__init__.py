"""
API v1 routes - equivalent to registering Controllers in .NET.
"""

from fastapi import APIRouter

from .film_routes import router as films_router
from .customer_routes import router as customers_router
from .ai_routes import router as ai_chat_router
from .auth_routes import router as auth_router
# from .streaming import router as streaming_router      # When created

# Main API router for version 1
api_router = APIRouter(
    prefix="/api/v1"
)

# Register all "controllers" (routers)
api_router.include_router(films_router)
api_router.include_router(customers_router)
api_router.include_router(ai_chat_router)
api_router.include_router(auth_router)
# api_router.include_router(streaming_router)     # When created 