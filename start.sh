#!/bin/bash

# Script para iniciar la aplicación Solar PV Analytics

echo "========================================"
echo "Solar PV Analytics - Iniciando Servicios"
echo "========================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Ejecutar desde el directorio raíz del proyecto"
    exit 1
fi

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo "📡 Iniciando Backend (FastAPI)..."
cd backend
source venv/bin/activate 2>/dev/null || {
    echo "⚠️  Entorno virtual no encontrado. Creando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "✅ Backend iniciado (PID: $BACKEND_PID)"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

# Esperar a que el backend esté listo
sleep 3

# Iniciar Frontend
echo "🎨 Iniciando Frontend (React + Vite)..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "⚠️  Dependencias no instaladas. Instalando..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"
echo "   App: http://localhost:5173"
echo ""

echo "========================================"
echo "✨ Aplicación lista!"
echo "========================================"
echo ""
echo "🌐 Abre tu navegador en: http://localhost:5173"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"
echo ""

# Esperar indefinidamente
wait
