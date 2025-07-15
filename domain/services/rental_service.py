"""
Service layer for rental operations.
"""

import time
from datetime import datetime
from typing import Optional

from domain.entities.business import Rental
from domain.models.requests.rental import CreateRentalRequest
from domain.models.responses.rental import RentalResponse, RentalCreateResponse
from domain.repositories.rental_repository import RentalRepository
from domain.repositories.customer_repository import CustomerRepository
from core.logging import get_logger

class RentalService:
    """Service class for rental operations."""
    
    def __init__(
        self, 
        rental_repository: RentalRepository,
        customer_repository: CustomerRepository
    ):
        self.rental_repository = rental_repository
        self.customer_repository = customer_repository
        self.logger = get_logger(__name__)
    
    async def create_rental(self, customer_id: int, rental_data: CreateRentalRequest) -> RentalCreateResponse:
        """
        Create a new rental for a customer.
        
        Args:
            customer_id: Customer ID
            rental_data: Rental creation data
            
        Returns:
            Created rental response
            
        Raises:
            ValueError: If validation fails
        """
        start_time = time.time()
        self.logger.debug("Creating rental", customer_id=customer_id, inventory_id=rental_data.inventory_id)
        
        # Validate customer exists
        customer = await self.customer_repository.get_customer_by_id(customer_id)
        if not customer:
            self.logger.error("Customer not found for rental", customer_id=customer_id)
            raise ValueError(f"Customer with ID {customer_id} not found")
        
        # Check if inventory is available
        if not await self.rental_repository.is_inventory_available(rental_data.inventory_id):
            self.logger.warning("Inventory not available for rental", inventory_id=rental_data.inventory_id)
            raise ValueError(f"Inventory item {rental_data.inventory_id} is currently rented out")
        
        # Note: Staff and inventory validation could be added with respective repositories
        # For now, we'll create the rental and let database constraints handle validation
        
        # Create rental
        rental = Rental(
            rental_date=datetime.utcnow(),
            inventory_id=rental_data.inventory_id,
            customer_id=customer_id,
            staff_id=rental_data.staff_id,
            return_date=None  # Will be set when returned
        )
        
        # Create rental through repository
        created_rental = await self.rental_repository.create_rental(rental)
        
        # Get rental with relationships for response (simplified for now)
        rental_with_details = await self.rental_repository.get_rental_by_id(created_rental.rental_id)
        
        film_title = "Unknown"
        if rental_with_details and rental_with_details.inventory and rental_with_details.inventory.film:
            film_title = rental_with_details.inventory.film.title
        
        response = RentalCreateResponse(
            rental_id=created_rental.rental_id,
            customer_id=customer_id,
            inventory_id=rental_data.inventory_id,
            film_title=film_title,
            rental_date=created_rental.rental_date,
            message="Rental created successfully"
        )
        
        duration = time.time() - start_time
        self.logger.info("Rental created successfully", rental_id=created_rental.rental_id, customer_id=customer_id, film_title=film_title, duration_ms=round(duration * 1000, 2))
        
        return response
    
    async def get_rental_by_id(self, rental_id: int) -> Optional[RentalResponse]:
        """
        Get a rental by ID.
        
        Args:
            rental_id: The rental ID
            
        Returns:
            RentalResponse if found, None otherwise
        """
        self.logger.debug("Getting rental by ID", rental_id=rental_id)
        
        rental = await self.rental_repository.get_rental_by_id(rental_id)
        
        if rental:
            self.logger.debug("Rental found", rental_id=rental_id)
            return RentalResponse.model_validate(rental)
        else:
            self.logger.debug("Rental not found", rental_id=rental_id)
            return None
    
    async def get_customer_rentals(self, customer_id: int, active_only: bool = False) -> list[RentalResponse]:
        """
        Get all rentals for a customer.
        
        Args:
            customer_id: Customer ID
            active_only: If True, only return active rentals
            
        Returns:
            List of rental responses
        """
        self.logger.debug("Getting customer rentals", customer_id=customer_id, active_only=active_only)
        
        rentals = await self.rental_repository.get_customer_rentals(customer_id, active_only)
        
        self.logger.debug("Customer rentals retrieved", customer_id=customer_id, rental_count=len(rentals))
        return [RentalResponse.model_validate(rental) for rental in rentals]
    
    async def return_rental(self, rental_id: int, return_date: datetime = None) -> Optional[RentalResponse]:
        """
        Mark a rental as returned.
        
        Args:
            rental_id: Rental ID
            return_date: Return date (defaults to current time)
            
        Returns:
            Updated rental response if found, None otherwise
        """
        start_time = time.time()
        self.logger.debug("Returning rental", rental_id=rental_id)
        
        updated_rental = await self.rental_repository.return_rental(rental_id, return_date)
        
        if updated_rental:
            duration = time.time() - start_time
            self.logger.info("Rental returned successfully", rental_id=rental_id, duration_ms=round(duration * 1000, 2))
            return RentalResponse.model_validate(updated_rental)
        else:
            self.logger.warning("Rental not found for return", rental_id=rental_id)
            return None
    
    async def get_overdue_rentals(self, days_overdue: int = 7) -> list[RentalResponse]:
        """
        Get rentals that are overdue.
        
        Args:
            days_overdue: Number of days past rental duration to consider overdue
            
        Returns:
            List of overdue rental responses
        """
        self.logger.debug("Getting overdue rentals", days_overdue=days_overdue)
        
        rentals = await self.rental_repository.get_overdue_rentals(days_overdue)
        
        self.logger.debug("Overdue rentals retrieved", overdue_count=len(rentals))
        return [RentalResponse.model_validate(rental) for rental in rentals] 