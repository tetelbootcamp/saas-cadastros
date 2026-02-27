from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_tenant_id
from app.schemas.city import CityCreate, CityUpdate, CityOut
from app.repositories.city import list_cities, get_city, create_city, update_city, delete_city

router = APIRouter(prefix="/api/v1/cities", tags=["City"])

@router.get("", response_model=list[CityOut])
def get_all(state_id: int | None = None, q: str | None = None, limit: int = 50, offset: int = 0,
            tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    return list_cities(db, tenant_id, state_id=state_id, q=q, limit=limit, offset=offset)

@router.get("/{city_id}", response_model=CityOut)
def get_one(city_id: int, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    obj = get_city(db, tenant_id, city_id)
    if not obj:
        raise HTTPException(status_code=404, detail="City não encontrado")
    return obj

@router.post("", response_model=CityOut, status_code=status.HTTP_201_CREATED)
def create(payload: CityCreate, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    return create_city(db, tenant_id, payload)

@router.put("/{city_id}", response_model=CityOut)
def update(city_id: int, payload: CityUpdate, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    obj = update_city(db, tenant_id, city_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="City não encontrado")
    return obj

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(city_id: int, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    ok = delete_city(db, tenant_id, city_id)
    if not ok:
        raise HTTPException(status_code=404, detail="City não encontrado")
