"""
Reasoning endpoint - POST /api/reason
Accepts vision analysis JSON and returns trade scenarios
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from ..services.reasoning import ReasoningService
from ..utils.validation import validate_confidence_score

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["reasoning"])

# Initialize services
reasoning_service = None


class ReasoningRequest(BaseModel):
    """Request to generate trade scenarios from vision analysis"""
    vision_data: Dict[str, Any]
    pair: Optional[str] = None
    timeframe: Optional[str] = None


class TradeScenario(BaseModel):
    """A single trade scenario"""
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    confidence_score: float


class ReasoningResponse(BaseModel):
    """Response with scenarios and explanation"""
    success: bool
    scenarios: List[TradeScenario]
    mentor_explanation: str
    overall_confidence: float
    pair: Optional[str] = None
    timeframe: Optional[str] = None
    analysis_id: str
    timestamp: str


def get_reasoning_service() -> ReasoningService:
    """Get or create reasoning service instance"""
    global reasoning_service
    if reasoning_service is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        reasoning_service = ReasoningService(api_key)
    return reasoning_service


@router.post("/reason", response_model=dict)
async def generate_scenarios(request: ReasoningRequest):
    """
    POST /api/reason
    
    Accepts vision analysis JSON and generates trade scenarios.
    
    Request:
    {
        "vision_data": { ... vision output ... },
        "pair": "EUR/USD",
        "timeframe": "4H"
    }
    
    Returns:
    {
        "success": true,
        "scenarios": [
            {
                "direction": "bullish",
                "entry_price": 1.0850,
                "stop_loss": 1.0800,
                "take_profit": 1.0950,
                "risk_reward_ratio": 2.0,
                "confidence_score": 55.0
            },
            ...
        ],
        "mentor_explanation": "Based on the chart analysis...",
        "overall_confidence": 55.0,
        "pair": "EUR/USD",
        "timeframe": "4H",
        "analysis_id": "uuid",
        "timestamp": "ISO8601"
    }
    
    Error cases:
    - 400: Invalid vision data or reasoning fails
    - 503: Claude API timeout or error
    - 500: Internal error
    """
    analysis_id = str(uuid.uuid4())
    
    try:
        # Validate vision_data
        if not request.vision_data:
            raise HTTPException(status_code=400, detail="Vision data is required")
        
        # Get reasoning service
        reasoning_svc = get_reasoning_service()
        
        # Generate scenarios
        try:
            reasoning_data = await reasoning_svc.generate_scenarios(request.vision_data)
        except ValueError as e:
            logger.error(f"Reasoning failed: {e}")
            raise HTTPException(status_code=400, detail=f"Could not generate scenarios: {str(e)}")
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Reasoning service temporarily unavailable. Please try again."
            )
        
        # Format response
        scenarios = []
        for scenario in reasoning_data.get("scenarios", []):
            scenarios.append({
                "direction": scenario.get("direction"),
                "entry_price": float(scenario.get("entry_price", 0)),
                "stop_loss": float(scenario.get("stop_loss", 0)),
                "take_profit": float(scenario.get("take_profit", 0)),
                "risk_reward_ratio": float(scenario.get("risk_reward_ratio", 0)),
                "confidence_score": float(scenario.get("confidence_score", 0))
            })
        
        return {
            "success": True,
            "scenarios": scenarios,
            "mentor_explanation": reasoning_data.get("mentor_explanation", ""),
            "overall_confidence": float(reasoning_data.get("overall_confidence", 0)),
            "pair": request.pair,
            "timeframe": request.timeframe,
            "analysis_id": analysis_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in reason endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
