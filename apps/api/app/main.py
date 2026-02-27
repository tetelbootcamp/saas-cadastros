from fastapi import FastAPI

app = FastAPI(title="SaaS Cadastros")

@app.get("/health")
def health():
    return {"status": "ok"}