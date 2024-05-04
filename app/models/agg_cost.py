from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey, String, select, TIMESTAMP, Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_
from typing import Any, List, Optional, Tuple
from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

Base = declarative_base()
class Condition(BaseModel):
    field: str
    operator: str
    value: Any

class ConditionList(BaseModel):
    conditions: List[Tuple[str, str, Any]]
    limit: Optional[int] = None
    offset: Optional[int] = None
    page: Optional[int] = None

class Agg(Base):
    __tablename__ = 'agg_cost'

    id = Column(Text, primary_key=True)
    year = Column(Integer)
    service_category = Column(Text)
    service_id = Column(String)
    service_name = Column(Text)
    state_abrvtn = Column(String)
    state_name = Column(String)
    country = Column(Text)
    provider_id = Column(String)
    provider_name = Column(String)
    provider_city = Column(String)
    provider_entity = Column(String)
    payer_name = Column(Text)
    avg_submitted_charge = Column(Float)
    avg_medicare_allowed = Column(Float)
    avg_medicare_payment = Column(Float)
    avg_payer_negotiated_fee = Column(Float)
    avg_payer_negotiated_cost = Column(Float)
    avg_payer_negotiated_perdiem = Column(Float)
    avg_payer_negotiated_percent = Column(Float)
    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Equi]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.limit(page_size).offset(offset).order_by(cls.betos_cd))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, id: int) -> Optional[Agg]:
        stmt = select(cls).where(cls.id == id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def query_data_with_dynamic_conditions(cls, session: AsyncSession, conditions: ConditionList) -> \
            AsyncIterator[Agg]:
        offset = (conditions.page - 1) * conditions.limit if conditions.page and conditions.limit else 0
        stmt = select(cls)

        for condition in conditions.conditions:
            column, operator, value = condition
            if operator == "==":
                stmt = stmt.where(getattr(cls, column) == value)
            elif operator == "!=":
                stmt = stmt.where(getattr(cls, column) != value)
            elif operator == "<":
                stmt = stmt.where(getattr(cls, column) < value)
            elif operator == "<=":
                stmt = stmt.where(getattr(cls, column) <= value)
            elif operator == ">":
                stmt = stmt.where(getattr(cls, column) > value)
            elif operator == ">=":
                stmt = stmt.where(getattr(cls, column) >= value)
            elif operator == "is_not":
                stmt = stmt.where(getattr(cls, column).isnot(value))
        # Apply limit and offset for pagination
        stmt = stmt.limit(conditions.limit) if conditions.limit else stmt
        stmt = stmt.offset(offset) if conditions.offset else stmt

        result = await session.stream(stmt)
        async for row in result.scalars():
            yield row
class AggSchema(BaseModel):
    id: Optional[str]
    year: Optional[int]
    service_category: Optional[str]
    service_id: Optional[str]
    service_name: Optional[str]
    state_abrvtn: Optional[str]
    state_name: Optional[str]
    country: Optional[str]
    provider_id: Optional[str]
    provider_name: Optional[str]
    provider_city: Optional[str]
    provider_entity: Optional[str]
    payer_name: Optional[str]
    avg_submitted_charge: Optional[float]
    avg_medicare_allowed: Optional[float]
    avg_medicare_payment: Optional[float]
    avg_payer_negotiated_fee: Optional[float]
    avg_payer_negotiated_cost: Optional[float]
    avg_payer_negotiated_perdiem: Optional[float]
    avg_payer_negotiated_percent: Optional[float]

    class Config:
        orm_mode = True