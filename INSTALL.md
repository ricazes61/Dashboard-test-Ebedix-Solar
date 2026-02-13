# 🚀 GUÍA DE INSTALACIÓN COMPLETA

## 📋 REQUISITOS PREVIOS

### **Windows:**
- ✅ Python 3.11+ o 3.13 ([Descargar](https://www.python.org/downloads/))
- ✅ Node.js 18+ ([Descargar](https://nodejs.org/))
- ✅ Git (opcional) ([Descargar](https://git-scm.com/))

### **Verificar instalación:**
```cmd
python --version
node --version
npm --version
```

---

## ⚡ MÉTODO 1: INSTALACIÓN AUTOMÁTICA (Recomendado)

### **Paso 1: Descomprimir el proyecto**
```cmd
cd C:\Users\Ricardo\projects
# Descomprimir solar-pv-analytics.tar.gz aquí
```

### **Paso 2: Ejecutar setup automático**
```cmd
cd solar-pv-analytics
setup.bat
```

**Este script:**
1. ✅ Crea entorno virtual Python
2. ✅ Instala todas las dependencias (pandas, numpy, fastapi, uvicorn, etc.)
3. ✅ Crea `settings.json`
4. ✅ Genera datos de ejemplo
5. ✅ Instala dependencias frontend (npm)
6. ✅ Verifica que todo esté instalado

**⏱️ Tiempo estimado: 5-10 minutos**

### **Paso 3: Iniciar aplicación**
```cmd
start.bat
```

Esto abrirá dos ventanas:
- **Backend** en http://localhost:8000
- **Frontend** en http://localhost:5173

---

## 🔧 MÉTODO 2: INSTALACIÓN MANUAL

### **Backend - Paso a Paso**

#### **1. Crear entorno virtual**
```cmd
cd solar-pv-analytics\backend
python -m venv venv
```

#### **2. Activar entorno virtual**
**CMD:**
```cmd
.\venv\Scripts\activate
```

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Verificar activación:**
Deberías ver `(venv)` al inicio del prompt.

#### **3. Actualizar pip**
```cmd
python -m pip install --upgrade pip setuptools wheel
```

#### **4. Instalar pandas y numpy (primero)**
```cmd
pip install --only-binary :all: "pandas>=3.0.0" "numpy>=2.0.0"
```

**Esperar mensaje:**
```
Successfully installed pandas-3.0.0 numpy-2.0.0
```

#### **5. Instalar resto de dependencias**
```cmd
pip install --only-binary :all: fastapi==0.104.1 uvicorn[standard]==0.24.0 python-dotenv==1.0.0 python-multipart==0.0.6 pydantic==2.5.0 pydantic-settings==2.1.0 openpyxl==3.1.2 reportlab==4.0.7 Pillow==10.1.0 openai==1.3.7 twilio==8.10.3 python-dateutil==2.8.2 pytz==2023.3 aiofiles==23.2.1
```

**⏱️ Esto toma 2-3 minutos**

#### **6. Verificar instalación**
```cmd
pip list | findstr "fastapi uvicorn pandas numpy"
```

**Esperado:**
```
fastapi          0.104.1
numpy            2.0.0 (o superior)
pandas           3.0.0 (o superior)
uvicorn          0.24.0
```

#### **7. Crear settings.json**
```cmd
copy settings.json.example settings.json
```

#### **8. Generar datos de ejemplo**
```cmd
python create_planta_data.py
python create_historico_data.py
python create_tickets_data.py
```

**Esperado:**
```
✓ Parametros_Planta.xlsx creado exitosamente
✓ Historico_Performance.csv creado con 91 registros
✓ Tickets_Mantenimiento.csv creado con 50 tickets
```

---

### **Frontend - Paso a Paso**

#### **1. Instalar dependencias**
```cmd
cd ..\frontend
npm install
```

**⏱️ Esto toma 1-2 minutos**

---

### **Iniciar Aplicación Manualmente**

#### **Terminal 1 - Backend:**
```cmd
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Data folder autoconfigurado: ../data/input
✅ Datos cargados: {'Parametros_Planta.xlsx': 14, ...}
INFO:     Application startup complete.
```

#### **Terminal 2 - Frontend:**
```cmd
cd frontend
npm run dev
```

**Esperado:**
```
VITE v5.0.8  ready in XXX ms
➜  Local:   http://localhost:5173/
```

---

## 🛠️ MÉTODO 3: USANDO install-deps.bat (Backend solo)

Si ya tienes el venv creado pero necesitas reinstalar dependencias:

```cmd
cd backend
install-deps.bat
```

Este script instala todas las dependencias de forma segura con `--only-binary`.

---

## ✅ VERIFICACIÓN DE INSTALACIÓN

### **1. Backend funcionando**
Abrir: http://localhost:8000/docs

Deberías ver la documentación Swagger UI con lista de endpoints.

### **2. Probar Health Check**
En Swagger UI:
1. GET /api/health
2. "Try it out"
3. "Execute"

**Esperado:**
```json
{
  "status": "healthy",
  "service": "Solar PV Analytics API",
  "version": "1.0.0"
}
```

### **3. Frontend funcionando**
Abrir: http://localhost:5173

Deberías ver el dashboard con:
- Navegación (Overview, CEO, CFO, COO, Configuración)
- Datos de la planta
- Gráficos y KPIs

---

## 🚨 TROUBLESHOOTING

### **Error: "python no se reconoce como comando"**
**Solución:**
1. Descargar Python desde https://www.python.org/downloads/
2. Durante instalación, marcar ☑️ **"Add Python to PATH"**
3. Reiniciar terminal
4. Verificar: `python --version`

---

### **Error: "npm no se reconoce como comando"**
**Solución:**
1. Descargar Node.js desde https://nodejs.org/
2. Instalar con opciones por defecto
3. Reiniciar terminal
4. Verificar: `npm --version`

---

### **Error: "No module named uvicorn"**
**Causa:** Dependencias no instaladas o venv no activado

**Solución:**
```cmd
cd backend
.\venv\Scripts\activate
pip install --only-binary :all: uvicorn[standard]==0.24.0
```

---

### **Error: Compilación de pandas/numpy**
**Causa:** Python 3.13 sin compilador C++ en Windows

**Solución:** Usar `--only-binary :all:`
```cmd
pip install --only-binary :all: "pandas>=3.0.0" "numpy>=2.0.0"
```

Si sigue fallando, instalar **Microsoft C++ Build Tools**:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

### **Error: "Data folder no configurado"**
**Causa:** `settings.json` no existe

**Solución:**
```cmd
cd backend
copy settings.json.example settings.json
```

Luego reiniciar backend.

---

### **Error: Puerto 8000/5173 ocupado**
**Solución:**
```cmd
REM Ver qué proceso usa el puerto
netstat -ano | findstr :8000

REM Matar el proceso (reemplazar XXXX con PID)
taskkill /PID XXXX /F
```

---

### **Error: PowerShell no permite ejecutar scripts**
**Error:**
```
.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled
```

**Solución:**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
solar-pv-analytics/
├── backend/
│   ├── venv/                    ← Entorno virtual (creado por setup)
│   ├── app/                     ← Código fuente
│   ├── create_*_data.py         ← Scripts generadores
│   ├── requirements.txt         ← Dependencias Python
│   ├── install-deps.bat         ← Instalador seguro
│   ├── settings.json            ← Config (creado por setup)
│   └── settings.json.example    ← Template
├── frontend/
│   ├── node_modules/            ← Dependencias (creado por npm install)
│   ├── src/                     ← Código fuente React
│   └── package.json             ← Dependencias Node.js
├── data/
│   ├── input/                   ← Datos generados
│   └── output/                  ← PDFs/audios generados
├── setup.bat                    ← Setup automático
├── start.bat                    ← Inicio rápido
├── README.md                    ← Documentación principal
├── QUICKSTART.md                ← Guía rápida
├── SWAGGER_GUIDE.md             ← Guía API
└── INSTALL.md                   ← Esta guía
```

---

## 🎯 CHECKLIST DE INSTALACIÓN

- [ ] Python 3.11+ instalado
- [ ] Node.js 18+ instalado
- [ ] Proyecto descomprimido
- [ ] `setup.bat` ejecutado sin errores
- [ ] Backend inicia en puerto 8000
- [ ] Frontend inicia en puerto 5173
- [ ] http://localhost:8000/docs carga Swagger UI
- [ ] http://localhost:5173 carga dashboard
- [ ] GET /api/health retorna `{"status": "healthy"}`

---

## 📞 SIGUIENTES PASOS

Una vez instalado:
1. 📖 Leer **QUICKSTART.md** para uso básico
2. 📖 Leer **SWAGGER_GUIDE.md** para usar la API
3. 🔑 Configurar API keys (opcional):
   - Editar `backend/.env`
   - Añadir `OPENAI_API_KEY` para TTS
   - Añadir `TWILIO_*` para WhatsApp

---

## ✅ TODO LISTO

Si completaste todos los pasos y la aplicación funciona, **¡felicitaciones!**

La aplicación está lista para:
- ✅ Explorar datos de planta solar
- ✅ Ver KPIs ejecutivos (CEO, CFO, COO)
- ✅ Generar reportes PDF
- ✅ Simular operación en tiempo real
- ✅ Gestionar tickets de mantenimiento

---

**¿Problemas durante la instalación?**
Revisa la sección de **Troubleshooting** arriba o copia el mensaje de error completo para recibir ayuda.
