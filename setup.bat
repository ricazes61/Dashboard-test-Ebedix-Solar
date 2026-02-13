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
echo    - Actualizando pip...
python -m pip install --upgrade pip setuptools wheel
echo    - Instalando pandas y numpy...
pip install --only-binary :all: "pandas>=3.0.0" "numpy>=2.0.0"
echo    - Instalando resto de dependencias...
pip install --only-binary :all: fastapi==0.104.1 uvicorn[standard]==0.24.0 python-dotenv==1.0.0 python-multipart==0.0.6 "pydantic>=2.10.0" "pydantic-settings>=2.7.0" openpyxl==3.1.2 reportlab==4.0.7 "Pillow>=11.0.0" openai==1.3.7 twilio==8.10.3 python-dateutil==2.8.2 pytz==2023.3 aiofiles==23.2.1
echo    - Dependencias instaladas correctamente

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
cd backend
call .\venv\Scripts\activate
echo.
echo Verificando paquetes clave:
pip list | findstr "fastapi uvicorn pandas numpy"
cd ..
echo.
echo ============================================
echo   SETUP COMPLETADO
============================================
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
