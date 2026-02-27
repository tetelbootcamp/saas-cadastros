from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.country import Country
from app.schemas.country import CountryCreate, CountryUpdate

def list_countries(db: Session, tenant_id: int, q: str | None=None, limit: int=50, offset: int=0):
    stmt = select(Country).where(Country.tenant_id==tenant_id)
    if q: stmt = stmt.where(Country.name.ilike(f"%{q}%"))
    return db.execute(stmt.order_by(Country.name).limit(limit).offset(offset)).scalars().all()

def get_country(db: Session, tenant_id: int, country_id: int):
    stmt = select(Country).where(Country.tenant_id==tenant_id, Country.id==country_id)
    return db.execute(stmt).scalars().first()

def create_country(db: Session, tenant_id: int, data: CountryCreate):
    obj = Country(tenant_id=tenant_id, name=data.name, iso2=data.iso2.upper())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def update_country(db: Session, tenant_id: int, country_id: int, data: CountryUpdate):
    obj = get_country(db, tenant_id, country_id)
    if not obj: return None
    if data.name is not None: obj.name = data.name
    if data.iso2 is not None: obj.iso2 = data.iso2.upper()
    db.commit(); db.refresh(obj); return obj

def delete_country(db: Session, tenant_id: int, country_id: int) -> bool:
    obj = get_country(db, tenant_id, country_id)
    if not obj: return False
    db.delete(obj); db.commit(); return True
