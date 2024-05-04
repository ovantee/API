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

class FactProviderService(Base):
    __tablename__ = 'fact_provider_service'

    geo_cd = Column(String, primary_key=True, nullable=False)
    service_id = Column(String)
    city = Column(String)
    provider_id = Column(String)
    avg_sbmtd_chrg = Column(Float)
    avg_mdcr_alowd_amt = Column(Float)
    avg_mdcr_pymt_amt = Column(Float)
    year = Column(Integer)
    category = Column(Text)
    type_ = Column(Text)
    state_name = Column(String(256))
    state_abrvtn = Column(String(2))
    region = Column(String(50))
    country = Column(Text)
    service_name = Column(String)
    service_type = Column(Text)
    prvdr_ccn = Column(String)
    prvdr_name = Column(String)
    prvdr_st = Column(String(256))
    prvdr_city = Column(String(256))
    ruca_cd = Column(Float)
    ruca_desc = Column(String(256))
    ruca_cat = Column(String(256))
    ruca_cd_new = Column(String(10))

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[FactProviderService]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.limit(page_size).offset(offset).order_by(cls.geo_cd))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, geo_cd: int) -> Optional[FactProviderService]:
        stmt = select(cls).where(cls.geo_cd == geo_cd)
        return await session.scalar(stmt.order_by(cls.geo_cd))

    @classmethod
    async def query_data_with_dynamic_conditions(cls, session: AsyncSession, conditions: ConditionList) -> \
            AsyncIterator[FactProviderService]:
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
class FactProviderServiceSchema(BaseModel):
    geo_cd: Optional[str]
    service_id: Optional[str]
    city: Optional[str]
    provider_id: Optional[str]
    avg_sbmtd_chrg: Optional[float]
    avg_mdcr_alowd_amt: Optional[float]
    avg_mdcr_pymt_amt: Optional[float]
    year: Optional[int]
    category: Optional[str]
    type_: Optional[str]
    state_name: Optional[str]
    state_abrvtn: Optional[str]
    region: Optional[str]
    country: Optional[str]
    service_name: Optional[str]
    service_type: Optional[str]
    prvdr_ccn: Optional[str]
    prvdr_name: Optional[str]
    prvdr_st: Optional[str]
    prvdr_city: Optional[str]
    ruca_cd: Optional[float]
    ruca_desc: Optional[str]
    ruca_cat: Optional[str]
    ruca_cd_new: Optional[str]

    class Config:
        orm_mode = True