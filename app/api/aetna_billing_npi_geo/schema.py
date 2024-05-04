from __future__ import annotations

from pydantic import BaseModel

from app.models.aetna_billing_npi_geo import AetnaSchema
class ReadListConditionAetnaResponse(BaseModel):
    data: list[AetnaSchema]