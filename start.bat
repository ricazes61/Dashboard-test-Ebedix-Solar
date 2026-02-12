@echo off
echo ========================================
echo Solar PV Analytics - Iniciando Servicios
echo ========================================
echo.

REM Verificar directorio
if not exist "backend" (
    echo Error: Ejecutar desde el directorio raiz del proyecto
    pause
    exit /b 1
)

REM Iniciar Backend
echo Iniciando Backend (FastAPI)...
cd backend

if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

start "Backend - FastAPI" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
cd ..

echo Backend iniciado
echo   API: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo.

timeout /t 3 /nobreak >nul

REM Iniciar Frontend
echo Iniciando Frontend (React + Vite)...
cd frontend

if not exist "node_modules" (
    echo Instalando dependencias...
    call npm install
)

start "Frontend - Vite" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo Aplicacion lista!
echo ========================================
echo.
echo Abre tu navegador en: http://localhost:5173
echo.
echo Presiona cualquier tecla para detener los servicios...
pause >nul

taskkill /FI "WINDOWTITLE eq Backend - FastAPI" /T /F
taskkill /FI "WINDOWTITLE eq Frontend - Vite" /T /F
