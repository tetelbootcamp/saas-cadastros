from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate

def list_cities(db: Session, tenant_id: int, state_id: int | None = None, q: str | None = None, limit: int = 50, offset: int = 0):
    stmt = select(City).where(City.tenant_id == tenant_id)
    if state_id is not None:
        stmt = stmt.where(City.state_id == state_id)
    if q:
        stmt = stmt.where(City.name.ilike(f"%{q}%"))
    return db.execute(stmt.order_by(City.name).limit(limit).offset(offset)).scalars().all()

def get_city(db: Session, tenant_id: int, city_id: int):
    stmt = select(City).where(City.tenant_id == tenant_id, City.id == city_id)
    return db.execute(stmt).scalars().first()

def create_city(db: Session, tenant_id: int, data: CityCreate):
    obj = City(
        tenant_id=tenant_id,
        state_id=data.state_id,
        name=data.name,
        ibge_code=data.ibge_code,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_city(db: Session, tenant_id: int, city_id: int, data: CityUpdate):
    obj = get_city(db, tenant_id, city_id)
    if not obj:
        return None
    if data.state_id is not None:
        obj.state_id = data.state_id
    if data.name is not None:
        obj.name = data.name
    if data.ibge_code is not None:
        obj.ibge_code = data.ibge_code
    db.commit()
    db.refresh(obj)
    return obj

def delete_city(db: Session, tenant_id: int, city_id: int) -> bool:
    obj = get_city(db, tenant_id, city_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
