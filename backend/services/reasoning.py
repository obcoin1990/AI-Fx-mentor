"""
Reasoning service - Generates trade scenarios from Vision analysis
"""

import logging
import json
from typing import List, Dict, Optional, Any
from anthropic import Anthropic
from ..utils.prompts import get_reasoning_prompt
from ..utils.validation import validate_confidence_score, validate_mentor_explanation, validate_trade_scenario

logger = logging.getLogger(__name__)


class ReasoningService:
    """
    Generates trading scenarios from Vision API output.
    
    Takes structured JSON from vision service and:
    - Generates 1-2 trade scenarios (direction, entry, SL, TP)
    - Calculates risk-reward ratios
    - Assigns confidence scores (0-65% capped)
    - Creates mentor-style explanations (3-5 sentences)
    
    QUALITY: Confidence capped at 65% to prevent false confidence
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)

    async def generate_scenarios(self, vision_data: dict) -> Dict[str, Any]:
        """
        Generate trade scenarios from vision analysis.
        
        Input: Vision service output (trend, zones, patterns, etc.)
        
        Returns:
            {
                "scenarios": [
                    {
                        "direction": "bullish|bearish",
                        "entry_price": float,
                        "stop_loss": float,
                        "take_profit": float,
                        "risk_reward_ratio": float,
                        "confidence_score": float (0-65)
                    },
                    ...
                ],
                "mentor_explanation": "3-5 sentence explanation",
                "overall_confidence": float (0-65)
            }
        
        Raises:
            ValueError: If reasoning fails or validation fails
        """
        try:
            # Get reasoning prompt with vision data
            vision_json = json.dumps(vision_data, indent=2)
            reasoning_prompt = get_reasoning_prompt(vision_json)
            
            # Call Claude Reasoning API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": reasoning_prompt
                    }
                ],
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse JSON
            reasoning_data = self._parse_reasoning_response(response_text)
            
            # Validate and process scenarios
            scenarios = reasoning_data.get("scenarios", [])
            if not scenarios:
                raise ValueError("No scenarios generated")
            
            # Process each scenario
            processed_scenarios = []
            for scenario in scenarios[:2]:  # Limit to 2 scenarios
                # Validate scenario
                is_valid, error_msg = validate_trade_scenario(scenario)
                if not is_valid:
                    logger.warning(f"Invalid scenario: {error_msg}")
                    continue
                
                # Cap confidence
                scenario["confidence_score"] = validate_confidence_score(
                    scenario.get("confidence_score", 0)
                )
                
                # Calculate R:R if not present
                if "risk_reward_ratio" not in scenario or scenario["risk_reward_ratio"] == 0:
                    scenario["risk_reward_ratio"] = self.calculate_risk_reward(
                        scenario.get("entry_price", 0),
                        scenario.get("stop_loss", 0),
                        scenario.get("take_profit", 0)
                    )
                
                processed_scenarios.append(scenario)
            
            if not processed_scenarios:
                raise ValueError("All scenarios failed validation")
            
            # Validate and process explanation
            explanation = reasoning_data.get("mentor_explanation", "")
            is_valid, error_msg = validate_mentor_explanation(explanation)
            if not is_valid:
                logger.warning(f"Mentor explanation validation: {error_msg}")
                # Continue anyway, but log warning
            
            # Calculate overall confidence
            confidences = [s.get("confidence_score", 0) for s in processed_scenarios]
            overall_confidence = validate_confidence_score(sum(confidences) / len(confidences))
            
            logger.info(f"Reasoning completed: {len(processed_scenarios)} scenarios generated")
            
            return {
                "scenarios": processed_scenarios,
                "mentor_explanation": explanation,
                "overall_confidence": overall_confidence
            }
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse reasoning response JSON: {e}")
            raise ValueError(f"Invalid JSON in reasoning response: {str(e)}")
        except Exception as e:
            logger.error(f"Reasoning API error: {str(e)}")
            raise ValueError(f"Reasoning API call failed: {str(e)}")

    def _parse_reasoning_response(self, response_text: str) -> Dict[str, Any]:
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

    def calculate_risk_reward(self, entry: float, sl: float, tp: float) -> float:
        """Calculate risk-reward ratio from entry, stop-loss, and take-profit."""
        try:
            risk = abs(entry - sl)
            reward = abs(tp - entry)
            if risk == 0:
                return 0.0
            return round(reward / risk, 2)
        except Exception as e:
            logger.error(f"Error calculating R:R: {e}")
            return 0.0

    def cap_confidence(self, confidence: float, max_confidence: float = 65.0) -> float:
        """Ensure confidence never exceeds maximum (prevents false confidence)."""
        return min(float(confidence), max_confidence)

    async def validate_scenario(self, scenario: dict, direction: str) -> bool:
        """
        Validate that a scenario makes logical sense.
        
        For bullish: entry > SL and entry < TP
        For bearish: entry < SL and entry > TP
        """
        entry = scenario.get("entry_price")
        sl = scenario.get("stop_loss")
        tp = scenario.get("take_profit")
        
        if not all([entry, sl, tp]):
            return False
        
        if direction == "bullish":
            return entry > sl and entry < tp
        elif direction == "bearish":
            return entry < sl and entry > tp
        
        return False
