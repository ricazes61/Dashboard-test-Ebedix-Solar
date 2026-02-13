@echo off
echo ============================================
echo   SOLAR PV ANALYTICS - SETUP INICIAL
echo ============================================
echo.

REM Paso 1: Crear entorno virtual
echo [1/6] Creando entorno virtual Python...
cd backend
if exist venv (
    echo    - venv ya existe, omitiendo...
) else (
    python -m venv venv
    echo    - venv creado
)

REM Paso 2: Activar venv e instalar dependencias
echo.
echo [2/6] Instalando dependencias Python...
call .\venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
pip install -r requirements.txt
echo    - Dependencias instaladas

REM Paso 3: Crear settings.json
echo.
echo [3/6] Configurando settings.json...
if not exist settings.json (
    copy settings.json.example settings.json > nul
    echo    - settings.json creado
) else (
    echo    - settings.json ya existe
)

REM Paso 4: Generar datos de ejemplo
echo.
echo [4/6] Generando datos de ejemplo...
python create_planta_data.py
python create_historico_data.py
python create_tickets_data.py

REM Paso 5: Instalar dependencias frontend
echo.
echo [5/6] Instalando dependencias Frontend...
cd ..\frontend
call npm install
echo    - Dependencias instaladas

REM Paso 6: Resumen
cd ..
echo.
echo [6/6] Verificando instalacion...
echo.
echo ============================================
echo   SETUP COMPLETADO
echo ============================================
echo.
echo   Backend:  backend\venv activado
echo   Frontend: node_modules instalado
echo   Datos:    Generados en data\input\
echo   Config:   backend\settings.json creado
echo.
echo Para iniciar la aplicacion:
echo   1. Ejecuta: start.bat
echo   2. Abre: http://localhost:5173
echo.
echo ============================================
echo.
pause
