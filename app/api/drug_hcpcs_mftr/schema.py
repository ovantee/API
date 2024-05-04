from __future__ import annotations

from pydantic import BaseModel

from app.models.drug_hcpcs_mftr import DrugSchema
class ReadListConditionDrugResponse(BaseModel):
    data: list[DrugSchema]