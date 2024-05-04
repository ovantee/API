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

class Equi(Base):
    __tablename__ = 'equi_hcpcs_phys'

    geo_cd = Column(String, primary_key=True)
    betos_cd = Column(String)
    hcpcs_cd = Column(String)
    suplr_rentl_ind = Column(String)
    tot_rfrg_prvdrs = Column(Integer)
    tot_suplrs = Column(Integer)
    tot_suplr_benes = Column(Integer)
    tot_suplr_clms = Column(Integer)
    tot_suplr_srvcs = Column(Integer)
    avg_suplr_sbmtd_chrg = Column(Float)
    avg_suplr_mdcr_alowd_amt = Column(Float)
    avg_suplr_mdcr_pymt_amt = Column(Float)
    avg_suplr_mdcr_stdzd_amt = Column(Float)
    year = Column(Integer)
    rfrg_npi = Column(Integer)
    type_ = Column(Text)
    betos_desc = Column(String)
    betos_lvl = Column(String)
    state_name = Column(String)
    state_abrvtn = Column(String)
    region = Column(String)
    country = Column(Text)
    hcpcs_desc = Column(String)
    apc_cd = Column(Integer)
    physician_npi = Column(Integer)
    physician_name = Column(Text)
    physician_ent_cd = Column(String)
    physician_type = Column(String)
    physician_prvdr_crdntls = Column(String)
    physician_gndr = Column(String)
    physician_nation_cat = Column(Text)
    physician_cntry = Column(String)
    physician_state_abrvtn = Column(String)
    physician_city = Column(String)
    physician_zip5 = Column(String)
    physician_st1 = Column(String)
    physician_st2 = Column(Text)
    physician_ruca_cd = Column(Float)
    physician_prtcptg_ind = Column(String)
    physician_ruca_cd_new = Column(String)
    ruca_cd = Column(Float)
    ruca_desc = Column(String)
    ruca_cat = Column(String)
    ruca_cd_new = Column(String)

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Equi]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.limit(page_size).offset(offset).order_by(cls.betos_cd))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, betos_cd: int) -> Optional[Equi]:
        stmt = select(cls).where(cls.betos_cd == betos_cd)
        return await session.scalar(stmt.order_by(cls.betos_cd))

    @classmethod
    async def query_data_with_dynamic_conditions(cls, session: AsyncSession, conditions: ConditionList) -> \
            AsyncIterator[Equi]:
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
class EquiSchema(BaseModel):
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