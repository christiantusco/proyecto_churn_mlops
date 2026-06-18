# proyecto_churn_mlops

API predictiva de ML-Ops para prediccion de abandono de clientes (churn), desarrollada con FastAPI y desplegada con Docker.

**Autor:** Christian Tusco

---

## Estructura del proyecto

```
proyecto_churn_mlops/
├── api/
│   ├── __init__.py
│   └── main.py          # API FastAPI con endpoints y validaciones
├── models/              # Archivos generados por train.py
│   ├── modelo_churn_v1.joblib
│   ├── modelo_churn_v1_metadata.json
│   └── metricas_modelo.md
├── train.py             # Script de entrenamiento del modelo
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Endpoints disponibles

| Endpoint   | Metodo | Descripcion                          |
|------------|--------|--------------------------------------|
| `/`        | GET    | Estado del servicio y autor          |
| `/health`  | GET    | Estado del modelo cargado            |
| `/info`    | GET    | Version, variables y metricas        |
| `/predict` | POST   | Prediccion de churn para un cliente  |
| `/docs`    | GET    | Swagger UI interactivo               |

---

## Requisitos de entrada para /predict

| Campo                 | Tipo  | Rango    |
|-----------------------|-------|----------|
| edad                  | int   | 18 - 90  |
| meses_contrato        | int   | 1 - 72   |
| llamadas_soporte      | int   | 0 - 20   |
| saldo_promedio        | float | 0 - 5000 |
| productos_contratados | int   | 1 - 5    |

---

## Ejecucion local

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Entrenar el modelo

```bash
python train.py
```

Genera en `models/`:
- `modelo_churn_v1.joblib`
- `modelo_churn_v1_metadata.json`
- `metricas_modelo.md`

### 3. Iniciar la API

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Probar endpoints

- `http://localhost:8000` — estado del servicio
- `http://localhost:8000/health` — salud del modelo
- `http://localhost:8000/info` — informacion del modelo
- `http://localhost:8000/docs` — Swagger UI

---

## Ejecucion con Docker

### 1. Construir la imagen

```bash
docker build -t churn-api-tusco .
```

### 2. Ejecutar el contenedor

```bash
docker run -d -p 8000:8000 --name churn-contenedor-tusco churn-api-tusco
```

### 3. Verificar el contenedor activo

```bash
docker ps
```

### 4. Ver logs del contenedor

```bash
docker logs churn-contenedor-tusco
```

### 5. Detener y eliminar el contenedor

```bash
docker stop churn-contenedor-tusco
docker rm churn-contenedor-tusco
```

---

## Ejemplo de solicitud valida

```json
POST /predict
{
  "edad": 35,
  "meses_contrato": 6,
  "llamadas_soporte": 12,
  "saldo_promedio": 300.0,
  "productos_contratados": 1
}
```

Respuesta esperada:

```json
{
  "churn": true,
  "probabilidad": 0.87,
  "nivel_riesgo": "Alto",
  "recomendacion": "Contactar al cliente de forma inmediata con una oferta de retencion",
  "autor": "Christian Tusco"
}
```

## Ejemplo de solicitud invalida (campo faltante)

```json
POST /predict
{
  "edad": 35,
  "meses_contrato": 6
}
```

Respuesta: `422 Unprocessable Entity`

## Ejemplo de valor fuera de rango

```json
POST /predict
{
  "edad": 150,
  "meses_contrato": 6,
  "llamadas_soporte": 5,
  "saldo_promedio": 1000.0,
  "productos_contratados": 2
}
```

Respuesta: `422 Unprocessable Entity`
