from pydantic import BaseModel
from typing import Optional

class AuthTokenResponse(BaseModel):
    access_token: str

class AuthenticatedUser(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    isActive: bool
    store_id: int
    role: Optional[str] = None

# Exceptions

class JWTError(Exception):
    """Base exception for JWT-related errors."""
    pass

class JWTExpiredError(JWTError):
    """Raised when JWT token has expired."""
    pass

class JWTInvalidError(JWTError):
    """Raised when JWT token is invalid."""
    pass

class JWTDecodeError(JWTError):
    """Raised when JWT token cannot be decoded."""
    pass