# Solar PV Analytics - Demo Ejecutable

Aplicación web full-stack para análisis ejecutivo de plantas solares fotovoltaicas. Demo realista y fácil de ejecutar localmente con arquitectura preparada para migración a producción.

## 🚀 **INICIO RÁPIDO**

### **Opción 1: Script Automático (Recomendado)**
```cmd
cd solar-pv-analytics
start.bat
```

### **Opción 2: Manual**
```cmd
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### **URLs de Acceso**
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Documentación Swagger:** http://localhost:8000/docs

---

## ✅ **CONFIGURACIÓN AUTOMÁTICA**

**El backend ahora se autoconfigura al iniciar:**
- ✅ Lee automáticamente `backend/settings.json`
- ✅ Carga datos desde `../data/input` al iniciar
- ✅ **NO necesitas configurar manualmente cada vez**

Si por alguna razón falla la carga automática:
1. Ir a http://localhost:8000/docs
2. POST `/api/settings` → `{"data_folder": "../data/input"}`
3. POST `/api/data/reload`

---

## 🎯 Objetivo del Producto

La aplicación permite a usuarios C-level (CEO / CFO / COO) explorar la performance de una granja solar, combinando:

- **Datos históricos/acumulados** leídos de archivos CSV/Excel
- **Parámetros generales de planta** desde Excel
- **Operación en tiempo real simulada** cada 5 minutos (series sintéticas)
- **Backlog de mantenimiento** desde CSV/Excel, ordenable por costo
- **Reportes ejecutivos en PDF** generados automáticamente
- **Resúmenes de audio TTS** con integración WhatsApp

## 🏗️ Arquitectura

### Stack Tecnológico

**Backend:**
- Python 3.10+
- FastAPI (API REST)
- Pandas (procesamiento de datos)
- ReportLab (generación de PDF)
- OpenAI API (Text-to-Speech)
- Twilio (WhatsApp)

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)
- TailwindCSS (estilos)
- Recharts (gráficos)
- Axios (HTTP client)

**Datos:**
- Archivos CSV/Excel (no requiere base de datos)
- Caché en memoria del backend
- Simulación sintética en tiempo real

### Estructura del Proyecto

```
solar-pv-analytics/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints REST
│   │   │   ├── health.py      # Health check
│   │   │   ├── settings.py    # Configuración
│   │   │   ├── data.py        # Datos y KPIs
│   │   │   └── reports.py     # PDF, TTS, WhatsApp
│   │   ├── core/
│   │   │   └── config.py      # Configuración y variables de entorno
│   │   ├── models/
│   │   │   └── schemas.py     # Modelos Pydantic
│   │   ├── services/
│   │   │   ├── data_loader.py        # Carga de archivos
│   │   │   ├── realtime_simulator.py # Simulación en tiempo real
│   │   │   ├── kpi_calculator.py     # Cálculo de KPIs
│   │   │   ├── pdf_generator.py      # Generación de PDF
│   │   │   ├── tts_service.py        # Text-to-Speech
│   │   │   └── whatsapp_service.py   # WhatsApp
│   │   └── main.py            # Aplicación FastAPI
│   ├── requirements.txt
│   └── create_*_data.py       # Scripts para generar datos de ejemplo
│
├── frontend/                   # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/        # Componentes reutilizables
│   │   │   │   └── KPICard.tsx
│   │   │   └── views/         # Vistas principales
│   │   │       ├── HomeView.tsx    # Overview ejecutivo
│   │   │       ├── CEOView.tsx     # Vista CEO
│   │   │       ├── CFOView.tsx     # Vista CFO
│   │   │       ├── COOView.tsx     # Vista COO
│   │   │       └── SettingsView.tsx # Configuración
│   │   ├── services/
│   │   │   └── api.ts         # Cliente API
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript interfaces
│   │   ├── App.tsx            # Componente principal
│   │   └── main.tsx           # Entry point
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   ├── input/                 # Archivos de entrada (REQUERIDOS)
│   │   ├── Parametros_Planta.xlsx
│   │   ├── Historico_Performance.csv
│   │   └── Tickets_Mantenimiento.csv
│   └── output/                # Archivos generados (PDF, audio)
│
├── .env.example               # Plantilla de variables de entorno
├── .gitignore
└── README.md
```

## 📋 Prerequisitos

- **Python 3.10 o superior**
- **Node.js 18 o superior** y npm
- **Git**

## 🚀 Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone <tu-repo>
cd solar-pv-analytics
```

### 2. Configurar Variables de Entorno

