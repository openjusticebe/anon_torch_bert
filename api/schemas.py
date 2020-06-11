from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, Json, PositiveInt


class inputSchema(BaseModel):
    v: PositiveInt = Field(..., alias='_v', description="Version")
    timestamp: datetime = Field(..., alias='_timestamp', description="Timestamp (UNIX Epoch)")
    text: str = Field(..., description="Text to parse")
    params: Json = Field(..., description="Raw parameters (Raw json datatype)")

    class Config:
        schema_extra = {
            'example': {
                '_v': 1,
                '_timestamp': 1239120938,
                'text': 'La Tragique histoire d\'Hamlet, prince de Danemark, plus couramment désigné sous le titre abrégé Hamlet',
                'params': '{}'
            }}


class entitySchema(BaseModel):
    group: str = Field(..., description="Word group")
    family: str = Field(..., description="Entity Family")


class outputSchema(BaseModel):
    v: PositiveInt = Field(..., alias='_v', description="Version")
    timestamp: datetime = Field(..., alias='_timestamp', description="Timestamp (UNIX Epoch)")
    # log: Json = Field(..., description="Raw log (Raw json datatype)")
    # text: str = Field(..., description="Depersonalized text")
    entities: List[entitySchema] = Field(..., description="List of entities")

    class Config:
        schema_extra = {
            'example': {
                '_v': 1,
                '_timestamp': 1239120938,
                'entities': [{
                    'group': 'Hamlet',
                    'family': 'PER'
                }]
            }}
