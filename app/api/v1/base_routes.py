"""
API v1 endpoints.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to mini-pagilla-api!"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 