from typing import Optional, Dict, Any
from fastapi import Depends
import logging

from domain.entities.business import Customer
from domain.repositories.deps import get_customer_repository
from domain.repositories.customer_repository import CustomerRepository
from domain.models.auth_models import AuthenticatedUser, JWTExpiredError, JWTInvalidError, JWTDecodeError

logger = logging.getLogger(__name__)

class AuthService:
    """Service class for customer operations."""
    
    def __init__(self, customer_repository: CustomerRepository = Depends(get_customer_repository)):
        self.customer_repository = customer_repository

    async def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        logger.info("AuthService: Authenticating user")
        try:
            user = await self.customer_repository.get_customer_by_id(customer_id)
            logger.info(f"AuthService: User authenticated")
            return user
        except Exception as e:
            logger.error(f"AuthService: Error authenticating user: {e}")
            raise e
    
    async def get_authenticated_user(self, payload: Dict[str, Any]) -> Optional[AuthenticatedUser]:
        try:
            user_id = payload.get("user_id")
            if user_id:
                payload = payload.get("user")
                return AuthenticatedUser(**payload)
        except (JWTExpiredError, JWTInvalidError, JWTDecodeError):
            raise e
        except Exception as e:
            logger.error(f"Error getting authenticated user: {e}")
            raise e