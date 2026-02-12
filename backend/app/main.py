from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.api import health, settings as settings_api, data, reports

# Configurar logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Crear aplicación
app = FastAPI(
    title="Solar PV Analytics API",
    description="API para análisis ejecutivo de plantas solares fotovoltaicas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = settings.cors_origins.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(settings_api.router, prefix="/api", tags=["Settings"])
app.include_router(data.router, prefix="/api", tags=["Data"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    logger.info("=" * 60)
    logger.info("Solar PV Analytics API - Iniciando")
    logger.info("=" * 60)
    logger.info(f"Entorno: {'DEBUG' if settings.debug else 'PRODUCTION'}")
    logger.info(f"CORS Origins: {origins}")
    logger.info(f"OpenAI TTS: {'Configurado' if settings.openai_api_key else 'NO configurado (modo simulación)'}")
    logger.info(f"Twilio WhatsApp: {'Configurado' if settings.twilio_account_sid else 'NO configurado (modo simulación)'}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    logger.info("Solar PV Analytics API - Cerrando")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug
    )
