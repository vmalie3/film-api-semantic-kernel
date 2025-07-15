"""
Customers API routes - equivalent to CustomersController in .NET.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import RequireAdminToken
from domain.services.rental_service import RentalService
from domain.models.requests.rental import CreateRentalRequest
from domain.models.responses.rental import RentalCreateResponse
from domain.services.deps import get_rental_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from core.auth.auth_handler import AuthHandler
from core.deps import get_auth_handler

security = HTTPBearer()

router = APIRouter(
    prefix="/customers",
    tags=["customers"],  # Swagger grouping
)

@router.post("/{customer_id}/rentals", response_model=RentalCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_rental(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    rental_data: CreateRentalRequest,
    auth_handler: AuthHandler = Depends(get_auth_handler),
    service: RentalService = Depends(get_rental_service)
) -> RentalCreateResponse:
    """Create a new rental for a customer. Requires admin authentication."""
    user = await auth_handler.get_admin_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        return await service.create_rental(user.user_id, rental_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 