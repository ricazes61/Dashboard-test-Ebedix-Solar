from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.models.schemas import KPIsEjecutivos, Ticket
from app.services.data_loader import data_loader
from app.services.realtime_simulator import realtime_simulator
from app.core.config import settings

class KPICalculator:
    """Servicio para calcular KPIs ejecutivos"""
    
    def calculate_executive_kpis(self, date_range: str = "30d") -> KPIsEjecutivos:
        """Calcula KPIs consolidados para CEO/CFO/COO"""
        if not data_loader.planta_data or not data_loader.historico:
            raise ValueError("Datos no cargados")
        
        # Filtrar histórico por rango
        filtered_hist = self._filter_by_range(data_loader.historico, date_range)
        
        if not filtered_hist:
            raise ValueError(f"No hay datos históricos para el rango {date_range}")
        
        planta = data_loader.planta_data.planta
        
        # KPIs CEO
        energia_real = sum(h.energia_real_kwh for h in filtered_hist)
        energia_esperada = sum(h.energia_esperada_kwh for h in filtered_hist)
        desviacion_pct = ((energia_real - energia_esperada) / energia_esperada * 100) if energia_esperada > 0 else 0
        
        # Tendencia simple
        if len(filtered_hist) >= 2:
            first_half = filtered_hist[:len(filtered_hist)//2]
            second_half = filtered_hist[len(filtered_hist)//2:]
            avg_first = sum(h.energia_real_kwh for h in first_half) / len(first_half)
            avg_second = sum(h.energia_real_kwh for h in second_half) / len(second_half)
            tendencia = "up" if avg_second > avg_first * 1.02 else "down" if avg_second < avg_first * 0.98 else "stable"
        else:
            tendencia = "stable"
        
        co2_evitado = energia_real * settings.co2_factor_kg_per_kwh
        
        # Alertas (basadas en umbrales)
        alertas = self._calculate_alertas(filtered_hist)
        
        # KPIs CFO
        ingresos = sum(h.ingresos_estimados_usd for h in filtered_hist)
        opex = sum(h.opex_estimado_usd for h in filtered_hist)
        margen_bruto = ingresos - opex
        margen_bruto_pct = (margen_bruto / ingresos * 100) if ingresos > 0 else 0
        costo_por_kwh = opex / energia_real if energia_real > 0 else 0
        
        # ROI simplificado (estimación)
        roi_estimado = None
        payback_years = None
        
        variaciones = {
            "energia_vs_esperada_pct": desviacion_pct,
            "ingresos_vs_objetivo_pct": 0.0,  # Simplificado
            "opex_vs_presupuesto_pct": 0.0,   # Simplificado
        }
        
        # KPIs COO
        pr_promedio = sum(h.pr_real for h in filtered_hist) / len(filtered_hist)
        availability_promedio = sum(h.availability_real_pct for h in filtered_hist) / len(filtered_hist)
        
        # Potencia actual (de simulación)
        current_point = realtime_simulator.get_current_point()
        potencia_actual = current_point.potencia_kw if current_point else 0
        
        # Estado del sistema
        if pr_promedio < planta.target_pr * 0.9:
            estado_sistema = "critico"
        elif pr_promedio < planta.target_pr * 0.95:
            estado_sistema = "alerta"
        else:
            estado_sistema = "normal"
        
        # Backlog de tickets
        tickets_pendientes = [
            t for t in data_loader.tickets
            if t.estado.lower() in ['pendiente', 'en progreso', 'bloqueado']
        ]
        backlog_total = sum(t.costo_estimado_usd for t in tickets_pendientes)
        
        # Top 5 tickets por costo
        top_tickets = sorted(
            tickets_pendientes,
            key=lambda x: x.costo_estimado_usd,
            reverse=True
        )[:5]
        
        return KPIsEjecutivos(
            # CEO
            energia_real_kwh=energia_real,
            energia_esperada_kwh=energia_esperada,
            desviacion_pct=round(desviacion_pct, 2),
            tendencia=tendencia,
            co2_evitado_kg=round(co2_evitado, 2),
            alertas_principales=alertas,
            
            # CFO
            ingresos_estimados_usd=round(ingresos, 2),
            opex_estimado_usd=round(opex, 2),
            margen_bruto_usd=round(margen_bruto, 2),
            margen_bruto_pct=round(margen_bruto_pct, 2),
            costo_por_kwh=round(costo_por_kwh, 4),
            roi_estimado_pct=roi_estimado,
            payback_years=payback_years,
            variaciones=variaciones,
            
            # COO
            pr_promedio=round(pr_promedio, 4),
            availability_promedio_pct=round(availability_promedio, 2),
            potencia_actual_kw=round(potencia_actual, 2),
            estado_sistema=estado_sistema,
            backlog_total_usd=round(backlog_total, 2),
            tickets_pendientes=len(tickets_pendientes),
            top_tickets=top_tickets
        )
    
    def _filter_by_range(self, historico: List, date_range: str) -> List:
        """Filtra histórico por rango de fechas"""
        now = datetime.now()
        
        if date_range == "30d":
            start_date = now - timedelta(days=30)
        elif date_range == "90d":
            start_date = now - timedelta(days=90)
        elif date_range == "YTD":
            start_date = datetime(now.year, 1, 1)
        elif date_range == "12m":
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(days=30)
        
        return [
            h for h in historico
            if datetime.strptime(h.fecha, '%Y-%m-%d') >= start_date
        ]
    
    def _calculate_alertas(self, historico: List) -> List[str]:
        """Calcula alertas basadas en umbrales"""
        if not data_loader.planta_data:
            return []
        
        alertas = []
        planta = data_loader.planta_data.planta
        umbrales = data_loader.planta_data.umbrales
        
        # PR bajo
        pr_promedio = sum(h.pr_real for h in historico) / len(historico)
        umbral_pr = next((u for u in umbrales if u.kpi.lower() == 'pr'), None)
        
        if umbral_pr and pr_promedio < umbral_pr.umbral_rojo:
            alertas.append(f"PR crítico: {pr_promedio:.2%} (objetivo: {planta.target_pr:.2%})")
        elif umbral_pr and pr_promedio < umbral_pr.umbral_amarillo:
            alertas.append(f"PR bajo: {pr_promedio:.2%} (objetivo: {planta.target_pr:.2%})")
        
        # Availability baja
        avail_promedio = sum(h.availability_real_pct for h in historico) / len(historico)
        umbral_avail = next((u for u in umbrales if u.kpi.lower() == 'availability'), None)
        
        if umbral_avail and avail_promedio < umbral_avail.umbral_rojo:
            alertas.append(f"Disponibilidad crítica: {avail_promedio:.1f}% (objetivo: {planta.target_availability:.1f}%)")
        
        return alertas[:5]  # Máximo 5 alertas

# Instancia global
kpi_calculator = KPICalculator()
