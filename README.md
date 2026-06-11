# proyecto_churn_mlops

API mínima de ML-Ops para predicción de churn, desplegada con Docker y FastAPI.

## Estructura

```
proyecto_churn_mlops/
├── api/
│   ├── __init__.py
│   └── main.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Requisitos

- Docker instalado

## Instrucciones de uso

### 1. Construir la imagen

```bash
docker build -t churn-api-tusco .
```

### 2. Ejecutar el contenedor

```bash
docker run -d -p 8000:8000 --name churn-contenedor-tusco churn-api-tusco
```

### 3. Probar la API

Abrir en el navegador: http://localhost:8000

### 4. Ver contenedores activos

```bash
docker ps
```

### 5. Detener el contenedor

```bash
docker stop churn-contenedor-tusco
docker rm churn-contenedor-tusco
```
