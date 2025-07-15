"""
Security and authentication utilities.
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

# Security scheme for Swagger UI
security = HTTPBearer()

ADMIN_TOKEN = settings.admin_token


async def validate_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Validate bearer token for admin access.
    
    Args:
        credentials: HTTPBearer credentials from request header
        
    Returns:
        The validated token
        
    Raises:
        HTTPException: If token is invalid
    """
    if credentials.credentials != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


# Dependency for protecting admin endpoints
RequireAdminToken = Depends(validate_admin_token)

# Placeholder for security-related utilities
# Add authentication, authorization, JWT handling, etc. here 