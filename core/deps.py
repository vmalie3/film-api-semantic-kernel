from core.auth.auth_handler import AuthHandler
from domain.services.auth_service import AuthService
from domain.services.deps import get_auth_service
from fastapi import Depends

def get_auth_handler(auth_service: AuthService = Depends(get_auth_service)) -> AuthHandler:
    return AuthHandler(auth_service)