Copiar el archivo `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DATA_FOLDER=./data/input

# OpenAI TTS (opcional para demo)
OPENAI_API_KEY=sk-your-key-here

# Twilio WhatsApp (opcional para demo)
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

> **Nota:** La aplicación funciona en modo simulación si no configuras las API keys externas.

### 3. Backend Setup

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Generar datos de ejemplo (si no existen)
python create_planta_data.py
python create_historico_data.py
python create_tickets_data.py

# Iniciar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs

### 4. Frontend Setup

En otra terminal:

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 📁 Archivos de Entrada

La aplicación requiere 3 archivos en el folder configurado (por defecto `./data/input`):

### 1. `Parametros_Planta.xlsx`

Excel con 3 hojas:

**Hoja "Planta":**
```
planta_id, nombre_planta, pais, provincia_estado, ciudad, lat, lon, zona_horaria,
potencia_dc_mwp, potencia_ac_mw, cantidad_paneles, cantidad_strings,
cantidad_inversores, fecha_puesta_en_marcha, tarifa_usd_mwh, target_pr,
target_availability, soiling_loss_target_pct, degradation_annual_pct, curtailment_policy
```

**Hoja "Equipos":**
```
equipo_id, tipo, fabricante, modelo, capacidad_kw, estado_base
```

**Hoja "Umbrales":**
```
kpi, umbral_amarillo, umbral_rojo, descripcion_alerta
```

### 2. `Historico_Performance.csv`

```csv
fecha, planta_id, energia_real_kwh, energia_esperada_kwh, irradiancia_poa_kwh_m2,
pr_real, availability_real_pct, curtailment_kwh, perdida_soiling_kwh,
perdida_otros_kwh, ingresos_estimados_usd, opex_estimado_usd
```

### 3. `Tickets_Mantenimiento.csv`

```csv
ticket_id, planta_id, fecha_creacion, estado, tipo, criticidad, equipo_id,
descripcion, costo_estimado_usd, impacto_estimado_kwh, sla_objetivo_horas,
responsable, fecha_estimada_resolucion
```

> **Nota:** Los scripts `create_*_data.py` generan estos archivos automáticamente con datos realistas.

## 🎨 Funcionalidades

### Vistas Ejecutivas

#### 1. **Home / Overview Ejecutivo**
- KPIs consolidados con semáforos (verde/amarillo/rojo)
- Energía real vs esperada
- Performance Ratio (PR)
- Disponibilidad
- Estado del sistema
- Ingresos, OPEX y margen bruto
- CO₂ evitado
- Backlog de mantenimiento
- Alertas principales
- Selector de rango (30d / 90d / YTD / 12m)
- Botón de recarga de datos
- Generación de PDF ejecutivo

#### 2. **Vista CEO**
- Energía real vs esperada con tendencia
- Desviación porcentual
- KPIs ESG: CO₂ evitado
- Alertas principales basadas en umbrales
- Gráfico de potencia en tiempo real
- Tendencia energética (mejorando/decreciendo/estable)

#### 3. **Vista CFO**
- Ingresos estimados vs OPEX
- Margen bruto (USD y %)
- Costo por kWh
- Resumen financiero detallado
- Variaciones vs objetivo
- ROI / Payback simplificado

#### 4. **Vista COO**
- PR promedio vs objetivo
- Disponibilidad (Availability)
- Potencia actual en tiempo real (actualización cada 15s)
- Estado de inversores
- Backlog total de mantenimiento
- Tabla de top 10 tickets por costo
  - Filtros por estado, criticidad, equipo
  - Badges visuales por criticidad
  - SLA vencido destacado
- Gráfico en tiempo real

#### 5. **Settings / Configuración**
- Configurar folder de datos
- Botón "Recargar datos" con feedback
- Generación de Reporte PDF ejecutivo
- Generación de audio TTS (resumen del reporte)
- Envío de audio por WhatsApp
- Visualización de última recarga
- Cantidad de registros cargados por archivo
- Mensajes de error claros y detallados

### Generación de Reportes

#### PDF Ejecutivo

El reporte incluye:
- **Portada:** Nombre planta, ubicación, fecha
- **Resumen ejecutivo:** 6-10 bullets con KPIs principales
- **Gráficos:** Energía, PR, Availability
- **Tabla:** Top 10 tickets por costo
- **Alertas y riesgos:** Umbrales rojos/amarillos

```python
# Endpoint
POST /api/report/pdf?range=30d
```

#### Text-to-Speech

Genera audio MP3 con resumen ejecutivo en español:

```python
# Endpoint
POST /api/report/tts
{
  "text": "Texto personalizado (opcional)"
}
```

#### WhatsApp

Envía audio por WhatsApp usando Twilio:

```python
# Endpoint
POST /api/whatsapp/send-audio
{
  "to_phone": "+5491112345678",
  "audio_path": "/ruta/al/audio.mp3"
}
```

### Simulación en Tiempo Real

- Genera datos sintéticos cada 5 minutos
- Basado en perfil solar tipo campana (6:00 - 20:00)
- Incorpora:
  - Potencia instantánea
  - Energía del intervalo
  - Irradiancia
  - Temperatura de módulos
  - Estado de inversores
- Simula caídas parciales si hay tickets críticos pendientes
- Frontend actualiza automáticamente cada 15 segundos (polling)

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Settings
```
GET  /api/settings
POST /api/settings
```

### Data Management
```
POST /api/data/reload              # Recarga archivos
GET  /api/plant                    # Parámetros de planta
GET  /api/kpis/exec?range=30d      # KPIs ejecutivos
GET  /api/series/realtime?hours=24 # Serie simulada
GET  /api/tickets?status=pendiente&sort=costo_desc&limit=10
```

### Reports
```
POST /api/report/pdf?range=30d     # Genera PDF
POST /api/report/tts               # Genera audio
POST /api/whatsapp/send-audio      # Envía por WhatsApp
```

Ver documentación interactiva completa en: http://localhost:8000/docs

## 🔐 Seguridad y Configuración

### Variables de Entorno Sensibles

**NUNCA** commitar credenciales. Usar `.env` (incluido en `.gitignore`):

- `OPENAI_API_KEY`: Para Text-to-Speech
- `TWILIO_ACCOUNT_SID`: Para WhatsApp
- `TWILIO_AUTH_TOKEN`: Para WhatsApp
- `TWILIO_WHATSAPP_FROM`: Número de Twilio

### Modo Simulación

Si no se configuran las APIs externas:
- **TTS:** Crea archivo placeholder
- **WhatsApp:** Muestra mensaje "SIMULACIÓN: se enviaría a..."

## 🏗️ Arquitectura para Producción

Esta aplicación está preparada para migración a plataformas cloud sin refactorizar desde cero:

### Backend (FastAPI)

**Opciones de deployment:**
- **Railway** (recomendado para demo)
- **Render**
- **Heroku**
- **AWS Elastic Beanstalk**
- **Google Cloud Run**
- **Azure App Service**

**Cambios necesarios:**
1. Migrar storage de archivos a:
   - **AWS S3** / **Google Cloud Storage** / **Azure Blob**
   - O usar base de datos (PostgreSQL, MySQL)
2. Configurar variables de entorno en la plataforma
3. Agregar `Procfile` o `Dockerfile` según plataforma

### Frontend (React + Vite)

**Opciones de deployment:**
- **Vercel** (recomendado)
- **Netlify**
- **AWS Amplify**
- **GitHub Pages**
- **Cloudflare Pages**

**Cambios necesarios:**
1. Actualizar `VITE_API_URL` con URL del backend en producción
2. Build: `npm run build`
3. Deploy carpeta `dist/`

### Base de Datos (Opcional)

Para producción se recomienda migrar de archivos a DB:

**Opciones:**
- **PostgreSQL** (Supabase, Neon, Railway)
- **MySQL** (PlanetScale)
- **SQLite** (para pequeña escala)

**Migración sugerida:**
1. Crear modelos SQLAlchemy basados en `schemas.py`
2. Seed inicial desde CSVs
3. Reemplazar `DataLoader` por queries a DB
4. Mantener API endpoints sin cambios (mismo contrato)

### Arquitectura Cloud Recomendada

```
┌─────────────────┐
│   Vercel/       │
│   Netlify       │ ← Frontend (React)
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│   Railway/      │
│   Render        │ ← Backend (FastAPI)
│   (Backend)     │
└────────┬────────┘
         │
         ├→ AWS S3 / GCS (archivos)
         ├→ PostgreSQL (datos)
         ├→ OpenAI API (TTS)
         └→ Twilio API (WhatsApp)
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

