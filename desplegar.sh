#!/bin/bash
echo "============================================"
echo "  Desplegando proyecto_churn_mlops"
echo "============================================"

echo ""
echo "[1/4] Construyendo imagen Docker..."
docker build -t churn-api-tusco .

echo ""
echo "[2/4] Deteniendo contenedor anterior (si existe)..."
docker stop churn-contenedor 2>/dev/null
docker rm churn-contenedor 2>/dev/null

echo ""
echo "[3/4] Ejecutando contenedor..."
docker run -d -p 8000:8000 --name churn-contenedor churn-api-tusco

echo ""
echo "[4/4] Listando contenedores activos..."
docker ps

echo ""
echo "============================================"
echo "  API lista en: http://localhost:8000"
echo "============================================"
sleep 2
open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null
