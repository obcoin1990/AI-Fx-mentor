"""
Analysis endpoint - POST /api/analyze-chart
Handles chart image upload, vision analysis, and returns structured JSON
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import logging
import os
import json
from datetime import datetime
import uuid

from ..services.vision import VisionService
from ..services.image_processor import ImageProcessor
from ..schemas.analysis import VisionAnalysisResult, ErrorResponse
from ..utils.validation import validate_vision_output

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analysis"])

# Initialize services
vision_service = None


def get_vision_service() -> VisionService:
    """Get or create vision service instance"""
    global vision_service
    if vision_service is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        vision_service = VisionService(api_key)
    return vision_service


@router.post("/analyze-chart", response_model=dict)
async def analyze_chart(
    file: UploadFile = File(...),
    pair: str = Form(default="UNKNOWN"),
    timeframe: str = Form(default="UNKNOWN"),
):
    """
    POST /api/analyze-chart
    
    Accepts multipart/form-data with:
    - file: Chart image (PNG/JPG)
    - pair: Forex pair (e.g., EUR/USD) - optional
    - timeframe: Chart timeframe (e.g., 4H, 1D) - optional
    
    Returns:
    {
        "success": true,
        "trend": "bullish|bearish|consolidating",
        "trend_confidence": 0-65,
        "support_zones": [...],
        "resistance_zones": [...],
        "patterns_detected": [...],
        "volatility_warning": null|string,
        "analysis_id": "uuid",
        "timestamp": "ISO8601",
        "pair": "EUR/USD",
        "timeframe": "4H"
    }
    
    Error cases:
    - 400: Invalid image format/size
    - 503: Claude API timeout or error
    - 500: Internal error
    """
    analysis_id = str(uuid.uuid4())
    
    try:
        # Read file contents
        image_bytes = await file.read()
        
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Image file is empty")
        
        # Validate image
        is_valid, error_msg = ImageProcessor.validate_image(image_bytes)
        if not is_valid:
            logger.warning(f"Image validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Get vision service
        vision_svc = get_vision_service()
        
        # Call vision API
        try:
            vision_data = await vision_svc.analyze_image(image_bytes)
        except ValueError as e:
            logger.error(f"Vision analysis failed: {e}")
            raise HTTPException(status_code=400, detail=f"Could not analyze chart: {str(e)}")
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Analysis service temporarily unavailable. Please try again."
            )
        
        # Validate vision output
        is_valid, error_msg = validate_vision_output(vision_data)
        if not is_valid:
            logger.error(f"Vision output validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=f"Invalid chart analysis: {error_msg}")
        
        # Validate extraction (ensure no hallucinations)
        is_valid = await vision_svc.validate_extraction(image_bytes, vision_data)
        if not is_valid:
            logger.warning(f"Extraction validation failed for analysis {analysis_id}")
            # Don't fail here - log warning but return result
        
        # Log analysis to database (audit trail)
        # TODO: Database logging will be implemented in Plan 06
        
        # Return response
        return {
            "success": True,
            "trend": vision_data.get("trend"),
            "trend_confidence": vision_data.get("trend_confidence", 0),
            "support_zones": vision_data.get("support_zones", []),
            "resistance_zones": vision_data.get("resistance_zones", []),
            "patterns_detected": vision_data.get("patterns_detected", []),
            "swing_highs": vision_data.get("swing_highs", []),
            "swing_lows": vision_data.get("swing_lows", []),
            "volatility_warning": vision_data.get("volatility_warning"),
            "analysis_id": analysis_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pair": pair if pair != "UNKNOWN" else None,
            "timeframe": timeframe if timeframe != "UNKNOWN" else None,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
