from fastapi import APIRouter, Depends, Path, Request, Body

from app.models.drug_hcpcs_mftr import DrugSchema, Drug, ConditionList
from .schema import (
    ReadListConditionDrugResponse
)
from .business import ReadListDrugCondition

router = APIRouter(prefix="/query")

@router.post("/drug", response_model=ReadListConditionDrugResponse)
async def read(
    request: Request,
    conditions: ConditionList = Body(..., description="List of conditions for querying drug_hcpcs_mftr table"),
    business: ReadListDrugCondition = Depends(ReadListDrugCondition),
) -> ReadListConditionDrugResponse:
    devices = [device async for device in business.execute(conditions)]
    return ReadListConditionDrugResponse(data=devices)