from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import JSON, String, select, TIMESTAMP, Column, Integer
from sqlalchemy.sql import func, and_, between
from datetime import datetime

from .base import Base

class AppConfigData(Base):
    __tablename__ = 'app_configs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
    

    @classmethod
    async def read_by_key(cls, session: AsyncSession, key: str) -> Optional[AppConfigData]:
        stmt = select(cls).where(cls.key == key)
        return await session.scalar(stmt.order_by(cls.id))

class AppConfigDataSchema(BaseModel):
    id: int
    name: str
    key: str
    value: list = []
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True