from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.models.schemas import PlantaData, KPIsEjecutivos, RealtimeDataPoint, Ticket
from app.services.data_loader import data_loader
from app.services.kpi_calculator import kpi_calculator
from app.services.realtime_simulator import realtime_simulator

router = APIRouter()

@router.post("/data/reload")
async def reload_data() -> Dict[str, Any]:
    """Recarga datos desde archivos"""
    try:
        result = data_loader.reload_data()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/plant", response_model=PlantaData)
async def get_plant_data() -> PlantaData:
    """Obtiene parámetros de planta, equipos y umbrales"""
    if not data_loader.planta_data:
        raise HTTPException(
            status_code=400,
            detail="Datos no cargados. Usar POST /api/data/reload primero."
        )
    
    return data_loader.planta_data

@router.get("/kpis/exec", response_model=KPIsEjecutivos)
async def get_executive_kpis(
    range: str = Query("30d", description="Rango: 30d, 90d, YTD, 12m")
) -> KPIsEjecutivos:
    """Obtiene KPIs consolidados para CEO/CFO/COO"""
    if not data_loader.planta_data or not data_loader.historico:
        raise HTTPException(
            status_code=400,
            detail="Datos no cargados. Usar POST /api/data/reload primero."
        )
    
    try:
        kpis = kpi_calculator.calculate_executive_kpis(range)
        return kpis
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando KPIs: {str(e)}")

@router.get("/series/realtime", response_model=List[RealtimeDataPoint])
async def get_realtime_series(
    hours: int = Query(24, ge=1, le=168, description="Horas de histórico (1-168)")
) -> List[RealtimeDataPoint]:
    """Obtiene serie temporal simulada en tiempo real"""
    if not data_loader.planta_data:
        raise HTTPException(
            status_code=400,
            detail="Datos no cargados. Usar POST /api/data/reload primero."
        )
    
    try:
        series = realtime_simulator.generate_series(hours)
        return series
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando serie: {str(e)}")

@router.get("/tickets", response_model=List[Ticket])
async def get_tickets(
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    sort: str = Query("costo_desc", description="Ordenamiento: costo_desc, costo_asc, fecha"),
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Límite de resultados")
) -> List[Ticket]:
    """Obtiene tickets de mantenimiento con filtros"""
    if not data_loader.tickets:
        raise HTTPException(
            status_code=400,
            detail="Datos no cargados. Usar POST /api/data/reload primero."
        )
    
    # Filtrar por estado
    tickets = data_loader.tickets
    
    if status:
        status_lower = status.lower()
        if status_lower == "pendiente":
            tickets = [
                t for t in tickets
                if t.estado.lower() in ['pendiente', 'en progreso', 'bloqueado']
            ]
        else:
            tickets = [t for t in tickets if t.estado.lower() == status_lower]
    
    # Ordenar
    if sort == "costo_desc":
        tickets = sorted(tickets, key=lambda x: x.costo_estimado_usd, reverse=True)
    elif sort == "costo_asc":
        tickets = sorted(tickets, key=lambda x: x.costo_estimado_usd)
    elif sort == "fecha":
        tickets = sorted(tickets, key=lambda x: x.fecha_creacion, reverse=True)
    
    # Limitar
    if limit:
        tickets = tickets[:limit]
    
    return tickets
