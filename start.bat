@echo off
echo ============================================
echo   SOLAR PV ANALYTICS - INICIO AUTOMATICO
echo ============================================
echo.

REM Verificar que settings.json existe
if not exist "backend\settings.json" (
    echo Creando settings.json...
    echo {"data_folder": "../data/input", "last_reload": null, "files_loaded": {}} > backend\settings.json
)

REM Verificar que los datos existen
if not exist "data\input\Parametros_Planta.xlsx" (
    echo.
    echo [ERROR] No se encuentran los archivos de datos
    echo Por favor, ejecuta primero:
    echo   cd backend
    echo   .\venv\Scripts\activate
    echo   python create_planta_data.py
    echo   python create_historico_data.py
    echo   python create_tickets_data.py
    echo.
    pause
    exit /b 1
)

echo [OK] Archivos de configuracion verificados
echo.

REM Iniciar Backend
echo Iniciando Backend FastAPI...
start "Solar PV - Backend" cmd /k "cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Esperar a que el backend inicie
echo Esperando a que el backend inicie (5 segundos)...
timeout /t 5 /nobreak > nul

REM Iniciar Frontend
echo Iniciando Frontend React...
start "Solar PV - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo   SERVICIOS INICIADOS
echo ============================================
echo.
echo   Backend:  http://localhost:8000
echo   Docs:     http://localhost:8000/docs
echo   Frontend: http://localhost:5173
echo.
echo   Presiona Ctrl+C en cada ventana para detener
echo ============================================
echo.
pause
