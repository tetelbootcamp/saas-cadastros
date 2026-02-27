from pydantic import BaseModel, Field, ConfigDict

class StateBase(BaseModel):
    country_id: int
    code: str = Field(..., min_length=2, max_length=2)
    name: str = Field(..., min_length=1, max_length=120)

class StateCreate(StateBase):
    pass

class StateUpdate(BaseModel):
    country_id: int | None = None
    code: str | None = Field(None, min_length=2, max_length=2)
    name: str | None = Field(None, min_length=1, max_length=120)

class StateOut(StateBase):
    id: int
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)
