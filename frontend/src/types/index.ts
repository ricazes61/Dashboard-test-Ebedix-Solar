// ========== Planta ==========
export interface Planta {
  planta_id: string;
  nombre_planta: string;
  pais: string;
  provincia_estado: string;
  ciudad: string;
  lat: number;
  lon: number;
  zona_horaria: string;
  potencia_dc_mwp: number;
  potencia_ac_mw: number;
  cantidad_paneles: number;
  cantidad_strings: number;
  cantidad_inversores: number;
  fecha_puesta_en_marcha: string;
  tarifa_usd_mwh: number;
  target_pr: number;
  target_availability: number;
  soiling_loss_target_pct: number;
  degradation_annual_pct: number;
  curtailment_policy: string;
}

export interface Equipo {
  equipo_id: string;
  tipo: string;
  fabricante: string;
  modelo: string;
  capacidad_kw: number;
  estado_base: string;
}

export interface Umbral {
  kpi: string;
  umbral_amarillo: number;
  umbral_rojo: number;
  descripcion_alerta: string;
}

export interface PlantaData {
  planta: Planta;
  equipos: Equipo[];
  umbrales: Umbral[];
}

// ========== Performance ==========
export interface HistoricoPerformance {
  fecha: string;
  planta_id: string;
  energia_real_kwh: number;
  energia_esperada_kwh: number;
  irradiancia_poa_kwh_m2: number;
  pr_real: number;
  availability_real_pct: number;
  curtailment_kwh: number;
  perdida_soiling_kwh: number;
  perdida_otros_kwh: number;
  ingresos_estimados_usd: number;
  opex_estimado_usd: number;
}

// ========== Tickets ==========
export interface Ticket {
  ticket_id: string;
  planta_id: string;
  fecha_creacion: string;
  estado: string;
  tipo: string;
  criticidad: string;
  equipo_id?: string;
  descripcion: string;
  costo_estimado_usd: number;
  impacto_estimado_kwh: number;
  sla_objetivo_horas: number;
  responsable: string;
  fecha_estimada_resolucion?: string;
}

// ========== KPIs Ejecutivos ==========
export interface KPIsEjecutivos {
  // CEO
  energia_real_kwh: number;
  energia_esperada_kwh: number;
  desviacion_pct: number;
  tendencia: 'up' | 'down' | 'stable';
  co2_evitado_kg: number;
  alertas_principales: string[];
  
  // CFO
  ingresos_estimados_usd: number;
  opex_estimado_usd: number;
  margen_bruto_usd: number;
  margen_bruto_pct: number;
  costo_por_kwh: number;
  roi_estimado_pct?: number;
  payback_years?: number;
  variaciones: {
    [key: string]: number;
  };
  
  // COO
  pr_promedio: number;
  availability_promedio_pct: number;
  potencia_actual_kw: number;
  estado_sistema: 'normal' | 'alerta' | 'critico';
  backlog_total_usd: number;
  tickets_pendientes: number;
  top_tickets: Ticket[];
}

// ========== Real-time Series ==========
export interface RealtimeDataPoint {
  timestamp: string;
  potencia_kw: number;
  energia_kwh_intervalo: number;
  irradiancia: number;
  temp_modulo: number;
  estado_inversores_pct: number;
}

// ========== Settings ==========
export interface Settings {
  data_folder: string;
  last_reload?: string;
  files_loaded?: {
    [key: string]: number;
  };
}

// ========== API Responses ==========
export interface ReloadResponse {
  success: boolean;
  results: {
    [key: string]: string;
  };
  errors: string[];
  files_loaded: {
    [key: string]: number;
  };
  last_reload: string;
}

export interface TTSResponse {
  success: boolean;
  audio_path: string;
  filename: string;
  message: string;
}

export interface WhatsAppResponse {
  success: boolean;
  mode: 'real' | 'simulation';
  message: string;
  sid: string;
  status: string;
  note?: string;
}
