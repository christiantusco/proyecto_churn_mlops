from fastapi import FastAPI

app = FastAPI(title="Servicio ML-Ops - Churn")

@app.get("/")
def inicio():
    return {
        "mensaje": "Servicio ML-Ops activo",
        "estado": "ok",
        "autor": "Christian Tusco"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
