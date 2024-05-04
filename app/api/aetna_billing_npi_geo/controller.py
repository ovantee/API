from fastapi import APIRouter, Depends, Path, Request, Body

from app.models.aetna_billing_npi_geo import AetnaSchema, Aetna, ConditionList
from .schema import (
    ReadListConditionAetnaResponse
)
from .business import ReadListAetnaCondition

router = APIRouter(prefix="/query")

@router.post("/aetna", response_model=ReadListConditionAetnaResponse)
async def read(
    request: Request,
    conditions: ConditionList = Body(..., description="List of conditions for querying aetna_billing_npi_geo table"),
    business: ReadListAetnaCondition = Depends(ReadListAetnaCondition),
) -> ReadListConditionAetnaResponse:
    devices = [device async for device in business.execute(conditions)]
    return ReadListConditionAetnaResponse(data=devices)