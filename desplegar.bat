@echo off
echo ============================================
echo   Desplegando proyecto_churn_mlops
echo ============================================

echo.
echo [1/4] Construyendo imagen Docker...
docker build -t churn-api-perez .

echo.
echo [2/4] Deteniendo contenedor anterior (si existe)...
docker stop churn-contenedor 2>nul
docker rm churn-contenedor 2>nul

echo.
echo [3/4] Ejecutando contenedor...
docker run -d -p 8000:8000 --name churn-contenedor churn-api-perez

echo.
echo [4/4] Listando contenedores activos...
docker ps

echo.
echo ============================================
echo   API lista en: http://localhost:8000
echo ============================================
echo Abriendo navegador...
timeout /t 3 /nobreak >nul
start http://localhost:8000

pause
