from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_tenant_id
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut
from app.repositories.country import list_countries, get_country, create_country, update_country, delete_country

router = APIRouter(prefix="/api/v1/countries", tags=["Country"])

@router.get("", response_model=list[CountryOut])
def get_all(q: str | None=None, limit: int=50, offset: int=0, tenant_id: int=Depends(get_tenant_id), db: Session=Depends(get_db)):
    return list_countries(db, tenant_id, q=q, limit=limit, offset=offset)

@router.get("/{country_id}", response_model=CountryOut)
def get_one(country_id: int, tenant_id: int=Depends(get_tenant_id), db: Session=Depends(get_db)):
    obj = get_country(db, tenant_id, country_id)
    if not obj: raise HTTPException(404, "Country não encontrado")
    return obj

@router.post("", response_model=CountryOut, status_code=status.HTTP_201_CREATED)
def create(payload: CountryCreate, tenant_id: int=Depends(get_tenant_id), db: Session=Depends(get_db)):
    return create_country(db, tenant_id, payload)

@router.put("/{country_id}", response_model=CountryOut)
def update(country_id: int, payload: CountryUpdate, tenant_id: int=Depends(get_tenant_id), db: Session=Depends(get_db)):
    obj = update_country(db, tenant_id, country_id, payload)
    if not obj: raise HTTPException(404, "Country não encontrado")
    return obj

@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(country_id: int, tenant_id: int=Depends(get_tenant_id), db: Session=Depends(get_db)):
    if not delete_country(db, tenant_id, country_id):
        raise HTTPException(404, "Country não encontrado")
