import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Configuración
output_dir = Path("../data/input")
output_dir.mkdir(parents=True, exist_ok=True)

# Generar tickets
tickets_data = []

estados = ['Pendiente', 'En Progreso', 'Bloqueado', 'Cerrado']
tipos = ['Correctivo', 'Preventivo', 'Predictivo', 'Emergencia']
criticidades = ['Baja', 'Media', 'Alta', 'Crítica']
equipos = ['INV-001', 'INV-002', 'INV-003', 'INV-004', 'INV-005', 'TRAFO-001', 'TRAFO-002', None]
responsables = ['Juan Pérez', 'María González', 'Carlos Rodríguez', 'Ana Martínez']

descripciones = [
    'Falla en inversor - mensaje de error en pantalla',
    'Mantenimiento preventivo trimestral - limpieza de paneles',
    'Revisión de conexiones en string',
    'Reemplazo de fusibles en caja combinadora',
    'Actualización de firmware de inversor',
    'Reparación de sistema de monitoreo',
    'Limpieza profunda de módulos fotovoltaicos',
    'Revisión de transformador - ruido anormal',
    'Mantenimiento de sistema SCADA',
    'Calibración de sensores de irradiancia',
    'Reemplazo de ventiladores en inversor',
    'Inspección termográfica de paneles',
    'Reparación de estructura de soporte',
    'Mantenimiento de sistema de seguridad',
    'Revisión de sistema de puesta a tierra'
]

# Generar 50 tickets
num_tickets = 50

for i in range(num_tickets):
    ticket_id = f"TKT-{i+1:04d}"
    
    # Distribución realista de estados
    if i < 15:
        estado = 'Pendiente'
    elif i < 25:
        estado = 'En Progreso'
    elif i < 30:
        estado = 'Bloqueado'
    else:
        estado = 'Cerrado'
    
    # Distribución de criticidad
    if i < 5:
        criticidad = 'Crítica'
    elif i < 15:
        criticidad = 'Alta'
    elif i < 35:
        criticidad = 'Media'
    else:
        criticidad = 'Baja'
    
    tipo = np.random.choice(tipos)
    equipo_id = np.random.choice(equipos)
    descripcion = np.random.choice(descripciones)
    responsable = np.random.choice(responsables)
    
    # Fecha de creación (últimos 60 días)
    days_ago = np.random.randint(1, 60)
    fecha_creacion = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    # Costo basado en criticidad
    if criticidad == 'Crítica':
        costo_base = np.random.uniform(15000, 50000)
    elif criticidad == 'Alta':
        costo_base = np.random.uniform(5000, 15000)
    elif criticidad == 'Media':
        costo_base = np.random.uniform(1000, 5000)
    else:
        costo_base = np.random.uniform(200, 1000)
    
    costo_estimado_usd = round(costo_base, 2)
    
    # Impacto en energía
    if criticidad in ['Crítica', 'Alta']:
        impacto_kwh = np.random.uniform(5000, 25000)
    elif criticidad == 'Media':
        impacto_kwh = np.random.uniform(500, 5000)
    else:
        impacto_kwh = np.random.uniform(0, 500)
    
    impacto_estimado_kwh = round(impacto_kwh, 2)
    
    # SLA
    if criticidad == 'Crítica':
        sla_objetivo_horas = 4
    elif criticidad == 'Alta':
        sla_objetivo_horas = 24
    elif criticidad == 'Media':
        sla_objetivo_horas = 72
    else:
        sla_objetivo_horas = 168
    
    # Fecha estimada de resolución
    if estado == 'Cerrado':
        fecha_estimada_resolucion = None
    else:
        days_to_resolve = np.random.randint(1, 15)
        fecha_estimada_resolucion = (datetime.now() + timedelta(days=days_to_resolve)).strftime('%Y-%m-%d')
    
    tickets_data.append({
        'ticket_id': ticket_id,
        'planta_id': 'PV-001',
        'fecha_creacion': fecha_creacion,
        'estado': estado,
        'tipo': tipo,
        'criticidad': criticidad,
        'equipo_id': equipo_id,
        'descripcion': descripcion,
        'costo_estimado_usd': costo_estimado_usd,
        'impacto_estimado_kwh': impacto_estimado_kwh,
        'sla_objetivo_horas': sla_objetivo_horas,
        'responsable': responsable,
        'fecha_estimada_resolucion': fecha_estimada_resolucion
    })

df = pd.DataFrame(tickets_data)
df.to_csv(output_dir / 'Tickets_Mantenimiento.csv', index=False)

print(f"✓ Tickets_Mantenimiento.csv creado con {len(df)} tickets")
print(f"  - Pendientes: {len(df[df['estado']=='Pendiente'])}")
print(f"  - En Progreso: {len(df[df['estado']=='En Progreso'])}")
print(f"  - Bloqueados: {len(df[df['estado']=='Bloqueado'])}")
print(f"  - Cerrados: {len(df[df['estado']=='Cerrado'])}")
