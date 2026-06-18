# 1. Imagen base de Python
FROM python:3.10-slim

LABEL author="Christian Tusco"
LABEL version="1.0"
LABEL description="API predictiva de churn - ML-Ops"

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el proyecto completo
COPY . .

# 5. Exponer el puerto de la API
EXPOSE 8000

# 6. Iniciar el servicio
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
