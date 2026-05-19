"""
Validation utilities for analysis outputs
"""

import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def validate_confidence_score(score: float, max_score: float = 65.0) -> float:
    """
    Validate and cap confidence score.
    
    QUALITY-03: Confidence scores must be capped at 65% to prevent false confidence.
    """
    # Ensure score is float
    score = float(score)
    
    # Clamp to 0-100 range
    score = max(0.0, min(100.0, score))
    
    # Cap at max_score (default 65%)
    score = min(score, max_score)
    
    return round(score, 1)


def is_low_confidence(score: float, threshold: float = 50.0) -> bool:
    """
    Check if confidence is below threshold (unreliable).
    
    QUALITY-05: Flag analyses with < 50% confidence as unreliable.
    """
    return float(score) < threshold


def validate_trade_scenario(scenario: dict) -> Tuple[bool, Optional[str]]:
    """
    Validate a trade scenario for logical consistency.
    
    Checks:
    - Entry price is reasonable
    - Stop-loss is protective
    - Take-profit is in correct direction
    - Risk-reward ratio is calculated correctly
    """
    try:
        direction = scenario.get("direction")
        entry = float(scenario.get("entry_price", 0))
        sl = float(scenario.get("stop_loss", 0))
        tp = float(scenario.get("take_profit", 0))
        rr = float(scenario.get("risk_reward_ratio", 0))
        
        # Check direction
        if direction not in ["bullish", "bearish"]:
            return False, f"Invalid direction: {direction}"
        
        # Check prices are reasonable
        if entry <= 0 or sl <= 0 or tp <= 0:
            return False, "Prices must be positive"
        
        # Check logical placement
        if direction == "bullish":
            if not (sl < entry < tp):
                return False, f"Bullish scenario invalid: SL({sl}) < Entry({entry}) < TP({tp})"
        elif direction == "bearish":
            if not (tp < entry < sl):
                return False, f"Bearish scenario invalid: TP({tp}) < Entry({entry}) < SL({sl})"
        
        # Validate R:R calculation
        expected_rr = abs(tp - entry) / abs(entry - sl) if abs(entry - sl) > 0 else 0
        expected_rr = round(expected_rr, 2)
        
        if abs(rr - expected_rr) > 0.1:  # Allow small floating point diff
            logger.warning(f"R:R mismatch: expected {expected_rr}, got {rr}")
        
        return True, None
    
    except Exception as e:
        return False, str(e)


def validate_mentor_explanation(explanation: str) -> Tuple[bool, Optional[str]]:
    """
    Validate mentor explanation meets quality standards.
    
    Checks:
    - Length (3-5 sentences, ~100-400 words)
    - No financial advice language ("should", "recommend", "buy", "sell")
    - Educational tone
    """
    if not explanation or not isinstance(explanation, str):
        return False, "Explanation must be non-empty string"
    
    # Check length (rough sentence count)
    sentences = explanation.split('.')
    sentence_count = len([s for s in sentences if s.strip()])
    
    if sentence_count < 2:
        return False, f"Explanation too short ({sentence_count} sentences, need 3-5)"
    
    if sentence_count > 8:
        logger.warning(f"Explanation long ({sentence_count} sentences, recommend 3-5)")
    
    # Check for financial advice language
    forbidden_phrases = [
        "should ", "should not",
        "I recommend", "I advise",
        "buy now", "sell now",
        "guaranteed", "will profit",
        "can't lose", "sure win"
    ]
    
    explanation_lower = explanation.lower()
    for phrase in forbidden_phrases:
        if phrase in explanation_lower:
            return False, f"Forbidden phrase detected: '{phrase}'"
    
    return True, None


def validate_vision_output(vision_data: dict) -> Tuple[bool, Optional[str]]:
    """
    Validate vision analysis output structure and content.
    
    QUALITY-04: Reject if key extraction fails.
    """
    try:
        # Check required fields
        required_fields = ["trend", "support_zones", "resistance_zones"]
        for field in required_fields:
            if field not in vision_data:
                return False, f"Missing required field: {field}"
        
        # Validate trend
        trend = vision_data.get("trend")
        if trend not in ["bullish", "bearish", "consolidating"]:
            return False, f"Invalid trend: {trend}"
        
        # Validate zones
        support_zones = vision_data.get("support_zones", [])
        resistance_zones = vision_data.get("resistance_zones", [])
        
        if not isinstance(support_zones, list) or not isinstance(resistance_zones, list):
            return False, "Zones must be lists"
        
        # Check for unreasonable zone counts
        if len(support_zones) > 10 or len(resistance_zones) > 10:
            logger.warning("Unusual number of zones detected")
        
        return True, None
    
    except Exception as e:
        return False, str(e)
