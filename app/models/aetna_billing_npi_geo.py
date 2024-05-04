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

class Aetna(Base):
    __tablename__ = 'aetna_billing_npi_geo'

    billing_code = Column(String(256), primary_key=True)
    provider_group_id = Column(Integer)
    service_code = Column(String(256))
    negotiation_arrangement = Column(String)
    billing_class = Column(String(256))
    billing_code_modifier = Column(String(256))
    expiration_date = Column(String(256))
    negotiated_rate = Column(String(256))
    negotiated_type = Column(String(256))
    npi = Column(String(256))
    type = Column(String(256))
    value = Column(Float)
    year = Column(Integer)
    billing_code_type = Column(String(256))
    billing_code_type_version = Column(Integer)
    description = Column(String(256))
    name = Column(String(256))
    prvd_name = Column(Text)
    prvd_type = Column(Text)
    prvd_credential = Column(String(256))
    prvd_mailing_address_city = Column(String(256))
    prvd_mailing_address_state = Column(String(256))
    prvd_mailing_address_postal = Column(String(256))
    prvd_first_line_practice_address = Column(String(256))
    prvd_second_line_practice_address = Column(String(256))
    npi_deact_reason_cd = Column(Float)
    npi_deact_date = Column(String(256))
    npi_react_date = Column(String(256))
    prvd_gender_cd = Column(String(256))
    cert_date = Column(String(256))
    geo_cd = Column(String(256))
    state_name = Column(String(256))
    state_abrvtn = Column(String(2))
    region = Column(String(50))
    country = Column(Text)

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Aetna]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.limit(page_size).offset(offset).order_by(cls.billing_code))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, billing_code: int) -> Optional[Aetna]:
        stmt = select(cls).where(cls.billing_code == billing_code)
        return await session.scalar(stmt.order_by(cls.billing_code))

    @classmethod
    async def query_data_with_dynamic_conditions(cls, session: AsyncSession, conditions: ConditionList) -> \
            AsyncIterator[Aetna]:
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
class AetnaSchema(BaseModel):
    billing_code: Optional[str]
    provider_group_id: Optional[int]
    service_code: Optional[str]
    negotiation_arrangement: Optional[str]
    billing_class: Optional[str]
    billing_code_modifier: Optional[str]
    expiration_date: Optional[str]
    negotiated_rate: Optional[str]
    negotiated_type: Optional[str]
    npi: Optional[str]
    type: Optional[str]
    value: Optional[float]
    year: Optional[int]
    billing_code_type: Optional[str]
    billing_code_type_version: Optional[int]
    description: Optional[str]
    name: Optional[str]
    prvd_name: Optional[str]
    prvd_type: Optional[str]
    prvd_credential: Optional[str]
    prvd_mailing_address_city: Optional[str]
    prvd_mailing_address_state: Optional[str]
    prvd_mailing_address_postal: Optional[str]
    prvd_first_line_practice_address: Optional[str]
    prvd_second_line_practice_address: Optional[str]
    npi_deact_reason_cd: Optional[float]
    npi_deact_date: Optional[str]
    npi_react_date: Optional[str]
    prvd_gender_cd: Optional[str]
    cert_date: Optional[str]
    geo_cd: Optional[str]
    state_name: Optional[str]
    state_abrvtn: Optional[str]
    region: Optional[str]
    country: Optional[str]

    class Config:
        orm_mode = True