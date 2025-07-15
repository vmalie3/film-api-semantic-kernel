"""
Rental request schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateRentalRequest(BaseModel):
    """Request schema for creating a new rental."""
    
    inventory_id: int = Field(..., gt=0, description="Inventory ID to rent")
    staff_id: int = Field(..., gt=0, description="Staff member processing the rental")
    rental_date: Optional[datetime] = Field(default_factory=datetime.now, description="Rental date (defaults to now)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "inventory_id": 1,
                "staff_id": 1
            }
        } 