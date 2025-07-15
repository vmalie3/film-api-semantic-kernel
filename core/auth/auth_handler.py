from typing import Dict

import logging
from domain.services.auth_service import AuthService
from domain.services.deps import get_auth_service
from domain.models.auth_models import AuthenticatedUser, AuthTokenResponse
from core.auth.jwt_service import JWTService
from fastapi import Depends
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class AuthHandler:
    """Handles JWT authentication operations."""
    
    def __init__(self, auth_service: AuthService = Depends(get_auth_service), jwt_service: JWTService = JWTService()):
        self.auth_service = auth_service
        self.jwt_service = jwt_service
    
    async def create_auth_token(self, customer_id: int) -> Dict[str, str]:
        user = await self.auth_service.get_customer_by_id(customer_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = await self.jwt_service.sign_jwt(user)
        return AuthTokenResponse(access_token=token)
    
    async def get_authenticated_user(self, token: str) -> AuthenticatedUser:
        payload = await self.jwt_service.decode_jwt(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = await self.auth_service.get_authenticated_user(payload)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    
    async def get_admin_user(self, token: str) -> AuthenticatedUser:
        user = await self.get_authenticated_user(token)
        if not user.role == "dvd_admin":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
