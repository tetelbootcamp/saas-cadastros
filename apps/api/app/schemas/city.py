from pydantic import BaseModel, Field, ConfigDict

class CityBase(BaseModel):
    state_id: int
    name: str = Field(..., min_length=1, max_length=120)
    ibge_code: str | None = Field(None, max_length=10)

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    state_id: int | None = None
    name: str | None = Field(None, min_length=1, max_length=120)
    ibge_code: str | None = Field(None, max_length=10)

class CityOut(CityBase):
    id: int
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)
