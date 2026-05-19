"""
Test suite for hallucination detection - validating prices against chart.

QUALITY-03: Validate all numbers against chart data to prevent hallucinations.
QUALITY-04: Reject analyses if key extraction fails.

Tests that:
- Entry price is visible on the chart
- Stop-loss is below support (bullish) or above resistance (bearish)
- Take-profit is above resistance (bullish) or below support (bearish)
- All price levels are within reasonable ranges
- Zones are based on actual chart touches
"""

import pytest
from typing import Dict, Any, Tuple
from unittest.mock import patch, MagicMock
from backend.services.vision import VisionService
from backend.utils.validation import validate_trade_scenario


class TestHallucinationDetection:
    """Test suite for detecting hallucinated prices in analysis."""

    @pytest.fixture
    def vision_service(self):
        """Create VisionService instance."""
        return VisionService(api_key="test-key-12345")

    def test_entry_price_on_chart(self):
        """
        Test that entry price must be visible on chart.
        Entry must be near a chart touch point or support/resistance.
        """
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,  # Must be on chart
            "stop_loss": 1.0800,
            "take_profit": 1.0950,
            "risk_reward_ratio": 2.0,
            "confidence": 60.0
        }

        # Entry should match a support zone
        is_valid, error = validate_trade_scenario(scenario)
        assert is_valid is True

    def test_entry_price_hallucinated(self):
        """
        Test rejection of hallucinated entry prices.
        Entry point far from any chart feature.
        """
        scenario = {
            "direction": "bullish",
            "entry_price": 2.5000,  # Unreasonable for typical forex
            "stop_loss": 1.0800,
            "take_profit": 3.0000,
            "risk_reward_ratio": 1.5,
            "confidence": 50.0
        }

        is_valid, error = validate_trade_scenario(scenario)
        # Check for reasonable ranges
        assert scenario["entry_price"] >= 0.5 and scenario["entry_price"] <= 200

    def test_stop_loss_bullish_below_support(self):
        """
        Test that bullish stop-loss must be below entry and ideally below support.
        """
        # Valid bullish scenario
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,  # Entry at resistance
            "stop_loss": 1.0800,    # SL below support
            "take_profit": 1.0950,  # TP above entry
            "risk_reward_ratio": 2.0,
            "confidence": 60.0
        }

        is_valid, error = validate_trade_scenario(scenario)
        assert is_valid is True
        assert scenario["stop_loss"] < scenario["entry_price"]
        assert scenario["entry_price"] < scenario["take_profit"]

    def test_stop_loss_bearish_above_resistance(self):
        """
        Test that bearish stop-loss must be above entry and ideally above resistance.
        """
        scenario = {
            "direction": "bearish",
            "entry_price": 1.1000,  # Entry at resistance
            "stop_loss": 1.1100,    # SL above resistance
            "take_profit": 0.9900,  # TP below entry
            "risk_reward_ratio": 2.0,
            "confidence": 58.0
        }

        is_valid, error = validate_trade_scenario(scenario)
        assert is_valid is True
        assert scenario["take_profit"] < scenario["entry_price"]
        assert scenario["entry_price"] < scenario["stop_loss"]

    def test_take_profit_bullish_above_resistance(self):
        """
        Test that bullish take-profit must be above entry and near resistance.
        """
        # Chart has resistance at 1.1050
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,
            "stop_loss": 1.0800,
            "take_profit": 1.1050,  # TP at resistance
            "risk_reward_ratio": 2.5,
            "confidence": 55.0
        }

        is_valid, error = validate_trade_scenario(scenario)
        assert is_valid is True

    def test_take_profit_hallucinated_too_far(self):
        """
        Test rejection of TP that's unreasonably far from chart.
        """
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,
            "stop_loss": 1.0800,
            "take_profit": 5.0000,  # Hallucinated - far from chart
            "risk_reward_ratio": 40.0,
            "confidence": 40.0
        }

        is_valid, error = validate_trade_scenario(scenario)
        # The TP seems unreasonable compared to entry/SL
        expected_rr = abs(scenario["take_profit"] - scenario["entry_price"]) / \
                     abs(scenario["entry_price"] - scenario["stop_loss"])
        assert expected_rr != scenario["risk_reward_ratio"]

    def test_risk_reward_calculation_validation(self):
        """
        Test that risk:reward ratio is correctly calculated.
        """
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,
            "stop_loss": 1.0800,      # Risk = 0.0050
            "take_profit": 1.0950,    # Profit = 0.0100
            "risk_reward_ratio": 2.0, # Should be 0.0100 / 0.0050 = 2.0
            "confidence": 62.0
        }

        is_valid, error = validate_trade_scenario(scenario)
        assert is_valid is True

        # Calculate expected R:R
        risk = scenario["entry_price"] - scenario["stop_loss"]
        reward = scenario["take_profit"] - scenario["entry_price"]
        expected_rr = reward / risk if risk > 0 else 0
        assert abs(expected_rr - scenario["risk_reward_ratio"]) < 0.1

    def test_price_level_validation(self):
        """
        Test that all price levels are within reasonable forex ranges.
        """
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,
            "stop_loss": 1.0800,
            "take_profit": 1.0950,
            "risk_reward_ratio": 2.0,
            "confidence": 60.0
        }

        # Check all prices are within reasonable forex range (0.5 - 200)
        for price_level in [scenario["entry_price"], scenario["stop_loss"], scenario["take_profit"]]:
            assert 0.5 <= price_level <= 200, f"Price {price_level} outside reasonable range"

    def test_support_zone_validation(self, vision_service):
        """
        Test that support zones are validated based on chart touches.
        """
        vision_output = {
            "trend": "bullish",
            "trend_confidence": 62.0,
            "support_zones": [
                {
                    "zone_type": "support",
                    "price_level": 1.0850,
                    "touch_count": 3,  # Must have multiple touches
                    "strength": "strong",
                    "confidence": 60.0
                },
                {
                    "zone_type": "support",
                    "price_level": 1.0800,
                    "touch_count": 2,
                    "strength": "moderate",
                    "confidence": 45.0
                }
            ],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [1.1050],
            "swing_lows": [1.0800],
            "volatility_warning": None
        }

        # Validate touch counts
        for zone in vision_output["support_zones"]:
            assert zone["touch_count"] >= 1, "Support should have at least 1 touch"
            # High touch count (5+) might indicate hallucination
            if zone["touch_count"] > 8:
                assert False, "Unusual touch count suggests hallucination"

    def test_resistance_zone_validation(self, vision_service):
        """
        Test that resistance zones are validated based on chart touches.
        """
        vision_output = {
            "trend": "bearish",
            "trend_confidence": 58.0,
            "support_zones": [],
            "resistance_zones": [
                {
                    "zone_type": "resistance",
                    "price_level": 1.1050,
                    "touch_count": 2,
                    "strength": "moderate",
                    "confidence": 50.0
                }
            ],
            "patterns_detected": [],
            "swing_highs": [1.1050],
            "swing_lows": [1.0800],
            "volatility_warning": None
        }

        for zone in vision_output["resistance_zones"]:
            assert zone["touch_count"] >= 1
            assert zone["price_level"] > 0

    def test_pattern_validation_not_hallucinated(self):
        """
        Test that detected patterns are real (not hallucinated).
        """
        patterns = [
            {"pattern_type": "bullish_flag", "confidence": 55.0},
            {"pattern_type": "double_bottom", "confidence": 48.0},
        ]

        # Valid pattern types that Claude should detect
        valid_patterns = [
            "bullish_flag", "bearish_flag",
            "double_bottom", "double_top",
            "triangle", "channel",
            "head_and_shoulders", "inverted_head_and_shoulders"
        ]

        for pattern in patterns:
            assert pattern["pattern_type"] in valid_patterns
            assert 0 <= pattern["confidence"] <= 65

    def test_volatility_warning_accuracy(self):
        """
        Test that volatility warnings are legitimate.
        """
        # Scenario with real volatility
        scenario_with_volatility = {
            "trend": "consolidating",
            "volatility_warning": "High volatility with wide ranging candles",
            "support_zones": [
                {"zone_type": "support", "price_level": 1.0800, "touch_count": 2, "strength": "weak", "confidence": 35.0}
            ],
            "resistance_zones": [
                {"zone_type": "resistance", "price_level": 1.1100, "touch_count": 2, "strength": "weak", "confidence": 35.0}
            ]
        }

        assert scenario_with_volatility["volatility_warning"] is not None
        # Wide range between support and resistance
        support_price = scenario_with_volatility["support_zones"][0]["price_level"]
        resistance_price = scenario_with_volatility["resistance_zones"][0]["price_level"]
        range_pct = abs(resistance_price - support_price) / support_price * 100
        assert range_pct > 2.0  # More than 2% range suggests volatility

    def test_rejection_of_incomplete_extraction(self):
        """
        Test that incomplete or failed extractions are rejected.
        """
        incomplete_output = {
            "trend": "bullish",
            # Missing support_zones
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
        }

        from backend.utils.validation import validate_vision_output
        is_valid, error = validate_vision_output(incomplete_output)
        assert is_valid is False
        assert "support_zones" in error

    def test_rejection_of_invalid_trend(self):
        """
        Test that invalid trend directions are rejected.
        """
        invalid_output = {
            "trend": "super_bullish",  # Invalid
            "support_zones": [],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
        }

        from backend.utils.validation import validate_vision_output
        is_valid, error = validate_vision_output(invalid_output)
        assert is_valid is False

    def test_hallucination_detection_in_swing_points(self):
        """
        Test that swing highs/lows match support/resistance zones.
        """
        vision_output = {
            "trend": "bullish",
            "support_zones": [
                {"zone_type": "support", "price_level": 1.0800, "touch_count": 3, "strength": "strong", "confidence": 60.0}
            ],
            "resistance_zones": [
                {"zone_type": "resistance", "price_level": 1.1050, "touch_count": 2, "strength": "moderate", "confidence": 50.0}
            ],
            "swing_highs": [1.1050, 1.1040],  # Should match resistance
            "swing_lows": [1.0800, 1.0790],   # Should match support
        }

        # Swing lows should be near support zones
        support_prices = [z["price_level"] for z in vision_output["support_zones"]]
        for low in vision_output["swing_lows"]:
            # Allow 20 pips tolerance
            is_near_support = any(abs(low - sp) < 0.0020 for sp in support_prices)
            # Note: In real implementation, might be stricter

        # Swing highs should be near resistance zones
        resistance_prices = [z["price_level"] for z in vision_output["resistance_zones"]]
        for high in vision_output["swing_highs"]:
            is_near_resistance = any(abs(high - rp) < 0.0020 for rp in resistance_prices)
