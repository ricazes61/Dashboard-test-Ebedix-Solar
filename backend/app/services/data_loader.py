import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.schemas import (
    PlantaData, PlantaBase, EquipoBase, UmbralBase,
    HistoricoPerformance, Ticket
)
from app.core.config import settings

class DataLoader:
    """Servicio para cargar y cachear datos desde archivos"""
    
    def __init__(self):
        self.data_folder: Optional[Path] = None
        self.planta_data: Optional[PlantaData] = None
        self.historico: List[HistoricoPerformance] = []
        self.tickets: List[Ticket] = []
        self.last_reload: Optional[datetime] = None
        self.files_loaded: Dict[str, int] = {}
        
    def set_data_folder(self, folder_path: str) -> None:
        """Configura el folder de datos"""
        self.data_folder = Path(folder_path)
        if not self.data_folder.exists():
            raise FileNotFoundError(f"El folder '{folder_path}' no existe")
    
    def reload_data(self) -> Dict[str, Any]:
        """Recarga todos los datos desde los archivos"""
        if not self.data_folder:
            raise ValueError("Data folder no configurado. Usar /api/settings primero.")
        
        errors = []
        results = {}
        
        # Cargar parámetros de planta
        try:
            self.planta_data = self._load_planta_params()
            results['planta'] = 'OK'
            self.files_loaded['Parametros_Planta.xlsx'] = (
                1 + len(self.planta_data.equipos) + len(self.planta_data.umbrales)
            )
        except Exception as e:
            errors.append(f"Error cargando Parametros_Planta.xlsx: {str(e)}")
            results['planta'] = f'ERROR: {str(e)}'
        
        # Cargar histórico
        try:
            self.historico = self._load_historico()
            results['historico'] = 'OK'
            self.files_loaded['Historico_Performance.csv'] = len(self.historico)
        except Exception as e:
            errors.append(f"Error cargando Historico_Performance.csv: {str(e)}")
            results['historico'] = f'ERROR: {str(e)}'
        
        # Cargar tickets
        try:
            self.tickets = self._load_tickets()
            results['tickets'] = 'OK'
            self.files_loaded['Tickets_Mantenimiento.csv'] = len(self.tickets)
        except Exception as e:
            errors.append(f"Error cargando Tickets_Mantenimiento.csv: {str(e)}")
            results['tickets'] = f'ERROR: {str(e)}'
        
        self.last_reload = datetime.now()
        
        return {
            'success': len(errors) == 0,
            'results': results,
            'errors': errors,
            'files_loaded': self.files_loaded,
            'last_reload': self.last_reload.isoformat()
        }
    
    def _load_planta_params(self) -> PlantaData:
        """Carga parámetros de planta desde Excel"""
        file_path = self.data_folder / "Parametros_Planta.xlsx"
        if not file_path.exists():
            raise FileNotFoundError(
                f"Archivo 'Parametros_Planta.xlsx' no encontrado en {self.data_folder}"
            )
        
        # Leer hojas
        try:
            df_planta = pd.read_excel(file_path, sheet_name='Planta')
            df_equipos = pd.read_excel(file_path, sheet_name='Equipos')
            df_umbrales = pd.read_excel(file_path, sheet_name='Umbrales')
        except Exception as e:
            raise ValueError(f"Error leyendo hojas del Excel: {str(e)}")
        
        # Validar columnas planta
        required_planta_cols = [
            'planta_id', 'nombre_planta', 'pais', 'provincia_estado', 'ciudad',
            'lat', 'lon', 'zona_horaria', 'potencia_dc_mwp', 'potencia_ac_mw',
            'cantidad_paneles', 'cantidad_strings', 'cantidad_inversores',
            'fecha_puesta_en_marcha', 'tarifa_usd_mwh', 'target_pr',
            'target_availability', 'soiling_loss_target_pct',
            'degradation_annual_pct', 'curtailment_policy'
        ]
        missing = set(required_planta_cols) - set(df_planta.columns)
        if missing:
            raise ValueError(f"Columnas faltantes en hoja 'Planta': {missing}")
        
        # Parsear planta (tomar primera fila)
        row = df_planta.iloc[0].to_dict()
        planta = PlantaBase(**row)
        
        # Parsear equipos
        equipos = [EquipoBase(**row) for _, row in df_equipos.iterrows()]
        
        # Parsear umbrales
        umbrales = [UmbralBase(**row) for _, row in df_umbrales.iterrows()]
        
        return PlantaData(planta=planta, equipos=equipos, umbrales=umbrales)
    
    def _load_historico(self) -> List[HistoricoPerformance]:
        """Carga histórico de performance desde CSV"""
        file_path = self.data_folder / "Historico_Performance.csv"
        if not file_path.exists():
            raise FileNotFoundError(
                f"Archivo 'Historico_Performance.csv' no encontrado en {self.data_folder}"
            )
        
        df = pd.read_csv(file_path)
        
        # Validar columnas
        required_cols = [
            'fecha', 'planta_id', 'energia_real_kwh', 'energia_esperada_kwh',
            'irradiancia_poa_kwh_m2', 'pr_real', 'availability_real_pct',
            'curtailment_kwh', 'perdida_soiling_kwh', 'perdida_otros_kwh',
            'ingresos_estimados_usd', 'opex_estimado_usd'
        ]
        missing = set(required_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Columnas faltantes en Historico_Performance.csv: {missing}")
        
        # Parsear fechas
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        
        return [HistoricoPerformance(**row) for _, row in df.iterrows()]
    
    def _load_tickets(self) -> List[Ticket]:
        """Carga tickets de mantenimiento desde CSV"""
        file_path = self.data_folder / "Tickets_Mantenimiento.csv"
        if not file_path.exists():
            raise FileNotFoundError(
                f"Archivo 'Tickets_Mantenimiento.csv' no encontrado en {self.data_folder}"
            )
        
        df = pd.read_csv(file_path)
        
        # Validar columnas
        required_cols = [
            'ticket_id', 'planta_id', 'fecha_creacion', 'estado', 'tipo',
            'criticidad', 'descripcion', 'costo_estimado_usd',
            'impacto_estimado_kwh', 'sla_objetivo_horas', 'responsable'
        ]
        missing = set(required_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Columnas faltantes en Tickets_Mantenimiento.csv: {missing}")
        
        # Parsear fechas
        df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion']).dt.strftime('%Y-%m-%d')
        if 'fecha_estimada_resolucion' in df.columns:
            df['fecha_estimada_resolucion'] = pd.to_datetime(
                df['fecha_estimada_resolucion'], errors='coerce'
            ).dt.strftime('%Y-%m-%d')
        
        return [Ticket(**row.to_dict()) for _, row in df.iterrows()]

# Instancia global
data_loader = DataLoader()
