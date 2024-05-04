from __future__ import annotations

from pydantic import BaseModel

from app.models.agg_cost import AggSchema
class ReadListConditionAggResponse(BaseModel):
    data: list[AggSchema]