### Manual Testing

1. **Configurar folder:** Settings → Ingresar ruta → "Guardar"
2. **Recargar datos:** Settings → "Recargar Datos Ahora"
3. **Verificar KPIs:** Home → Ver cards con datos
4. **Cambiar rango:** Selector 30d/90d/YTD/12m
5. **Generar PDF:** Home → "PDF" o Settings → "Generar Reporte PDF"
6. **Generar TTS:** Settings → "Generar Audio TTS"
7. **Enviar WhatsApp:** Settings → Ingresar número → "Enviar por WhatsApp"
8. **Verificar real-time:** COO → Ver gráfico actualizándose

## 🐛 Troubleshooting

### Error: "Datos no cargados"
- Verificar que existe `data/input/` con los 3 archivos
- Ir a Settings y configurar el folder correcto
- Presionar "Recargar Datos Ahora"

### Error: "CORS"
- Verificar que backend está en puerto 8000
- Verificar `CORS_ORIGINS` en `.env` incluye `http://localhost:5173`

### Error generando PDF
- Verificar que `reportlab` está instalado
- Verificar permisos de escritura en `data/output/`

### Error TTS/WhatsApp
- Verificar API keys en `.env`
- Ver logs del backend para detalles
- Funciona en modo simulación sin keys

## 📚 Recursos Adicionales

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Vite Docs:** https://vitejs.dev/
- **ReportLab:** https://www.reportlab.com/docs/reportlab-userguide.pdf
- **OpenAI TTS:** https://platform.openai.com/docs/guides/text-to-speech
- **Twilio WhatsApp:** https://www.twilio.com/docs/whatsapp/api

## 👥 Autores

Desarrollado por **Vreadynow** - Digital Twin Platform

## 📄 Licencia

Este proyecto es una demo para propósitos educativos y comerciales.

---

**¿Preguntas o problemas?** Abre un issue en el repositorio.
