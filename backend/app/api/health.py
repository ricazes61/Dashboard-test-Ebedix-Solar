from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Solar PV Analytics API",
        "version": "1.0.0"
    }
