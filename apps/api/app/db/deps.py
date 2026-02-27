from fastapi import Header, HTTPException
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tenant_id(x_tenant_id: int = Header(..., alias="X-Tenant-Id")) -> int:
    if x_tenant_id <= 0:
        raise HTTPException(status_code=400, detail="X-Tenant-Id inválido")
    return x_tenant_id
