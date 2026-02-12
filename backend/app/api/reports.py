from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Dict, Any

from app.models.schemas import ReportRequest, TTSRequest, WhatsAppRequest
from app.services.pdf_generator import pdf_generator
from app.services.tts_service import tts_service
from app.services.whatsapp_service import whatsapp_service
from app.services.data_loader import data_loader

router = APIRouter()

@router.post("/report/pdf")
async def generate_pdf_report(
    range: str = Query("30d", description="Rango: 30d, 90d, YTD, 12m")
) -> FileResponse:
    """Genera reporte ejecutivo en PDF"""
    if not data_loader.planta_data:
        raise HTTPException(
            status_code=400,
            detail="Datos no cargados. Usar POST /api/data/reload primero."
        )
    
    try:
        filepath = pdf_generator.generate_executive_report(range)
        return FileResponse(
            path=filepath,
            media_type='application/pdf',
            filename=filepath.split('/')[-1]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")

@router.post("/report/tts")
async def generate_tts_audio(request: TTSRequest = None) -> Dict[str, Any]:
    """Genera audio con resumen ejecutivo usando TTS"""
    if not data_loader.planta_data:
        raise HTTPException(
            status_code=400,
            detail="Datos no cargados. Usar POST /api/data/reload primero."
        )
    
    try:
        custom_text = request.text if request else None
        filepath = tts_service.generate_audio_summary(
            date_range="30d",
            custom_text=custom_text
        )
        
        return {
            "success": True,
            "audio_path": filepath,
            "filename": filepath.split('/')[-1],
            "message": "Audio generado exitosamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando audio: {str(e)}")

@router.post("/whatsapp/send-audio")
async def send_whatsapp_audio(request: WhatsAppRequest) -> Dict[str, Any]:
    """Envía audio por WhatsApp"""
    
    try:
        result = whatsapp_service.send_audio(
            to_phone=request.to_phone,
            audio_path=request.audio_path
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando WhatsApp: {str(e)}")

@router.post("/whatsapp/send-text")
async def send_whatsapp_text(
    to_phone: str = Query(..., description="Número en formato E.164 (ej: +5491112345678)"),
    message: str = Query(..., description="Mensaje de texto")
) -> Dict[str, Any]:
    """Envía mensaje de texto por WhatsApp"""
    
    try:
        result = whatsapp_service.send_text(
            to_phone=to_phone,
            message=message
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando WhatsApp: {str(e)}")
