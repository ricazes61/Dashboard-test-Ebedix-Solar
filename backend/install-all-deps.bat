@echo off
echo ============================================
echo   INSTALACION DE DEPENDENCIAS BACKEND
echo   Solar PV Analytics
echo ============================================
echo.

REM Verificar que estamos en backend/
if not exist "venv\" (
    echo [ERROR] No se encuentra venv/
    echo.
    echo Por favor ejecuta primero:
    echo   cd backend
    echo   python -m venv venv
    echo.
    pause
    exit /b 1
)

echo [1/6] Activando entorno virtual...
call .\venv\Scripts\activate

echo.
echo [2/6] Actualizando pip, setuptools y wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERROR] Fallo al actualizar pip
    pause
    exit /b 1
)

echo.
echo [3/6] Instalando pandas y numpy...
pip install --only-binary :all: "pandas>=3.0.0" "numpy>=2.0.0"
if errorlevel 1 (
    echo [ERROR] Fallo al instalar pandas/numpy
    pause
    exit /b 1
)

echo.
echo [4/6] Instalando FastAPI, Uvicorn y Pydantic...
pip install --only-binary :all: fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.0 pydantic-settings==2.1.0
if errorlevel 1 (
    echo [ERROR] Fallo al instalar FastAPI/Uvicorn
    pause
    exit /b 1
)

echo.
echo [5/6] Instalando dependencias adicionales...
pip install --only-binary :all: python-dotenv==1.0.0 python-multipart==0.0.6 openpyxl==3.1.2 reportlab==4.0.7 Pillow==10.1.0 openai==1.3.7 twilio==8.10.3 python-dateutil==2.8.2 pytz==2023.3 aiofiles==23.2.1
if errorlevel 1 (
    echo [ERROR] Fallo al instalar dependencias adicionales
    pause
    exit /b 1
)

echo.
echo [6/6] Verificando instalacion...
echo.
echo Paquetes criticos instalados:
pip list | findstr "fastapi uvicorn pandas numpy pydantic"
echo.

echo Verificando versiones especificas:
python -c "import fastapi; print(f'fastapi: {fastapi.__version__}')"
python -c "import uvicorn; print(f'uvicorn: {uvicorn.__version__}')"
python -c "import pandas; print(f'pandas: {pandas.__version__}')"
python -c "import numpy; print(f'numpy: {numpy.__version__}')"
python -c "import pydantic; print(f'pydantic: {pydantic.__version__}')"

echo.
echo ============================================
echo   INSTALACION COMPLETADA
echo ============================================
echo.
echo Total de paquetes instalados:
pip list | find /c /v ""
echo.
echo Para iniciar el backend:
echo   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo ============================================
pause
