"""
Vision API service - Handles Claude Vision API integration
"""

import logging
from typing import Optional, Dict, Any
import json
import base64
from anthropic import Anthropic
from ..utils.prompts import get_vision_prompt
from ..utils.validation import validate_confidence_score, validate_vision_output

logger = logging.getLogger(__name__)


class VisionService:
    """
    Handles image analysis using Claude Vision API
    
    Extracted data:
    - Trend direction (bullish/bearish/consolidating)
    - Swing highs and lows
    - Support zones (identified by multiple price touches)
    - Resistance zones (identified by multiple price touches)
    - Chart patterns (double top/bottom, channels, triangles, flags, H&S)
    - Returns structured JSON
    
    PRIVACY: Does NOT store uploaded images, only extracts and returns analysis data
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)

    async def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Send image to Claude Vision API and extract chart data.
        
        Returns:
            {
                "trend": "bullish|bearish|consolidating",
                "trend_confidence": 0-65,
                "support_zones": [...],
                "resistance_zones": [...],
                "patterns_detected": [...],
                "swing_highs": [...],
                "swing_lows": [...],
                "volatility_warning": null|string
            }
        
        Raises:
            ValueError: If image is invalid or API fails
        """
        try:
            # Convert image bytes to base64
            image_base64 = base64.standard_b64encode(image_bytes).decode('utf-8')
            
            # Get vision prompt
            vision_prompt = get_vision_prompt()
            
            # Call Claude Vision API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64,
                                },
                            },
                            {
                                "type": "text",
                                "text": vision_prompt
                            }
                        ],
                    }
                ],
            )
            
            # Extract JSON from response
            response_text = message.content[0].text
            
            # Try to parse JSON from response
            vision_data = self._parse_vision_response(response_text)
            
            # Validate extracted data
            is_valid, error_msg = validate_vision_output(vision_data)
            if not is_valid:
                logger.error(f"Vision validation failed: {error_msg}")
                raise ValueError(f"Invalid vision extraction: {error_msg}")
            
            # Cap confidence scores
            vision_data["trend_confidence"] = validate_confidence_score(
                vision_data.get("trend_confidence", 0)
            )
            
            # Cap confidence for zones
            for zone in vision_data.get("support_zones", []):
                if "confidence" in zone:
                    zone["confidence"] = validate_confidence_score(zone["confidence"])
            for zone in vision_data.get("resistance_zones", []):
                if "confidence" in zone:
                    zone["confidence"] = validate_confidence_score(zone["confidence"])
            
            logger.info(f"Vision analysis completed: trend={vision_data.get('trend')}")
            return vision_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse vision response JSON: {e}")
            raise ValueError(f"Invalid JSON in vision response: {str(e)}")
        except Exception as e:
            logger.error(f"Vision API error: {str(e)}")
            raise ValueError(f"Vision API call failed: {str(e)}")

    def _parse_vision_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Claude's JSON response into structured data.
        Handles cases where JSON is wrapped in markdown code blocks.
        """
        # Try to extract JSON if wrapped in markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        
        # Parse JSON
        return json.loads(response_text)

    async def validate_extraction(self, image_bytes: bytes, extracted_data: dict) -> bool:
        """
        Validate that extracted data doesn't have hallucinated prices.
        
        Checks if prices match visual chart data.
        For MVP, we perform basic structural validation.
        Future: Could use vision model to double-check prices.
        """
        try:
            # Validate structure
            is_valid, error_msg = validate_vision_output(extracted_data)
            if not is_valid:
                logger.warning(f"Extraction validation failed: {error_msg}")
                return False
            
            # Check for reasonable price ranges
            for zone in extracted_data.get("support_zones", []) + extracted_data.get("resistance_zones", []):
                price = zone.get("price_level", 0)
                # Basic sanity check: forex prices typically 0.5 - 150
                if price <= 0 or price > 200:
                    logger.warning(f"Unreasonable price detected: {price}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
