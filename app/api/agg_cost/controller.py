from fastapi import APIRouter, Depends, Path, Request, Body

from app.models.agg_cost import AggSchema, Agg, ConditionList
from .schema import (
    ReadListConditionAggResponse
)
from .business import ReadListAggCondition

router = APIRouter(prefix="/query")

@router.post("/agg_cost", response_model=ReadListConditionAggResponse)
async def read(
    request: Request,
    conditions: ConditionList = Body(..., description="List of conditions for querying Agg_cost table"),
    business: ReadListAggCondition = Depends(ReadListAggCondition),
) -> ReadListConditionAggResponse:
    devices = [device async for device in business.execute(conditions)]
    return ReadListConditionAggResponse(data=devices)