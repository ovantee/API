from fastapi import APIRouter, Depends, Path, Request, Body

from app.models.equi_hcpcs_phys import EquiSchema, Equi, ConditionList
from .schema import (
    ReadListConditionEquiResponse
)
from .business import ReadListEquiCondition

router = APIRouter(prefix="/query")

@router.post("/equi", response_model=ReadListConditionEquiResponse)
async def read(
    request: Request,
    conditions: ConditionList = Body(..., description="List of conditions for querying equi_hcpcs_phys table"),
    business: ReadListEquiCondition = Depends(ReadListEquiCondition),
) -> ReadListConditionEquiResponse:
    devices = [device async for device in business.execute(conditions)]
    return ReadListConditionEquiResponse(data=devices)