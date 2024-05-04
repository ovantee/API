from fastapi import APIRouter, Depends, Path, Request, Body

from app.models.fact_provider_service import ConditionList

from .schema import (
    ReadListConditionFactResponse
)
from .business import  ReadListFactCondition

router = APIRouter(prefix="/query")

@router.post("/fact_provider", response_model=ReadListConditionFactResponse)
async def read(
    request: Request,
    conditions: ConditionList = Body(..., description="List of conditions for querying fact_provider_service table"),
    business: ReadListFactCondition = Depends(ReadListFactCondition),
) -> ReadListConditionFactResponse:
    devices = [device async for device in business.execute(conditions)]
    return ReadListConditionFactResponse(data=devices)