from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_tenant_id
from app.schemas.state import StateCreate, StateUpdate, StateOut
from app.repositories.state import list_states, get_state, create_state, update_state, delete_state

router = APIRouter(prefix="/api/v1/states", tags=["State"])

@router.get("", response_model=list[StateOut])
def get_all(country_id: int | None = None, q: str | None = None, limit: int = 50, offset: int = 0,
            tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    return list_states(db, tenant_id, country_id=country_id, q=q, limit=limit, offset=offset)

@router.get("/{state_id}", response_model=StateOut)
def get_one(state_id: int, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    obj = get_state(db, tenant_id, state_id)
    if not obj:
        raise HTTPException(status_code=404, detail="State não encontrado")
    return obj

@router.post("", response_model=StateOut, status_code=status.HTTP_201_CREATED)
def create(payload: StateCreate, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    return create_state(db, tenant_id, payload)

@router.put("/{state_id}", response_model=StateOut)
def update(state_id: int, payload: StateUpdate, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    obj = update_state(db, tenant_id, state_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="State não encontrado")
    return obj

@router.delete("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(state_id: int, tenant_id: int = Depends(get_tenant_id), db: Session = Depends(get_db)):
    ok = delete_state(db, tenant_id, state_id)
    if not ok:
        raise HTTPException(status_code=404, detail="State não encontrado")
