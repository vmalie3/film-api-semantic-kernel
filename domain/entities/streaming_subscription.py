"""
Streaming subscription model.
"""

from sqlmodel import Field, Relationship
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import Column, INTEGER, ForeignKey
from typing import Optional, TYPE_CHECKING
from datetime import date

from .base import Base

if TYPE_CHECKING:
    from domain.entities.business import Customer


class StreamingSubscription(Base, table=True):
    __tablename__ = 'streaming_subscription'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(sa_column=Column(INTEGER, ForeignKey("customer.customer_id"), nullable=False))
    plan_name: str = Field(max_length=100, nullable=False)
    start_date: date = Field(nullable=False)
    end_date: Optional[date] = Field(default=None)
    
    # Relationships
    customer: Optional["Customer"] = Relationship(
        back_populates="streaming_subscriptions",
        sa_relationship=RelationshipProperty("Customer", primaryjoin="StreamingSubscription.customer_id == Customer.customer_id")
    )
