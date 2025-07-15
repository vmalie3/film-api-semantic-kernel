"""
Service layer for customer operations.
"""

from typing import Optional, List
from fastapi import Depends

from domain.entities.business import Customer
from domain.repositories.deps import get_customer_repository
from domain.repositories.customer_repository import CustomerRepository

class CustomerService:
    """Service class for customer operations."""
    
    def __init__(self, customer_repository: CustomerRepository = Depends(get_customer_repository)):
        self.customer_repository = customer_repository
    
    async def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Get a customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer if found, None otherwise
        """
        return await self.customer_repository.get_customer_by_id(customer_id)
    
    async def get_customers_by_store(self, store_id: int) -> List[Customer]:
        """
        Get all customers for a specific store.
        
        Args:
            store_id: Store ID
            
        Returns:
            List of customers
        """
        return await self.customer_repository.get_customers_by_store(store_id)
    
    async def search_customers_by_name(self, search_term: str) -> List[Customer]:
        """
        Search customers by name.
        
        Args:
            search_term: Search term for first or last name
            
        Returns:
            List of matching customers
        """
        return await self.customer_repository.search_customers_by_name(search_term)
    
    async def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """
        Get a customer by email address.
        
        Args:
            email: Email address
            
        Returns:
            Customer if found, None otherwise
        """
        return await self.customer_repository.get_customer_by_email(email)
    
    async def get_active_customers(self) -> List[Customer]:
        """
        Get all active customers.
        
        Returns:
            List of active customers
        """
        return await self.customer_repository.get_active_customers()
    
    async def create_customer(self, customer: Customer) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer: Customer instance to create
            
        Returns:
            Created customer
        """
        return await self.customer_repository.create_customer(customer)
    
    async def update_customer(self, customer: Customer) -> Customer:
        """
        Update an existing customer.
        
        Args:
            customer: Customer instance to update
            
        Returns:
            Updated customer
        """
        return await self.customer_repository.update_customer(customer)
    
    async def deactivate_customer(self, customer_id: int) -> Optional[Customer]:
        """
        Deactivate a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Updated customer if found, None otherwise
        """
        return await self.customer_repository.deactivate_customer(customer_id)
    
    async def activate_customer(self, customer_id: int) -> Optional[Customer]:
        """
        Activate a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Updated customer if found, None otherwise
        """
        return await self.customer_repository.activate_customer(customer_id) 