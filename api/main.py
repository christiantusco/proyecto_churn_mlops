from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import json
import os

AUTOR = "Christian Tusco"
VERSION = "1.0"
MODEL_PATH = "models/modelo_churn_v1.joblib"
METADATA_PATH = "models/modelo_churn_v1_metadata.json"

app = FastAPI(
    title="API Predictiva de Churn - ML-Ops",
    description="Servicio de prediccion de abandono de clientes. Autor: Christian Tusco",
    version=VERSION,
)

model = None
metadata = None


@app.on_event("startup")
def cargar_modelo():
    global model, metadata
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)


class EntradaCliente(BaseModel):
    edad: int = Field(..., ge=18, le=90, description="Edad del cliente (18-90)")
    meses_contrato: int = Field(..., ge=1, le=72, description="Meses de contrato (1-72)")
    llamadas_soporte: int = Field(..., ge=0, le=20, description="Llamadas al soporte (0-20)")
    saldo_promedio: float = Field(..., ge=0, le=5000, description="Saldo promedio en cuenta (0-5000)")
    productos_contratados: int = Field(..., ge=1, le=5, description="Cantidad de productos contratados (1-5)")


@app.get("/")
def inicio():
    return {
        "mensaje": "Servicio ML-Ops activo",
        "estado": "ok",
        "autor": AUTOR,
        "version": VERSION,
    }


@app.get("/health")
def health():
    modelo_cargado = model is not None
    return {
        "status": "healthy" if modelo_cargado else "degraded",
        "modelo_cargado": modelo_cargado,
        "modelo": "modelo_churn_v1.joblib",
        "autor": AUTOR,
    }


@app.get("/info")
def info():
    if metadata is None:
        raise HTTPException(status_code=503, detail="Metadata del modelo no disponible")
    return {
        "autor": AUTOR,
        "version": VERSION,
        "modelo": metadata.get("modelo"),
        "algoritmo": metadata.get("algoritmo"),
        "fecha_entrenamiento": metadata.get("fecha_entrenamiento"),
        "variables": metadata.get("variables"),
        "metricas": metadata.get("metricas"),
    }


@app.post("/predict")
def predecir(datos: EntradaCliente):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible. Ejecute train.py primero.")

    X = [[
        datos.edad,
        datos.meses_contrato,
        datos.llamadas_soporte,
        datos.saldo_promedio,
        datos.productos_contratados,
    ]]

    prediccion = int(model.predict(X)[0])
    probabilidad = float(model.predict_proba(X)[0][1])

    if probabilidad >= 0.7:
        nivel_riesgo = "Alto"
        recomendacion = "Contactar al cliente de forma inmediata con una oferta de retencion"
    elif probabilidad >= 0.4:
        nivel_riesgo = "Medio"
        recomendacion = "Monitorear el cliente y ofrecer mejoras en el servicio contratado"
    else:
        nivel_riesgo = "Bajo"
        recomendacion = "Cliente estable, mantener seguimiento regular"

    return {
        "churn": bool(prediccion),
        "probabilidad": round(probabilidad, 4),
        "nivel_riesgo": nivel_riesgo,
        "recomendacion": recomendacion,
        "autor": AUTOR,
    }
