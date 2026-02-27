from pydantic import BaseModel, Field, ConfigDict
class CountryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    iso2: str = Field(..., min_length=2, max_length=2)
class CountryCreate(CountryBase): pass
class CountryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=120)
    iso2: str | None = Field(None, min_length=2, max_length=2)
class CountryOut(CountryBase):
    id: int
    tenant_id: int
    model_config = ConfigDict(from_attributes=True)
