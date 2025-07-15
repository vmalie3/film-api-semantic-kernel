import time
from typing import Dict, Optional, Any
import uuid

import jwt
from core.config import settings
import logging
from domain.entities.business import Customer
from domain.models.auth_models import JWTExpiredError, JWTInvalidError, JWTDecodeError

logger = logging.getLogger(__name__)

class JWTService:
    """Handles JWT authentication operations."""
    
    def __init__(self):
        pass
    
    async def sign_jwt(self, user: Customer) -> str:
        logger.info(f"Signing JWT for user_id: {user.customer_id}")
        payload = {
            "session_id": str(uuid.uuid4()),
            "user_id": user.customer_id,
            "role": "dvd_admin" if user.customer_id < 100 else "customer",
            "user": {
                "user_id": user.customer_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "isActive": user.activebool,
                "store_id": user.store_id,
                "role": "dvd_admin" if user.customer_id < 100 else "customer"
            },
            "expires": time.time() + 600
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        
        return token

    
    async def decode_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            decoded_token = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            
            # Check if token is expired
            if decoded_token.get("expires", 0) < time.time():
                logger.debug("JWT token expired")
                raise JWTExpiredError("JWT token has expired")
                
            return decoded_token
            
        except jwt.ExpiredSignatureError:
            logger.debug("JWT token has expired")
            raise JWTExpiredError("JWT token has expired")
            
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            raise JWTInvalidError(f"Invalid JWT token: {e}")

        except Exception as e:
            logger.error(f"Unexpected error decoding JWT token: {e}", exc_info=True)
            raise JWTDecodeError(f"Unexpected error decoding JWT token: {e}")
