"""
Structured logging configuration using structlog.
"""

import sys
import structlog
from typing import Any, Dict
from core.config import settings


def configure_logging() -> None:
    """Configure structlog for the application."""
    
    # Configure structlog processors
    structlog.configure(
        processors=[
            # Add timestamp
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # JSON output for production, console for development
            structlog.processors.JSONRenderer() if not settings.debug else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


def log_request_info(logger: structlog.stdlib.BoundLogger, method: str, path: str, status_code: int, duration: float) -> None:
    """
    Log HTTP request information.
    
    Args:
        logger: Logger instance
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration: Request duration in seconds
    """
    logger.info(
        "HTTP request completed",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=round(duration * 1000, 2),
    )


def log_database_operation(logger: structlog.stdlib.BoundLogger, operation: str, table: str, duration: float, **kwargs) -> None:
    """
    Log database operation information.
    
    Args:
        logger: Logger instance
        operation: Database operation (SELECT, INSERT, UPDATE, DELETE)
        table: Table name
        duration: Operation duration in seconds
        **kwargs: Additional context
    """
    logger.info(
        "Database operation completed",
        operation=operation,
        table=table,
        duration_ms=round(duration * 1000, 2),
        **kwargs
    )


def log_service_operation(logger: structlog.stdlib.BoundLogger, service: str, operation: str, duration: float, **kwargs) -> None:
    """
    Log service operation information.
    
    Args:
        logger: Logger instance
        service: Service name
        operation: Operation name
        duration: Operation duration in seconds
        **kwargs: Additional context
    """
    logger.info(
        "Service operation completed",
        service=service,
        operation=operation,
        duration_ms=round(duration * 1000, 2),
        **kwargs
    ) 