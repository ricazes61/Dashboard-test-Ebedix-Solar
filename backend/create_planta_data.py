import pandas as pd
from pathlib import Path

# Crear directorio de salida
output_dir = Path("../data/input")
output_dir.mkdir(parents=True, exist_ok=True)

# === Hoja 1: Planta ===
planta_data = {
    'planta_id': ['PV-001'],
    'nombre_planta': ['Solar del Valle'],
    'pais': ['Argentina'],
    'provincia_estado': ['Mendoza'],
    'ciudad': ['San Rafael'],
    'lat': [-34.6177],
    'lon': [-68.3301],
    'zona_horaria': ['America/Argentina/Buenos_Aires'],
    'potencia_dc_mwp': [50.0],
    'potencia_ac_mw': [45.0],
    'cantidad_paneles': [125000],
    'cantidad_strings': [2500],
    'cantidad_inversores': [45],
    'fecha_puesta_en_marcha': ['2022-06-15'],
    'tarifa_usd_mwh': [65.0],
    'target_pr': [0.82],
    'target_availability': [98.5],
    'soiling_loss_target_pct': [2.0],
    'degradation_annual_pct': [0.5],
    'curtailment_policy': ['5% durante picos de demanda']
}

df_planta = pd.DataFrame(planta_data)

# === Hoja 2: Equipos ===
equipos_data = {
    'equipo_id': ['INV-001', 'INV-002', 'INV-003', 'INV-004', 'INV-005', 'TRAFO-001', 'TRAFO-002'],
    'tipo': ['Inversor', 'Inversor', 'Inversor', 'Inversor', 'Inversor', 'Transformador', 'Transformador'],
    'fabricante': ['SMA', 'SMA', 'SMA', 'Huawei', 'Huawei', 'ABB', 'ABB'],
    'modelo': ['SC2200', 'SC2200', 'SC2200', 'SUN2000-215KTL', 'SUN2000-215KTL', 'DT-1250', 'DT-1250'],
    'capacidad_kw': [1000, 1000, 1000, 1000, 1000, 2500, 2500],
    'estado_base': ['Operativo', 'Operativo', 'Operativo', 'Operativo', 'Mantenimiento', 'Operativo', 'Operativo']
}

df_equipos = pd.DataFrame(equipos_data)

# === Hoja 3: Umbrales ===
umbrales_data = {
    'kpi': ['PR', 'PR', 'Availability', 'Availability', 'Soiling', 'Soiling'],
    'umbral_amarillo': [0.78, 0.75, 95.0, 92.0, 3.0, 5.0],
    'umbral_rojo': [0.75, 0.70, 92.0, 88.0, 5.0, 8.0],
    'descripcion_alerta': [
        'PR por debajo del 78% - Revisar equipos',
        'PR crítico por debajo del 75% - Acción inmediata',
        'Disponibilidad por debajo del 95% - Revisar mantenimiento',
        'Disponibilidad crítica por debajo del 92% - Acción inmediata',
        'Pérdidas por soiling superiores al 3% - Programar limpieza',
        'Pérdidas críticas por soiling superiores al 5% - Limpieza urgente'
    ]
}

df_umbrales = pd.DataFrame(umbrales_data)

# Guardar en Excel con múltiples hojas
with pd.ExcelWriter(output_dir / 'Parametros_Planta.xlsx', engine='openpyxl') as writer:
    df_planta.to_excel(writer, sheet_name='Planta', index=False)
    df_equipos.to_excel(writer, sheet_name='Equipos', index=False)
    df_umbrales.to_excel(writer, sheet_name='Umbrales', index=False)

print("✓ Parametros_Planta.xlsx creado exitosamente")
