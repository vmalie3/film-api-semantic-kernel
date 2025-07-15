from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import RequireAdminToken

security = HTTPBearer()
from core.deps import get_auth_handler
from domain.models.auth_models import AuthTokenResponse, AuthenticatedUser
from fastapi import Query
from core.auth.auth_handler import AuthHandler
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/login", response_model=AuthTokenResponse)
async def get_auth_token(
    user_id: int = Query(..., description="Customer ID"),
    auth_handler: AuthHandler = Depends(get_auth_handler)
) -> AuthTokenResponse:
    """Get an authentication token for a customer."""
    return await auth_handler.create_auth_token(user_id)

@router.get("/me", response_model=AuthenticatedUser)
async def get_authenticated_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_handler: AuthHandler = Depends(get_auth_handler)
) -> AuthenticatedUser:
    """Get the authenticated user."""
    token = credentials.credentials
    return await auth_handler.get_authenticated_user(token)