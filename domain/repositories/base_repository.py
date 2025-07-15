"""
Base repository class providing common database operations for SQLModel.
"""

import time
from typing import Optional, List, Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel
from core.logging import get_logger, log_database_operation

T = TypeVar('T', bound=SQLModel)


class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations for SQLModel."""
    
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
    
    def _get_primary_key_name(self) -> str:
        """Get the primary key field name for the model."""
        table = self.model.__table__
        if table is not None and len(table.primary_key.columns) > 0:
            return list(table.primary_key.columns)[0].name
        return f"{self.model.__tablename__}_id"
    
    async def get_by_id(self, id: int, load_relationships: List[str] = None) -> Optional[T]:
        """
        Get a single record by ID.
        
        Args:
            id: Record ID
            load_relationships: List of relationship names to eagerly load
            
        Returns:
            Record if found, None otherwise
        """
        start_time = time.time()
        
        try:
            pk_name = self._get_primary_key_name()
            query = select(self.model).where(getattr(self.model, pk_name) == id)
            
            if load_relationships:
                for relationship in load_relationships:
                    query = query.options(selectinload(getattr(self.model, relationship)))
            
            result = await self.db.execute(query)
            record = result.scalar_one_or_none()
            
            duration = time.time() - start_time
            log_database_operation(
                logger=self.logger,
                operation="SELECT",
                table=self.model.__tablename__,
                duration=duration,
                record_id=id,
                found=record is not None
            )
            
            return record
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="SELECT",
                table=self.model.__tablename__,
                record_id=id,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def get_all(self, skip: int = 0, limit: int = 100, load_relationships: List[str] = None) -> List[T]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            load_relationships: List of relationship names to eagerly load
            
        Returns:
            List of records
        """
        start_time = time.time()
        
        try:
            query = select(self.model).offset(skip).limit(limit)
            
            if load_relationships:
                for relationship in load_relationships:
                    query = query.options(selectinload(getattr(self.model, relationship)))
            
            result = await self.db.execute(query)
            records = result.scalars().all()
            
            duration = time.time() - start_time
            log_database_operation(
                logger=self.logger,
                operation="SELECT",
                table=self.model.__tablename__,
                duration=duration,
                skip=skip,
                limit=limit,
                count=len(records)
            )
            
            return records
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="SELECT",
                table=self.model.__tablename__,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def count(self) -> int:
        """
        Get total count of records.
        
        Returns:
            Total count
        """
        start_time = time.time()
        
        try:
            pk_name = self._get_primary_key_name()
            query = select(func.count(getattr(self.model, pk_name)))
            result = await self.db.execute(query)
            count = result.scalar()
            
            duration = time.time() - start_time
            log_database_operation(
                logger=self.logger,
                operation="COUNT",
                table=self.model.__tablename__,
                duration=duration,
                count=count
            )
            
            return count
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="COUNT",
                table=self.model.__tablename__,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def create(self, instance: T) -> T:
        """
        Create a new record.
        
        Args:
            instance: Instance to create
            
        Returns:
            Created instance
        """
        start_time = time.time()
        
        try:
            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)
            
            duration = time.time() - start_time
            pk_name = self._get_primary_key_name()
            record_id = getattr(instance, pk_name, None)
            
            log_database_operation(
                logger=self.logger,
                operation="INSERT",
                table=self.model.__tablename__,
                duration=duration,
                record_id=record_id
            )
            
            return instance
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="INSERT",
                table=self.model.__tablename__,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def update(self, instance: T) -> T:
        """
        Update an existing record.
        
        Args:
            instance: Instance to update
            
        Returns:
            Updated instance
        """
        start_time = time.time()
        
        try:
            await self.db.commit()
            await self.db.refresh(instance)
            
            duration = time.time() - start_time
            pk_name = self._get_primary_key_name()
            record_id = getattr(instance, pk_name, None)
            
            log_database_operation(
                logger=self.logger,
                operation="UPDATE",
                table=self.model.__tablename__,
                duration=duration,
                record_id=record_id
            )
            
            return instance
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="UPDATE",
                table=self.model.__tablename__,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def delete(self, instance: T) -> bool:
        """
        Delete a record.
        
        Args:
            instance: Instance to delete
            
        Returns:
            True if deleted successfully
        """
        start_time = time.time()
        
        try:
            pk_name = self._get_primary_key_name()
            record_id = getattr(instance, pk_name, None)
            
            await self.db.delete(instance)
            await self.db.commit()
            
            duration = time.time() - start_time
            log_database_operation(
                logger=self.logger,
                operation="DELETE",
                table=self.model.__tablename__,
                duration=duration,
                record_id=record_id
            )
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="DELETE",
                table=self.model.__tablename__,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def delete_by_id(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID to delete
            
        Returns:
            True if deleted successfully
        """
        start_time = time.time()
        
        try:
            pk_name = self._get_primary_key_name()
            query = delete(self.model).where(getattr(self.model, pk_name) == id)
            result = await self.db.execute(query)
            await self.db.commit()
            
            deleted = result.rowcount > 0
            
            duration = time.time() - start_time
            log_database_operation(
                logger=self.logger,
                operation="DELETE",
                table=self.model.__tablename__,
                duration=duration,
                record_id=id,
                deleted=deleted
            )
            
            return deleted
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="DELETE",
                table=self.model.__tablename__,
                record_id=id,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise
    
    async def exists(self, id: int) -> bool:
        """
        Check if a record exists by ID.
        
        Args:
            id: Record ID to check
            
        Returns:
            True if record exists
        """
        start_time = time.time()
        
        try:
            pk_name = self._get_primary_key_name()
            query = select(func.count(getattr(self.model, pk_name))).where(
                getattr(self.model, pk_name) == id
            )
            result = await self.db.execute(query)
            exists = result.scalar() > 0
            
            duration = time.time() - start_time
            log_database_operation(
                logger=self.logger,
                operation="EXISTS",
                table=self.model.__tablename__,
                duration=duration,
                record_id=id,
                exists=exists
            )
            
            return exists
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                "Database operation failed",
                operation="EXISTS",
                table=self.model.__tablename__,
                record_id=id,
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True
            )
            raise 