from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Data
    data_folder: str = "./data/input"
    
    # OpenAI TTS
    openai_api_key: Optional[str] = None
    openai_tts_model: str = "tts-1"
    openai_tts_voice: str = "alloy"
    
    # ElevenLabs TTS (alternativa)
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    
    # Twilio WhatsApp
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_from: Optional[str] = None
    
    # WhatsApp Cloud API (alternativa)
    meta_access_token: Optional[str] = None
    meta_phone_number_id: Optional[str] = None
    meta_whatsapp_from: Optional[str] = None
    
    # Planta solar
    co2_factor_kg_per_kwh: float = 0.5
    timezone: str = "America/Argentina/Buenos_Aires"
    
    # Simulación
    simulation_interval_minutes: int = 5
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
