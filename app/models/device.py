from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey, String, select, TIMESTAMP, Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from .base import Base

# Define the pagination parameters
page_number = 1  # The page number you want to retrieve
page_size = 300   # The number of items per page

# Calculate the offset based on the page number and page size
offset = (page_number - 1) * page_size


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    request_id = Column(String, nullable=False)
    device_sn = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    connect_status = Column(Integer, nullable=False, default=1)
    collection_time = Column(Integer, nullable=True)
    station_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, default=None, onupdate=func.now())

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Device]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.limit(page_size).offset(offset).order_by(cls.id))
        async for row in stream:
            yield row


class DeviceSchema(BaseModel):
    id: int
    request_id: str
    device_sn: str
    device_id: str
    device_type: str
    connect_status: int
    collection_time: int
    station_id: int = None
    created_at: datetime
    updated_at: datetime = None

    class Config:
        orm_mode = True