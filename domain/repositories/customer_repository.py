"""
Customer repository for customer-related database operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from domain.entities.business import Customer
from .base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Repository for Customer entity with specialized queries."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Customer)
    
    async def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Get a customer by ID with address and store relationships loaded.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer if found, None otherwise
        """
        query = (
            select(Customer)
            .options(
                selectinload(Customer.address),
                selectinload(Customer.store)
            )
            .where(Customer.customer_id == customer_id)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_customers_by_store(self, store_id: int) -> List[Customer]:
        """
        Get all customers for a specific store.
        
        Args:
            store_id: Store ID
            
        Returns:
            List of customers
        """
        query = (
            select(Customer)
            .options(selectinload(Customer.address))
            .where(Customer.store_id == store_id)
            .order_by(Customer.last_name, Customer.first_name)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def search_customers_by_name(self, search_term: str) -> List[Customer]:
        """
        Search customers by first name or last name.
        
        Args:
            search_term: Search term
            
        Returns:
            List of matching customers
        """
        query = (
            select(Customer)
            .options(selectinload(Customer.address))
            .where(
                or_(
                    Customer.first_name.ilike(f"%{search_term}%"),
                    Customer.last_name.ilike(f"%{search_term}%")
                )
            )
            .order_by(Customer.last_name, Customer.first_name)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """
        Get a customer by email address.
        
        Args:
            email: Email address
            
        Returns:
            Customer if found, None otherwise
        """
        query = (
            select(Customer)
            .options(selectinload(Customer.address))
            .where(Customer.email == email)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_active_customers(self) -> List[Customer]:
        """
        Get all active customers.
        
        Returns:
            List of active customers
        """
        query = (
            select(Customer)
            .options(selectinload(Customer.address))
            .where(Customer.activebool == True)
            .order_by(Customer.last_name, Customer.first_name)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_customer(self, customer: Customer) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer: Customer instance to create
            
        Returns:
            Created customer
        """
        return await self.create(customer)
    
    async def update_customer(self, customer: Customer) -> Customer:
        """
        Update an existing customer.
        
        Args:
            customer: Customer instance to update
            
        Returns:
            Updated customer
        """
        return await self.update(customer)
    
    async def deactivate_customer(self, customer_id: int) -> Optional[Customer]:
        """
        Deactivate a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Updated customer if found, None otherwise
        """
        customer = await self.get_by_id(customer_id)
        if not customer:
            return None
        
        customer.activebool = False
        return await self.update(customer)
    
    async def activate_customer(self, customer_id: int) -> Optional[Customer]:
        """
        Activate a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Updated customer if found, None otherwise
        """
        customer = await self.get_by_id(customer_id)
        if not customer:
            return None
        
        customer.activebool = True
        return await self.update(customer) 