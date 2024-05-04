from __future__ import annotations

from pydantic import BaseModel

from app.models.equi_hcpcs_phys import EquiSchema
class ReadListConditionEquiResponse(BaseModel):
    data: list[EquiSchema]