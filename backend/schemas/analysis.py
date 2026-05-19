"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ImageUploadRequest(BaseModel):
    """Request schema for chart analysis"""
    # File is handled separately in route
    pair: Optional[str] = Field(None, description="Forex pair (e.g., EUR/USD)")
    timeframe: Optional[str] = Field(None, description="Chart timeframe (e.g., 4H, 1D)")


class SupportResistanceZone(BaseModel):
    """Support or resistance zone identified in the chart"""
    zone_type: str = Field(..., description="'support' or 'resistance'")
    price_level: float = Field(..., description="Price level of the zone")
    touch_count: int = Field(..., description="Number of times price touched this level")
    strength: str = Field(..., description="'weak', 'moderate', or 'strong'")


class TradeScenario(BaseModel):
    """Potential trade scenario based on chart analysis"""
    direction: str = Field(..., description="'bullish' or 'bearish'")
    entry_price: float = Field(..., description="Suggested entry price")
    stop_loss: float = Field(..., description="Suggested stop loss price")
    take_profit: float = Field(..., description="Suggested take profit price")
    risk_reward_ratio: float = Field(..., description="Risk to reward ratio")
    confidence_score: float = Field(..., le=65, description="Confidence (0-65%, capped)")


class VisionAnalysisResult(BaseModel):
    """Result from Claude Vision API analysis"""
    trend: str = Field(..., description="'bullish', 'bearish', or 'consolidating'")
    trend_confidence: float = Field(..., le=65)
    support_zones: List[SupportResistanceZone] = Field(default_factory=list)
    resistance_zones: List[SupportResistanceZone] = Field(default_factory=list)
    patterns_detected: List[str] = Field(default_factory=list)
    volatility_warning: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalysisResponse(BaseModel):
    """Final analysis response to client"""
    trend: str
    zones: List[dict]
    scenarios: List[TradeScenario]
    mentor_explanation: str
    confidence_score: float
    volatility_warning: Optional[str] = None
    analysis_id: str
    timestamp: datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None
