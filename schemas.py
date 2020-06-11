from datetime import datetime
# from typing import List
from pydantic import BaseModel, Field, Json, PositiveInt


class inputModel(BaseModel):
    v: PositiveInt = Field(..., alias='_v', description="Version")
    timestamp: datetime = Field(..., alias='_timestamp', description="Timestamp (UNIX Epoch)")
    text: str = Field(..., description="Text to parse")
    params: Json = Field(..., description="Raw parameters (Raw json datatype)")


class outputModel(BaseModel):
    v: PositiveInt = Field(..., alias='_v', description="Version")
    timestamp: datetime = Field(..., alias='_timestamp', description="Timestamp (UNIX Epoch)")
    log: Json = Field(..., description="Raw log (Raw json datatype)")
    text: str = Field(..., description="Depersonalized text")
