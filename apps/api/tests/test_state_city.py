from fastapi.testclient import TestClient
from sqlalchemy import delete
from app.main import app
from app.db.session import SessionLocal
from app.models.country import Country
from app.models.state import State
from app.models.city import City

client = TestClient(app)
H = {"X-Tenant-Id": "1"}

def cleanup():
    with SessionLocal() as db:
        db.execute(delete(City).where(City.tenant_id == 1))
        db.execute(delete(State).where(State.tenant_id == 1))
        db.execute(delete(Country).where(Country.tenant_id == 1))
        db.commit()

def test_state_city_flow():
    cleanup()

    r = client.post("/api/v1/countries", headers=H, json={"name": "Brasil", "iso2": "BR"})
    assert r.status_code == 201
    country_id = r.json()["id"]

    r = client.post("/api/v1/states", headers=H, json={"country_id": country_id, "code": "SC", "name": "Santa Catarina"})
    assert r.status_code == 201
    state_id = r.json()["id"]

    r = client.post("/api/v1/cities", headers=H, json={"state_id": state_id, "name": "Criciúma", "ibge_code": "4204608"})
    assert r.status_code == 201
    city_id = r.json()["id"]

    r = client.get(f"/api/v1/cities/{city_id}", headers=H)
    assert r.status_code == 200
    assert r.json()["name"] == "Criciúma"
