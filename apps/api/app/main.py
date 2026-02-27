from fastapi import FastAPI
from app.api.v1.routers.country import router as country_router
from app.api.v1.routers.state import router as state_router
from app.api.v1.routers.city import router as city_router

app = FastAPI(title="SaaS Cadastros")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(country_router)
app.include_router(state_router)
app.include_router(city_router)