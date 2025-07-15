"""
Location-related models: Country, City, Address.
"""

from sqlmodel import Field, Relationship
from sqlalchemy import Index, TEXT, Column, TIMESTAMP, INTEGER, ForeignKey
from sqlalchemy.sql import func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from domain.entities.business import Customer, Staff, Store


class Country(Base, table=True):
    __tablename__ = 'country'
    
    country_id: Optional[int] = Field(default=None, primary_key=True)
    country: str = Field(sa_column=Column(TEXT, nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    cities: List["City"] = Relationship(back_populates="country")


class City(Base, table=True):
    __tablename__ = 'city'
    
    city_id: Optional[int] = Field(default=None, primary_key=True)
    city: str = Field(sa_column=Column(TEXT, nullable=False))
    country_id: int = Field(sa_column=Column(INTEGER, ForeignKey("country.country_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    country: Optional[Country] = Relationship(back_populates="cities")
    addresses: List["Address"] = Relationship(back_populates="city")
    
    # Index - matches pagila schema exactly
    __table_args__ = (
        Index('idx_fk_country_id', 'country_id'),
    )


class Address(Base, table=True):
    __tablename__ = 'address'
    
    address_id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(sa_column=Column(TEXT, nullable=False))
    address2: Optional[str] = Field(sa_column=Column(TEXT))
    district: str = Field(sa_column=Column(TEXT, nullable=False))
    city_id: int = Field(sa_column=Column(INTEGER, ForeignKey("city.city_id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False))
    postal_code: Optional[str] = Field(sa_column=Column(TEXT))
    phone: str = Field(sa_column=Column(TEXT, nullable=False))
    last_update: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    
    # Relationships
    city: Optional[City] = Relationship(back_populates="addresses")
    customers: List["Customer"] = Relationship(back_populates="address")
    staff: List["Staff"] = Relationship(back_populates="address")
    stores: List["Store"] = Relationship(back_populates="address")
    
    # Index - matches pagila schema exactly
    __table_args__ = (
        Index('idx_fk_city_id', 'city_id'),
    ) 