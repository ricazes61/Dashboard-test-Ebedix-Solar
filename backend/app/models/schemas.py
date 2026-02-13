from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date

# ========== Planta ==========
class PlantaBase(BaseModel):
    planta_id: str
    nombre_planta: str
    pais: str
    provincia_estado: str
    ciudad: str
    lat: float
    lon: float
    zona_horaria: str
    potencia_dc_mwp: float
    potencia_ac_mw: float
    cantidad_paneles: int
    cantidad_strings: int
    cantidad_inversores: int
    fecha_puesta_en_marcha: str
    tarifa_usd_mwh: float
    target_pr: float
    target_availability: float
    soiling_loss_target_pct: float
    degradation_annual_pct: float
    curtailment_policy: str

class EquipoBase(BaseModel):
    equipo_id: str
    tipo: str
    fabricante: str
    modelo: str
    capacidad_kw: float
    estado_base: str

class UmbralBase(BaseModel):
    kpi: str
    umbral_amarillo: float
    umbral_rojo: float
    descripcion_alerta: str

class PlantaData(BaseModel):
    planta: PlantaBase
    equipos: List[EquipoBase]
    umbrales: List[UmbralBase]

# ========== Performance ==========
class HistoricoPerformance(BaseModel):
    fecha: str
    planta_id: str
    energia_real_kwh: float
    energia_esperada_kwh: float
    irradiancia_poa_kwh_m2: float
    pr_real: float
    availability_real_pct: float
    curtailment_kwh: float
    perdida_soiling_kwh: float
    perdida_otros_kwh: float
    ingresos_estimados_usd: float
    opex_estimado_usd: float

# ========== Tickets ==========
class Ticket(BaseModel):
    ticket_id: str
    planta_id: str
    fecha_creacion: str
    estado: str
    tipo: str
    criticidad: str
    equipo_id: Optional[str] = None
    descripcion: str
    costo_estimado_usd: float
    impacto_estimado_kwh: float
    sla_objetivo_horas: int
    responsable: str
    fecha_estimada_resolucion: Optional[str] = None

# ========== KPIs Ejecutivos ==========
class KPIsEjecutivos(BaseModel):
    # CEO
    energia_real_kwh: float
    energia_esperada_kwh: float
    desviacion_pct: float
    tendencia: str  # "up", "down", "stable"
    co2_evitado_kg: float
    alertas_principales: List[str]
    
    # CFO
    ingresos_estimados_usd: float
    opex_estimado_usd: float
    margen_bruto_usd: float
    margen_bruto_pct: float
    costo_por_kwh: float
    roi_estimado_pct: Optional[float] = None
    payback_years: Optional[float] = None
    variaciones: Dict[str, float]
    
    # COO
    pr_promedio: float
    availability_promedio_pct: float
    potencia_actual_kw: float
    estado_sistema: str  # "normal", "alerta", "critico"
    backlog_total_usd: float
    tickets_pendientes: int
    top_tickets: List[Ticket]

# ========== Real-time Series ==========
class RealtimeDataPoint(BaseModel):
    timestamp: datetime
    potencia_kw: float
    energia_kwh_intervalo: float
    irradiancia: float
    temp_modulo: float
    estado_inversores_pct: float

# ========== Settings ==========
class SettingsRequest(BaseModel):
    data_folder: str

class SettingsResponse(BaseModel):
    data_folder: str
    last_reload: Optional[str] = None
    files_loaded: Dict[str, int] = {}

# ========== Report ==========
class ReportRequest(BaseModel):
    range: str = "30d"  # 30d, 90d, YTD, 12m

class TTSRequest(BaseModel):
    text: Optional[str] = None  # Si no se provee, usar resumen automático

class WhatsAppRequest(BaseModel):
    to_phone: str
    audio_path: str
