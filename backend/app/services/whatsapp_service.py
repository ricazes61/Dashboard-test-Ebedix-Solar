from twilio.rest import Client
from pathlib import Path
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Servicio de envío de mensajes por WhatsApp usando Twilio"""
    
    def __init__(self):
        self.client = None
        
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
    
    def send_audio(self, to_phone: str, audio_path: str) -> dict:
        """
        Envía audio por WhatsApp
        
        Args:
            to_phone: Número de teléfono en formato E.164 (ej: +5491112345678)
            audio_path: Ruta al archivo de audio
        
        Returns:
            dict con resultado del envío
        """
        
        # Validar número de teléfono
        if not to_phone.startswith('+'):
            raise ValueError(
                "El número de teléfono debe estar en formato E.164 (comenzar con +)"
            )
        
        # Validar que el archivo existe
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")
        
        # Modo simulación si no hay credenciales
        if not self.client:
            logger.warning("Credenciales de Twilio no configuradas. Modo simulación.")
            return {
                "success": True,
                "mode": "simulation",
                "message": f"SIMULACIÓN: Audio se enviaría a {to_phone}",
                "sid": "MOCK_SID_123456",
                "status": "simulated"
            }
        
        try:
            # Nota: Para enviar archivos multimedia con Twilio WhatsApp,
            # el archivo debe estar accesible públicamente via URL.
            # Para demo local, simular el envío.
            
            # En producción, subir el archivo a un servidor accesible
            # y usar la URL pública aquí
            
            # Por ahora, enviar mensaje de texto indicando que hay audio
            message = self.client.messages.create(
                from_=settings.twilio_whatsapp_from,
                body=f"📊 Nuevo reporte ejecutivo disponible. Audio generado el {Path(audio_path).stat().st_mtime}",
                to=f"whatsapp:{to_phone}"
            )
            
            logger.info(f"Mensaje WhatsApp enviado a {to_phone}. SID: {message.sid}")
            
            return {
                "success": True,
                "mode": "real",
                "message": "Mensaje enviado exitosamente",
                "sid": message.sid,
                "status": message.status,
                "note": "Para enviar el audio, debe estar accesible via URL pública"
            }
            
        except Exception as e:
            logger.error(f"Error enviando mensaje WhatsApp: {str(e)}")
            raise ValueError(f"Error enviando WhatsApp: {str(e)}")
    
    def send_text(self, to_phone: str, message: str) -> dict:
        """
        Envía mensaje de texto por WhatsApp
        
        Args:
            to_phone: Número de teléfono en formato E.164
            message: Texto del mensaje
        
        Returns:
            dict con resultado del envío
        """
        
        if not to_phone.startswith('+'):
            raise ValueError(
                "El número de teléfono debe estar en formato E.164 (comenzar con +)"
            )
        
        if not self.client:
            logger.warning("Credenciales de Twilio no configuradas. Modo simulación.")
            return {
                "success": True,
                "mode": "simulation",
                "message": f"SIMULACIÓN: Mensaje se enviaría a {to_phone}",
                "sid": "MOCK_SID_123456",
                "status": "simulated"
            }
        
        try:
            msg = self.client.messages.create(
                from_=settings.twilio_whatsapp_from,
                body=message,
                to=f"whatsapp:{to_phone}"
            )
            
            logger.info(f"Mensaje WhatsApp enviado a {to_phone}. SID: {msg.sid}")
            
            return {
                "success": True,
                "mode": "real",
                "message": "Mensaje enviado exitosamente",
                "sid": msg.sid,
                "status": msg.status
            }
            
        except Exception as e:
            logger.error(f"Error enviando mensaje WhatsApp: {str(e)}")
            raise ValueError(f"Error enviando WhatsApp: {str(e)}")

# Instancia global
whatsapp_service = WhatsAppService()
