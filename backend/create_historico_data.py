import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Configuración
output_dir = Path("../data/input")
output_dir.mkdir(parents=True, exist_ok=True)

# Generar 90 días de histórico
num_days = 90
end_date = datetime.now()
start_date = end_date - timedelta(days=num_days)

dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Parámetros de la planta
potencia_dc_mwp = 50.0
target_pr = 0.82
target_availability = 98.5
tarifa_usd_mwh = 65.0

# Generar datos
data = []

for date in dates:
    # Simular variación estacional y aleatoria
    season_factor = 1.0 + 0.2 * np.sin((date.dayofyear / 365) * 2 * np.pi - np.pi/2)
    daily_hours_equiv = 5.5 * season_factor  # Horas equivalentes de sol
    
    # Energía esperada (kWh)
    energia_esperada_kwh = potencia_dc_mwp * 1000 * daily_hours_equiv * target_pr
    
    # Energía real con variación aleatoria
    variation = np.random.normal(1.0, 0.05)  # +/- 5%
    energia_real_kwh = energia_esperada_kwh * variation
    
    # Irradiancia
    irradiancia_poa = daily_hours_equiv * np.random.uniform(0.95, 1.05)
    
    # PR real
    pr_real = (energia_real_kwh / (potencia_dc_mwp * 1000 * irradiancia_poa)) if irradiancia_poa > 0 else 0
    pr_real = max(0.70, min(0.88, pr_real))
    
    # Availability
    availability_real = np.random.uniform(96.0, 99.8)
    
    # Pérdidas
    curtailment_kwh = energia_esperada_kwh * np.random.uniform(0.02, 0.05)
    perdida_soiling_kwh = energia_esperada_kwh * np.random.uniform(0.015, 0.035)
    perdida_otros_kwh = energia_esperada_kwh * np.random.uniform(0.01, 0.03)
    
    # Financiero
    ingresos_estimados_usd = (energia_real_kwh / 1000) * tarifa_usd_mwh
    opex_estimado_usd = ingresos_estimados_usd * np.random.uniform(0.15, 0.25)
    
    data.append({
        'fecha': date.strftime('%Y-%m-%d'),
        'planta_id': 'PV-001',
        'energia_real_kwh': round(energia_real_kwh, 2),
        'energia_esperada_kwh': round(energia_esperada_kwh, 2),
        'irradiancia_poa_kwh_m2': round(irradiancia_poa, 2),
        'pr_real': round(pr_real, 4),
        'availability_real_pct': round(availability_real, 2),
        'curtailment_kwh': round(curtailment_kwh, 2),
        'perdida_soiling_kwh': round(perdida_soiling_kwh, 2),
        'perdida_otros_kwh': round(perdida_otros_kwh, 2),
        'ingresos_estimados_usd': round(ingresos_estimados_usd, 2),
        'opex_estimado_usd': round(opex_estimado_usd, 2)
    })

df = pd.DataFrame(data)
df.to_csv(output_dir / 'Historico_Performance.csv', index=False)

print(f"✓ Historico_Performance.csv creado con {len(df)} registros")
