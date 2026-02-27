from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.state import State
from app.schemas.state import StateCreate, StateUpdate

def list_states(db: Session, tenant_id: int, country_id: int | None = None, q: str | None = None, limit: int = 50, offset: int = 0):
    stmt = select(State).where(State.tenant_id == tenant_id)
    if country_id is not None:
        stmt = stmt.where(State.country_id == country_id)
    if q:
        stmt = stmt.where(State.name.ilike(f"%{q}%"))
    return db.execute(stmt.order_by(State.name).limit(limit).offset(offset)).scalars().all()

def get_state(db: Session, tenant_id: int, state_id: int):
    stmt = select(State).where(State.tenant_id == tenant_id, State.id == state_id)
    return db.execute(stmt).scalars().first()

def create_state(db: Session, tenant_id: int, data: StateCreate):
    obj = State(
        tenant_id=tenant_id,
        country_id=data.country_id,
        code=data.code.upper(),
        name=data.name,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_state(db: Session, tenant_id: int, state_id: int, data: StateUpdate):
    obj = get_state(db, tenant_id, state_id)
    if not obj:
        return None
    if data.country_id is not None:
        obj.country_id = data.country_id
    if data.code is not None:
        obj.code = data.code.upper()
    if data.name is not None:
        obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj

def delete_state(db: Session, tenant_id: int, state_id: int) -> bool:
    obj = get_state(db, tenant_id, state_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
