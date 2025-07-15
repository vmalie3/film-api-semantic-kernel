"""
Custom middleware for the application.
"""

import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from core.logging import get_logger, log_request_info

logger = get_logger(__name__)


class DebugMiddleware(BaseHTTPMiddleware):
    """Middleware for debugging and logging requests."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request start
        logger.debug(
            "HTTP request started",
            method=request.method,
            path=str(request.url.path),
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else None,
        )
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log request completion
            log_request_info(
                logger=logger,
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                duration=duration
            )
            
            return response
            
        except Exception as e:
            # Log request error
            duration = time.time() - start_time
            logger.error(
                "HTTP request failed",
                method=request.method,
                path=str(request.url.path),
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise 