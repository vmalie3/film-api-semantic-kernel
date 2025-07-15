"""
Rental repository for rental-related database operations.
"""

from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.business import Rental, Customer, Staff, Inventory
from .base_repository import BaseRepository


class RentalRepository(BaseRepository[Rental]):
    """Repository for Rental entity with specialized queries."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Rental)
    
    async def get_rental_by_id(self, rental_id: int) -> Optional[Rental]:
        """
        Get a rental by ID with all relationships loaded.
        
        Args:
            rental_id: Rental ID
            
        Returns:
            Rental if found, None otherwise
        """
        query = (
            select(Rental)
            .options(
                selectinload(Rental.customer),
                selectinload(Rental.staff),
                selectinload(Rental.inventory).selectinload(Inventory.film)
            )
            .where(Rental.rental_id == rental_id)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_customer_rentals(self, customer_id: int, active_only: bool = False) -> List[Rental]:
        """
        Get all rentals for a customer.
        
        Args:
            customer_id: Customer ID
            active_only: If True, only return active rentals (not returned)
            
        Returns:
            List of rentals
        """
        query = (
            select(Rental)
            .options(
                selectinload(Rental.inventory).selectinload(Inventory.film),
                selectinload(Rental.staff)
            )
            .where(Rental.customer_id == customer_id)
        )
        
        if active_only:
            query = query.where(Rental.return_date.is_(None))
        
        query = query.order_by(Rental.rental_date.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_active_rental_for_inventory(self, inventory_id: int) -> Optional[Rental]:
        """
        Get active rental for a specific inventory item.
        
        Args:
            inventory_id: Inventory ID
            
        Returns:
            Active rental if found, None otherwise
        """
        query = (
            select(Rental)
            .where(
                Rental.inventory_id == inventory_id,
                Rental.return_date.is_(None)
            )
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_overdue_rentals(self, days_overdue: int = 7) -> List[Rental]:
        """
        Get rentals that are overdue.
        
        Args:
            days_overdue: Number of days past rental duration to consider overdue
            
        Returns:
            List of overdue rentals
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_overdue)
        
        query = (
            select(Rental)
            .options(
                selectinload(Rental.customer),
                selectinload(Rental.inventory).selectinload(Inventory.film)
            )
            .where(
                Rental.return_date.is_(None),
                Rental.rental_date < cutoff_date
            )
            .order_by(Rental.rental_date)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_rentals_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Rental]:
        """
        Get rentals within a date range.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            List of rentals
        """
        query = (
            select(Rental)
            .options(
                selectinload(Rental.customer),
                selectinload(Rental.inventory).selectinload(Inventory.film)
            )
            .where(
                Rental.rental_date >= start_date,
                Rental.rental_date <= end_date
            )
            .order_by(Rental.rental_date.desc())
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_rental(self, rental: Rental) -> Rental:
        """
        Create a new rental.
        
        Args:
            rental: Rental instance to create
            
        Returns:
            Created rental
        """
        return await self.create(rental)
    
    async def return_rental(self, rental_id: int, return_date: datetime = None) -> Optional[Rental]:
        """
        Mark a rental as returned.
        
        Args:
            rental_id: Rental ID
            return_date: Return date (defaults to current time)
            
        Returns:
            Updated rental if found, None otherwise
        """
        rental = await self.get_by_id(rental_id)
        if not rental:
            return None
        
        rental.return_date = return_date or datetime.utcnow()
        return await self.update(rental)
    
    async def is_inventory_available(self, inventory_id: int) -> bool:
        """
        Check if an inventory item is available for rental.
        
        Args:
            inventory_id: Inventory ID
            
        Returns:
            True if available, False if currently rented
        """
        active_rental = await self.get_active_rental_for_inventory(inventory_id)
        return active_rental is None 