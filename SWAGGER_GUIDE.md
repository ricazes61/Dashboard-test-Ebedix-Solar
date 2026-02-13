# 📖 GUÍA RÁPIDA - API SWAGGER UI

## 🔗 Acceso a Swagger UI
http://localhost:8000/docs

---

## ✅ SECUENCIA CORRECTA DE USO

### **1. Verificar Salud del Backend**
**Endpoint:** `GET /api/health`

1. Click en **GET /api/health**
2. Click en **"Try it out"**
3. Click en **"Execute"**

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "Solar PV Analytics API",
  "version": "1.0.0"
}
```

---

### **2. Configurar Carpeta de Datos**
**Endpoint:** `POST /api/settings`

1. Click en **POST /api/settings**
2. Click en **"Try it out"**
3. En el **Request body**, pegar:
```json
{
  "data_folder": "../data/input"
}
```
4. Click en **"Execute"**

**Respuesta esperada:**
```json
{
  "data_folder": "../data/input",
  "last_reload": null,
  "files_loaded": {}
}
```

---

### **3. Recargar Datos**
**Endpoint:** `POST /api/data/reload`

1. Click en **POST /api/data/reload**
2. Click en **"Try it out"**
3. Click en **"Execute"**

**Respuesta esperada:**
```json
{
  "success": true,
  "results": {
    "planta": "OK",
    "historico": "OK",
    "tickets": "OK"
  },
  "errors": [],
  "files_loaded": {
    "Parametros_Planta.xlsx": 14,
    "Historico_Performance.csv": 91,
    "Tickets_Mantenimiento.csv": 50
  },
  "last_reload": "2026-02-13T12:34:56.789012"
}
```

---

### **4. Obtener Datos de Planta**
**Endpoint:** `GET /api/plant`

1. Click en **GET /api/plant**
2. Click en **"Try it out"**
3. Click en **"Execute"**

**Respuesta esperada:**
```json
{
  "planta": {
    "planta_id": "PV-001",
    "nombre_planta": "Planta Solar San Juan",
    "pais": "Argentina",
    "potencia_dc_mwp": 50.0,
    ...
  },
  "equipos": [...],
  "umbrales": [...]
}
```

---

### **5. Obtener KPIs Ejecutivos**
**Endpoint:** `GET /api/kpis`

1. Click en **GET /api/kpis**
2. Click en **"Try it out"**
3. Click en **"Execute"**

**Respuesta esperada:**
```json
{
  "energia_real_kwh": 5630425.66,
  "energia_esperada_kwh": 5584791.88,
  "desviacion_pct": 0.82,
  "tendencia": "up",
  "ingresos_estimados_usd": 365977.64,
  "opex_estimado_usd": 69996.96,
  ...
}
```

---

### **6. Obtener Datos en Tiempo Real**
**Endpoint:** `GET /api/realtime`

1. Click en **GET /api/realtime**
2. Click en **"Try it out"**
3. Click en **"Execute"**

**Respuesta esperada:**
```json
{
  "timestamp": "2026-02-13T12:34:56.789012",
  "potencia_actual_kw": 15345.68,
  "energia_hoy_kwh": 123456.78,
  "irradiancia_poa": 850.5,
  "temperatura_ambiente": 28.3,
  "estado_inversores": {
    "INV-001": "Operando",
    "INV-002": "Operando",
    ...
  }
}
```

---

### **7. Obtener Tickets de Mantenimiento**
**Endpoint:** `GET /api/tickets`

**Parámetros opcionales:**
- `estado`: "Pendiente", "En Progreso", "Bloqueado", "Cerrado"
- `criticidad`: "Crítica", "Alta", "Media", "Baja"
- `tipo`: "Correctivo", "Preventivo", "Predictivo"

**Ejemplo 1: Todos los tickets**
1. Click en **GET /api/tickets**
2. Click en **"Try it out"**
3. Click en **"Execute"**

**Ejemplo 2: Solo tickets pendientes**
1. Click en **GET /api/tickets**
2. Click en **"Try it out"**
3. En **estado**, escribir: `Pendiente`
4. Click en **"Execute"**

**Respuesta esperada:**
```json
[
  {
    "ticket_id": "TKT-0001",
    "planta_id": "PV-001",
    "estado": "Pendiente",
    "tipo": "Correctivo",
    "criticidad": "Alta",
    "descripcion": "Falla en inversor",
    "costo_estimado_usd": 15000.0,
    ...
  },
  ...
]
```

---

## 🚨 ERRORES COMUNES

### **Error: "Failed to fetch"**
**Causa:** CORS o backend no corriendo  
**Solución:** Reiniciar backend con `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### **Error: "Data folder no configurado"**
**Causa:** No se ejecutó POST /api/settings  
**Solución:** Ejecutar POST /api/settings con `{"data_folder": "../data/input"}`

### **Error: 422 Unprocessable Entity**
**Causa:** JSON incorrecto en el request body  
**Solución:** Verificar que el JSON esté bien formado (comillas dobles, comas, etc.)

### **Error: "detail": [{"loc": ["string", 0], ...}]**
**Causa:** Formato de request incorrecto  
**Solución:** Usar el ejemplo exacto de JSON de arriba

---

## 📝 FORMATO CORRECTO DE JSON

### ✅ CORRECTO
```json
{
  "data_folder": "../data/input"
}
```

### ❌ INCORRECTO
```json
{
  data_folder: "../data/input"  // Falta comillas en la clave
}
```

```json
{
  "data_folder": '../data/input'  // Comillas simples no permitidas
}
```

```json
{
  "data_folder": "../data/input",  // Coma extra al final
}
```

---

## 🎯 ORDEN RECOMENDADO DE PRUEBA

1. ✅ GET /api/health
2. ✅ POST /api/settings
3. ✅ POST /api/data/reload
4. ✅ GET /api/plant
5. ✅ GET /api/kpis
6. ✅ GET /api/realtime
7. ✅ GET /api/tickets

---

## 📞 ENDPOINTS AVANZADOS

### **Generar Reporte PDF**
**POST /api/reports/pdf**
```json
{
  "range": "30d"
}
```

### **Generar Audio TTS**
**POST /api/reports/tts**
```json
{
  "text": null
}
```
*(null = genera resumen automático)*

### **Enviar por WhatsApp**
**POST /api/reports/whatsapp**
```json
{
  "to_phone": "+54911XXXXXXXX",
  "audio_path": "output/resumen_ejecutivo.mp3"
}
```

---

## 💡 TIPS

1. **Autoconfiguración:** Si reiniciaste el backend, los datos se cargan automáticamente desde `settings.json`

2. **Simulación en Tiempo Real:** Los datos de `/api/realtime` cambian cada 5 minutos

3. **Filtros de Tickets:** Combina múltiples filtros para búsquedas específicas

4. **Documentación Interactiva:** Swagger UI muestra ejemplos de respuesta para cada endpoint

---

## ✅ TODO LISTO

Si llegaste hasta aquí y todos los endpoints funcionan, la aplicación está **100% operativa**.

Ahora puedes:
- Abrir el frontend en http://localhost:5173
- Explorar las vistas CEO, CFO, COO
- Generar reportes PDF
- Probar TTS y WhatsApp (requiere API keys)
