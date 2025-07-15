#!/usr/bin/env python3
"""
Main entry point for the mini-pagilla-api application.
"""
import time
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.api.v1 import api_router
from core.config import settings
from core.middleware import DebugMiddleware
from core.logging import configure_logging, get_logger
from core.ai_kernel import kernel_lifespan

# Configure structured logging
configure_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = time.time()
    logger.info("Starting application initialization")
    
    try:
        # Initialize AI kernel using the dedicated lifespan manager
        async with kernel_lifespan() as kernel:
            app.state.kernel = kernel
            
            init_duration = time.time() - start_time
            logger.info("Application initialization completed", duration_ms=round(init_duration * 1000, 2))
            
            yield
            
    except Exception as e:
        logger.error("Application initialization failed", error=str(e), exc_info=True)
        raise
    finally:
        # Cleanup
        logger.info("Shutting down application")

# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add debug middleware (only in debug mode)
if settings.debug:
    app.add_middleware(DebugMiddleware)

# Include API routes (equivalent to registering Controllers in .NET)
app.include_router(api_router)

# Root endpoint for convenience
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Mini Pagilla API!",
        "version": settings.app_version,
        "docs": "/docs",
        "api_v1": "/api/v1/"
    }

def main():
    """Main function to run the application."""
    print(f"Starting {settings.app_name} server...")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

if __name__ == "__main__":
    main() 