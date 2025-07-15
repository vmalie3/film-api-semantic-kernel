"""
Rental response schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RentalResponse(BaseModel):
    """Response schema for a rental."""
    
    model_config = ConfigDict(from_attributes=True)
    
    rental_id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    return_date: Optional[datetime] = None
    staff_id: int
    last_update: datetime


class RentalCreateResponse(BaseModel):
    """Response schema for created rental."""
    
    model_config = ConfigDict(from_attributes=True)
    
    rental_id: int
    customer_id: int
    inventory_id: int
    film_title: str
    rental_date: datetime
    message: str = "Rental created successfully" 