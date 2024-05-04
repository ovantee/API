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

class Drug(Base):
    __tablename__ = 'drug_hcpcs_mftr'

    hcpcs_mftr_cd = Column(Integer, primary_key=True)
    drug_brand_code = Column(Integer)
    year = Column(Integer)
    tot_spndng = Column(Float)
    tot_dsg_unts = Column(Float)
    tot_clms = Column(Integer)
    tot_benes = Column(Float)
    avg_spnd_per_dsg_unt_wghtd = Column(Float)
    avg_spnd_per_clm = Column(Float)
    avg_spnd_per_bene = Column(Float)
    outlier_flag = Column(Integer)
    category = Column(String(50))
    desc_ = Column(String(50))
    drug_brnd_cd = Column(Integer)
    drug_brnd_name = Column(String(50))
    drug_gnrc_name = Column(String(50))

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Drug]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.limit(page_size).offset(offset).order_by(cls.hcpcs_mftr_cd))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, hcpcs_mftr_cd: int) -> Optional[Drug]:
        stmt = select(cls).where(cls.hcpcs_mftr_cd == hcpcs_mftr_cd)
        return await session.scalar(stmt.order_by(cls.hcpcs_mftr_cd))

    @classmethod
    async def query_data_with_dynamic_conditions(cls, session: AsyncSession, conditions: ConditionList) -> \
            AsyncIterator[Drug]:
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
class DrugSchema(BaseModel):
    hcpcs_mftr_cd: Optional[int]
    drug_brand_code: Optional[int]
    year: Optional[int]
    tot_spndng: Optional[float]
    tot_dsg_unts: Optional[float]
    tot_clms: Optional[int]
    tot_benes: Optional[float]
    avg_spnd_per_dsg_unt_wghtd: Optional[float]
    avg_spnd_per_clm: Optional[float]
    avg_spnd_per_bene: Optional[float]
    outlier_flag: Optional[int]
    category: Optional[str]
    desc_: Optional[str]
    drug_brnd_cd: Optional[int]
    drug_brnd_name: Optional[str]
    drug_gnrc_name: Optional[str]

    class Config:
        orm_mode = True