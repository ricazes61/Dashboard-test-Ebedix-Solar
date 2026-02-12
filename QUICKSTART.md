# 🚀 Guía Rápida de Inicio

## Inicio Rápido (5 minutos)

### Opción 1: Script Automático

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

### Opción 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Abrir navegador:** http://localhost:5173

## Primeros Pasos en la App

1. **Ir a Settings** (menú superior)
2. **Verificar folder de datos:** `../data/input` (ya configurado)
3. **Presionar "Recargar Datos Ahora"**
4. **Ir a Home** para ver el dashboard

## Datos de Ejemplo

Los datos ya están generados en `data/input/`:
- ✅ `Parametros_Planta.xlsx` - Planta "Solar del Valle" (50 MWp)
- ✅ `Historico_Performance.csv` - 90 días de histórico
- ✅ `Tickets_Mantenimiento.csv` - 50 tickets de ejemplo

## Probar Funcionalidades

### 1. Ver KPIs Ejecutivos
- **Home** → Ver cards con métricas
- Cambiar rango: 30d / 90d / YTD / 12m

### 2. Vistas Especializadas
- **CEO** → Energía, CO₂, tendencias, gráfico real-time
- **CFO** → Ingresos, OPEX, margen bruto
- **COO** → PR, Availability, tickets pendientes

### 3. Generar Reporte PDF
- **Home** → Botón "PDF"
- O **Settings** → "Generar Reporte PDF Ejecutivo"

### 4. Text-to-Speech (opcional)
- **Settings** → "Generar Audio TTS"
- Requiere `OPENAI_API_KEY` en `.env` (o funciona en modo simulación)

### 5. WhatsApp (opcional)
- Primero generar audio TTS
- Ingresar número en formato E.164: `+5491112345678`
- Presionar "Enviar por WhatsApp"
- Requiere credenciales Twilio (o funciona en modo simulación)

## Configuración Opcional

### Habilitar OpenAI TTS

Editar `backend/.env`:
```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Habilitar Twilio WhatsApp

Editar `backend/.env`:
```env
TWILIO_ACCOUNT_SID=tu-account-sid
TWILIO_AUTH_TOKEN=tu-auth-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

## Troubleshooting Rápido

**Error: "Datos no cargados"**
→ Ir a Settings → "Recargar Datos Ahora"

**Error: CORS**
→ Verificar que backend está en puerto 8000
→ Verificar que frontend está en puerto 5173

**Error: Módulo no encontrado**
→ Backend: `pip install -r requirements.txt`
→ Frontend: `npm install`

**Puerto ocupado**
→ Cambiar puerto en `.env` o matar proceso existente

## URLs Importantes

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **API Redoc:** http://localhost:8000/redoc

## Próximos Pasos

1. Explorar todas las vistas ejecutivas
2. Generar reportes PDF
3. Probar diferentes rangos de fecha
4. Ver actualización real-time en vista COO
5. Configurar APIs externas para TTS/WhatsApp
6. Modificar datos de entrada para tu caso

## Documentación Completa

Ver `README.md` para:
- Arquitectura detallada
- Formato de archivos de entrada
- API endpoints completos
- Guía de deployment a producción
- Troubleshooting avanzado

---

**¿Dudas?** Revisa el README.md completo o abre un issue.
