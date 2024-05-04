from typing import Annotated, AsyncIterator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db import get_session
from app.models.fact_provider_service import FactProviderServiceSchema, FactProviderService, ConditionList

AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

class ReadListFactCondition:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, conditions: ConditionList) -> AsyncIterator[FactProviderServiceSchema]:
        async with self.async_session() as session:
            facts = FactProviderService.query_data_with_dynamic_conditions(session, conditions)  # Await the coroutine
            async for fact in facts:  # Iterate over the list of devices
                yield FactProviderServiceSchema.from_orm(fact)
