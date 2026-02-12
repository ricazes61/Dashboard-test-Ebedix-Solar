from openai import OpenAI
from pathlib import Path
from datetime import datetime
from typing import Optional
import logging

from app.core.config import settings
from app.services.kpi_calculator import kpi_calculator
from app.services.data_loader import data_loader

logger = logging.getLogger(__name__)

class TTSService:
    """Servicio de Text-to-Speech usando OpenAI"""
    
    def __init__(self, output_folder: str = "./data/output"):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.client = None
        
        if settings.openai_api_key:
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                logger.warning(f"No se pudo inicializar OpenAI client: {e}")
    
    def generate_audio_summary(
        self,
        date_range: str = "30d",
        custom_text: Optional[str] = None
    ) -> str:
        """Genera audio con resumen ejecutivo"""
        
        if not self.client:
            # Modo simulación
            logger.warning("OpenAI API key no configurada. Modo simulación activado.")
            return self._generate_mock_audio()
        
        # Generar texto del resumen
        if custom_text:
            text = custom_text
        else:
            text = self._generate_summary_text(date_range)
        
        # Generar audio con OpenAI TTS
        try:
            response = self.client.audio.speech.create(
                model=settings.openai_tts_model,
                voice=settings.openai_tts_voice,
                input=text
            )
            
            # Guardar audio
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resumen_ejecutivo_{timestamp}.mp3"
            filepath = self.output_folder / filename
            
            response.stream_to_file(str(filepath))
            
            logger.info(f"Audio generado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error generando audio con OpenAI: {str(e)}")
            raise ValueError(f"Error generando audio: {str(e)}")
    
    def _generate_summary_text(self, date_range: str) -> str:
        """Genera texto del resumen ejecutivo en español"""
        if not data_loader.planta_data:
            raise ValueError("Datos de planta no cargados")
        
        planta = data_loader.planta_data.planta
        kpis = kpi_calculator.calculate_executive_kpis(date_range)
        
        # Crear resumen de 30-60 segundos
        text = f"""
        Resumen ejecutivo de {planta.nombre_planta}.
        
        Durante el período analizado, la planta generó {kpis.energia_real_kwh:,.0f} kilovatios hora, 
        con una desviación de {kpis.desviacion_pct:+.1f} por ciento respecto a lo esperado.
        
        El Performance Ratio alcanzó {kpis.pr_promedio:.1%}, 
        y la disponibilidad fue de {kpis.availability_promedio_pct:.1f} por ciento.
        
        Los ingresos estimados totalizaron {kpis.ingresos_estimados_usd:,.0f} dólares,
        con un margen bruto de {kpis.margen_bruto_pct:.1f} por ciento.
        
        Se evitaron {kpis.co2_evitado_kg:,.0f} kilogramos de emisiones de C O 2.
        
        El backlog de mantenimiento asciende a {kpis.backlog_total_usd:,.0f} dólares,
        con {kpis.tickets_pendientes} tickets pendientes.
        
        El estado general del sistema es {kpis.estado_sistema}.
        """
        
        # Agregar alertas si existen
        if kpis.alertas_principales:
            text += "\n\nAlertas principales: " + ". ".join(kpis.alertas_principales[:2])
        
        return text.strip()
    
    def _generate_mock_audio(self) -> str:
        """Genera archivo de audio simulado (mock)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resumen_ejecutivo_{timestamp}_MOCK.mp3"
        filepath = self.output_folder / filename
        
        # Crear archivo vacío como placeholder
        filepath.touch()
        
        logger.info(f"Audio simulado generado: {filepath}")
        return str(filepath)

# Instancia global
tts_service = TTSService()
