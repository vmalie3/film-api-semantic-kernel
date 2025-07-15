"""
Business-related models: Store, Staff, Customer, Inventory, Rental, Payment.
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import Index, LargeBinary, Column, TIMESTAMP, TEXT, NUMERIC, INTEGER, ForeignKey
from sqlalchemy.sql import func
from typing import Optional, List, TYPE_CHECKING, Any
from datetime import date, datetime

from .base import Base

if TYPE_CHECKING:
    from domain.entities.location import Address
    from domain.entities.film import Film
    from domain.entities.streaming_subscription import StreamingSubscription


class Store(Base, table=True):
    __tablename__ = 'store'
    
    store_id: Optional[int] = Field(default=None, primary_key=True)
    manager_staff_id: int = Field(nullable=False)
    address_id: int = Field(sa_column=Column(INTEGER, ForeignKey("address.address_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    address: Optional["Address"] = Relationship(back_populates="stores")
    staff: List["Staff"] = Relationship(back_populates="store")
    customers: List["Customer"] = Relationship(back_populates="store")
    inventory: List["Inventory"] = Relationship(back_populates="store")
    # Note: manager relationship removed - no FK in original schema
    
    # Index - matches pagila schema exactly (UNIQUE index)
    __table_args__ = (
        Index('idx_unq_manager_staff_id', 'manager_staff_id', unique=True),
    )


class Staff(Base, table=True):
    __tablename__ = 'staff'
    
    staff_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=Column(TEXT, nullable=False))
    last_name: str = Field(sa_column=Column(TEXT, nullable=False))
    address_id: int = Field(sa_column=Column(INTEGER, ForeignKey("address.address_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    email: Optional[str] = Field(sa_column=Column(TEXT))
    store_id: int = Field(sa_column=Column(INTEGER, ForeignKey("store.store_id"), nullable=False))
    active: bool = Field(default=True, nullable=False)
    username: str = Field(sa_column=Column(TEXT, nullable=False))
    password: Optional[str] = Field(sa_column=Column(TEXT))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    picture: Optional[bytes] = Field(sa_column=Column(LargeBinary))  # bytea in PostgreSQL
    
    # Relationships
    address: Optional["Address"] = Relationship(back_populates="staff")
    store: Optional[Store] = Relationship(back_populates="staff")
    rentals: List["Rental"] = Relationship(back_populates="staff")
    payments: List["Payment"] = Relationship(
        back_populates="staff",
        sa_relationship=RelationshipProperty("Payment", primaryjoin="Staff.staff_id == foreign(Payment.staff_id)")
    )
    # Note: managed_store relationship removed - no FK in original schema


class Customer(Base, table=True):
    __tablename__ = 'customer'
    
    customer_id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(sa_column=Column(INTEGER, ForeignKey("store.store_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    first_name: str = Field(sa_column=Column(TEXT, nullable=False))
    last_name: str = Field(sa_column=Column(TEXT, nullable=False))
    email: Optional[str] = Field(sa_column=Column(TEXT))
    address_id: int = Field(sa_column=Column(INTEGER, ForeignKey("address.address_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    activebool: bool = Field(default=True, nullable=False)
    create_date: date = Field(default_factory=lambda: func.current_date(), nullable=False)
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now()))
    active: Optional[int] = Field(default=None)
    
    # Relationships
    store: Optional[Store] = Relationship(back_populates="customers")
    address: Optional["Address"] = Relationship(back_populates="customers")
    rentals: List["Rental"] = Relationship(back_populates="customer")
    streaming_subscriptions: List["StreamingSubscription"] = Relationship(back_populates="customer")
    payments: List["Payment"] = Relationship(
        back_populates="customer",
        sa_relationship=RelationshipProperty("Payment", primaryjoin="Customer.customer_id == foreign(Payment.customer_id)")
    )
    
    # Indexes - match pagila schema exactly
    __table_args__ = (
        Index('idx_fk_store_id', 'store_id'),
        Index('idx_fk_address_id', 'address_id'),
        Index('idx_last_name', 'last_name'),
    )


class Inventory(Base, table=True):
    __tablename__ = 'inventory'
    
    inventory_id: Optional[int] = Field(default=None, primary_key=True)
    film_id: int = Field(sa_column=Column(INTEGER, ForeignKey("film.film_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    store_id: int = Field(sa_column=Column(INTEGER, ForeignKey("store.store_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    film: Optional["Film"] = Relationship(back_populates="inventory")
    store: Optional[Store] = Relationship(back_populates="inventory")
    rentals: List["Rental"] = Relationship(back_populates="inventory")
    
    # Index - matches pagila schema exactly
    __table_args__ = (
        Index('idx_store_id_film_id', 'store_id', 'film_id'),
    )


class Rental(Base, table=True):
    __tablename__ = 'rental'
    
    rental_id: Optional[int] = Field(default=None, primary_key=True)
    rental_date: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
    inventory_id: int = Field(sa_column=Column(INTEGER, ForeignKey("inventory.inventory_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    customer_id: int = Field(sa_column=Column(INTEGER, ForeignKey("customer.customer_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    return_date: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    staff_id: int = Field(sa_column=Column(INTEGER, ForeignKey("staff.staff_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    inventory: Optional[Inventory] = Relationship(back_populates="rentals")
    customer: Optional[Customer] = Relationship(back_populates="rentals")
    staff: Optional[Staff] = Relationship(back_populates="rentals")
    payment: Optional["Payment"] = Relationship(
        back_populates="rental",
        sa_relationship=RelationshipProperty("Payment", primaryjoin="Rental.rental_id == foreign(Payment.rental_id)")
    )
    
    # Indexes - match pagila schema exactly
    __table_args__ = (
        Index('idx_fk_inventory_id', 'inventory_id'),
        Index('idx_unq_rental_rental_date_inventory_id_customer_id', 'rental_date', 'inventory_id', 'customer_id', unique=True),
    )


class Payment(Base, table=True):
    __tablename__ = 'payment'
    
    payment_id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(nullable=False)
    staff_id: int = Field(nullable=False)
    rental_id: int = Field(nullable=False)
    amount: float = Field(sa_column=Column(NUMERIC(5, 2), nullable=False))
    payment_date: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, primary_key=True))
    
    
    # Note: This table is partitioned by payment_date in PostgreSQL
    # The partitioning is handled at the database level, not in SQLAlchemy 