@echo off
echo ============================================
echo   INSTALACION SEGURA DE DEPENDENCIAS
echo   (Compatible con Windows + Python 3.13)
echo ============================================
echo.

REM Verificar que estamos en backend/
if not exist "venv\" (
    echo [ERROR] No se encuentra venv/
    echo Por favor ejecuta primero:
    echo   python -m venv venv
    echo.
    pause
    exit /b 1
)

echo [1/4] Activando entorno virtual...
call .\venv\Scripts\activate

echo.
echo [2/4] Actualizando pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo [3/4] Instalando dependencias principales (pandas, numpy)...
pip install --only-binary :all: "pandas>=3.0.0" "numpy>=2.0.0"

echo.
echo [4/4] Instalando resto de dependencias...
pip install --only-binary :all: ^
    fastapi==0.104.1 ^
    uvicorn[standard]==0.24.0 ^
    python-dotenv==1.0.0 ^
    python-multipart==0.0.6 ^
    "pydantic>=2.10.0" ^
    "pydantic-settings>=2.7.0" ^
    openpyxl==3.1.2 ^
    reportlab==4.0.7 ^
    Pillow==10.1.0 ^
    openai==1.3.7 ^
    twilio==8.10.3 ^
    python-dateutil==2.8.2 ^
    pytz==2023.3 ^
    aiofiles==23.2.1

echo.
echo ============================================
echo   VERIFICACION
echo ============================================
echo.
echo Paquetes instalados:
pip list | findstr "fastapi uvicorn pandas numpy"

echo.
echo ============================================
echo   INSTALACION COMPLETADA
echo ============================================
echo.
echo Para iniciar el backend:
echo   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
pause
