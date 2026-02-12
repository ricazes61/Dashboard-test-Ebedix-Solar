import random
import math
from datetime import datetime, timedelta
from typing import List
from app.models.schemas import RealtimeDataPoint
from app.services.data_loader import data_loader

class RealtimeSimulator:
    """Motor de simulación de datos en tiempo real"""
    
    def __init__(self):
        self.start_time = datetime.now()
        
    def generate_series(self, hours: int = 24) -> List[RealtimeDataPoint]:
        """Genera serie temporal simulada para las últimas N horas"""
        if not data_loader.planta_data:
            raise ValueError("Datos de planta no cargados")
        
        planta = data_loader.planta_data.planta
        potencia_ac_kw = planta.potencia_ac_mw * 1000
        
        # Generar puntos cada 5 minutos
        points = []
        now = datetime.now()
        num_points = (hours * 60) // 5  # Puntos cada 5 minutos
        
        for i in range(num_points):
            timestamp = now - timedelta(minutes=5 * (num_points - i - 1))
            
            # Calcular factor solar basado en hora del día
            hour = timestamp.hour + timestamp.minute / 60.0
            solar_factor = self._calculate_solar_factor(hour)
            
            # Agregar ruido realista
            noise = random.uniform(0.92, 1.08)
            
            # Calcular potencia base
            potencia_base = potencia_ac_kw * solar_factor * noise
            
            # Simular caídas por tickets críticos
            if self._has_critical_tickets():
                potencia_base *= random.uniform(0.7, 0.95)
            
            # Calcular irradiancia (proxy)
            irradiancia = solar_factor * random.uniform(800, 1000)
            
            # Temperatura del módulo
            temp_modulo = 25 + solar_factor * random.uniform(20, 35)
            
            # Estado de inversores
            estado_inversores_pct = random.uniform(95, 100) if solar_factor > 0.1 else 0
            
            # Energía del intervalo (5 min = 1/12 hora)
            energia_kwh = potencia_base / 12
            
            point = RealtimeDataPoint(
                timestamp=timestamp,
                potencia_kw=round(potencia_base, 2),
                energia_kwh_intervalo=round(energia_kwh, 2),
                irradiancia=round(irradiancia, 2),
                temp_modulo=round(temp_modulo, 2),
                estado_inversores_pct=round(estado_inversores_pct, 2)
            )
            points.append(point)
        
        return points
    
    def _calculate_solar_factor(self, hour: float) -> float:
        """Calcula factor solar basado en curva tipo campana"""
        # Curva solar: pico a las 13:00, amanecer ~6:00, atardecer ~20:00
        if hour < 6 or hour > 20:
            return 0.0
        
        # Usar función gaussiana centrada en 13:00
        center = 13.0
        width = 4.5
        factor = math.exp(-((hour - center) ** 2) / (2 * width ** 2))
        
        return max(0, factor)
    
    def _has_critical_tickets(self) -> bool:
        """Verifica si hay tickets críticos pendientes"""
        if not data_loader.tickets:
            return False
        
        critical_tickets = [
            t for t in data_loader.tickets
            if t.criticidad.lower() in ['alta', 'crítica', 'critica']
            and t.estado.lower() in ['pendiente', 'en progreso', 'bloqueado']
        ]
        
        return len(critical_tickets) > 0
    
    def get_current_point(self) -> RealtimeDataPoint:
        """Obtiene el punto actual de la simulación"""
        series = self.generate_series(hours=1)
        return series[-1] if series else None

# Instancia global
realtime_simulator = RealtimeSimulator()
