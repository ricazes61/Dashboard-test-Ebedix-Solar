from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path

from app.models.schemas import SettingsRequest, SettingsResponse
from app.services.data_loader import data_loader

router = APIRouter()

SETTINGS_FILE = Path("settings.json")

@router.get("/settings", response_model=SettingsResponse)
async def get_settings() -> SettingsResponse:
    """Obtiene configuración actual"""
    
    # Leer desde archivo si existe
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            return SettingsResponse(**data)
    
    # Default
    return SettingsResponse(
        data_folder="./data/input",
        last_reload=None,
        files_loaded={}
    )

@router.post("/settings", response_model=SettingsResponse)
async def update_settings(settings: SettingsRequest) -> SettingsResponse:
    """Actualiza configuración del folder de datos"""
    
    try:
        # Configurar folder
        data_loader.set_data_folder(settings.data_folder)
        
        # Guardar en archivo
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        response_data = {
            "data_folder": settings.data_folder,
            "last_reload": data_loader.last_reload.isoformat() if data_loader.last_reload else None,
            "files_loaded": data_loader.files_loaded
        }
        
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        return SettingsResponse(**response_data)
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
