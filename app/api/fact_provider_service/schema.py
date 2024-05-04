from __future__ import annotations

from pydantic import BaseModel

from app.models.fact_provider_service import FactProviderServiceSchema
#Fact table
class ReadListConditionFactResponse(BaseModel):
    data: list[FactProviderServiceSchema]