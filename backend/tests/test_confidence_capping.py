"""
Test suite for confidence score capping.

REASON-03: Assign confidence score (0-100%, capped at 65%)
REASON-05: Flag confidence <50% as unreliable

Tests that:
- All confidence scores are capped at 65% maximum
- Low confidence (<50%) analyses are flagged as unreliable
- Confidence calculation is consistent across all elements
- Low confidence is visually distinct from normal confidence
"""

import pytest
from typing import Dict, Any
from backend.utils.validation import validate_confidence_score, is_low_confidence


class TestConfidenceCapping:
    """Test suite for confidence score validation and capping."""

    def test_cap_high_confidence_trend(self):
        """
        Test that trend confidence above 65% is capped at 65%.
        """
        raw_confidence = 95.0
        capped = validate_confidence_score(raw_confidence)
        
        assert capped == 65.0, f"Expected 65.0, got {capped}"
        assert capped <= 65.0

    def test_cap_extreme_confidence(self):
        """
        Test that extreme confidence (100%) is capped at 65%.
        """
        raw_confidence = 100.0
        capped = validate_confidence_score(raw_confidence)
        
        assert capped == 65.0
        assert capped <= 65.0

    def test_preserve_normal_confidence(self):
        """
        Test that normal confidence (below 65%) is preserved.
        """
        normal_scores = [45.0, 55.0, 60.0, 64.9]
        
        for score in normal_scores:
            capped = validate_confidence_score(score)
            assert capped == score, f"Score {score} was modified"

    def test_zero_confidence(self):
        """
        Test that zero confidence is handled correctly.
        """
        capped = validate_confidence_score(0.0)
        assert capped == 0.0

    def test_clamp_negative_confidence(self):
        """
        Test that negative confidence is clamped to 0.
        """
        capped = validate_confidence_score(-10.0)
        assert capped == 0.0

    def test_clamp_over_100_confidence(self):
        """
        Test that confidence > 100% is clamped to 100 then capped at 65.
        """
        capped = validate_confidence_score(150.0)
        assert capped == 65.0

    def test_confidence_float_conversion(self):
        """
        Test that confidence scores are converted to float properly.
        """
        capped = validate_confidence_score("65.5")
        assert isinstance(capped, float)
        assert capped == 65.0  # Capped to 65

    def test_confidence_rounding(self):
        """
        Test that confidence is rounded to 1 decimal place.
        """
        capped = validate_confidence_score(62.556)
        assert capped == 62.6

    def test_low_confidence_threshold(self):
        """
        Test that low confidence (<50%) is correctly identified.
        """
        scores_low = [0.0, 25.0, 49.9]
        scores_normal = [50.0, 55.0, 65.0]
        
        for score in scores_low:
            assert is_low_confidence(score) is True
        
        for score in scores_normal:
            assert is_low_confidence(score) is False

    def test_low_confidence_boundary(self):
        """
        Test low confidence at exactly 50%.
        """
        # Exactly 50% should NOT be flagged as unreliable
        assert is_low_confidence(50.0) is False
        assert is_low_confidence(49.9) is True

    def test_low_confidence_string_conversion(self):
        """
        Test low confidence check with string input.
        """
        assert is_low_confidence("45.0") is True
        assert is_low_confidence("55.0") is False

    def test_vision_output_confidence_capping(self):
        """
        Test that vision output has all confidence scores capped.
        """
        vision_output = {
            "trend": "bullish",
            "trend_confidence": 95.0,  # Should be capped
            "support_zones": [
                {
                    "zone_type": "support",
                    "price_level": 1.0850,
                    "touch_count": 3,
                    "strength": "strong",
                    "confidence": 85.0  # Should be capped
                }
            ],
            "resistance_zones": [
                {
                    "zone_type": "resistance",
                    "price_level": 1.1050,
                    "touch_count": 2,
                    "strength": "moderate",
                    "confidence": 72.0  # Should be capped
                }
            ],
            "patterns_detected": [
                {"pattern_type": "bullish_flag", "confidence": 78.0}  # Should be capped
            ],
            "swing_highs": [],
            "swing_lows": [],
            "volatility_warning": None
        }

        # Cap all confidence scores
        vision_output["trend_confidence"] = validate_confidence_score(vision_output["trend_confidence"])
        for zone in vision_output["support_zones"] + vision_output["resistance_zones"]:
            zone["confidence"] = validate_confidence_score(zone["confidence"])
        for pattern in vision_output["patterns_detected"]:
            pattern["confidence"] = validate_confidence_score(pattern["confidence"])

        # Verify all are capped
        assert vision_output["trend_confidence"] <= 65.0
        for zone in vision_output["support_zones"] + vision_output["resistance_zones"]:
            assert zone["confidence"] <= 65.0
        for pattern in vision_output["patterns_detected"]:
            assert pattern["confidence"] <= 65.0

    def test_trade_scenario_confidence_capping(self):
        """
        Test that trade scenario confidence is capped.
        """
        scenario = {
            "direction": "bullish",
            "entry_price": 1.0850,
            "stop_loss": 1.0800,
            "take_profit": 1.0950,
            "risk_reward_ratio": 2.0,
            "confidence": 88.0  # Should be capped
        }

        scenario["confidence"] = validate_confidence_score(scenario["confidence"])
        assert scenario["confidence"] == 65.0

    def test_mentor_explanation_confidence_capping(self):
        """
        Test that mentor explanation confidence is capped.
        """
        explanation_confidence = 92.0
        capped = validate_confidence_score(explanation_confidence)
        assert capped == 65.0

    def test_display_logic_for_low_confidence(self):
        """
        Test that low confidence should be displayed differently in UI.
        """
        score = 45.0
        is_unreliable = is_low_confidence(score)
        
        if is_unreliable:
            # UI should show "Low confidence - unreliable" or red color
            assert True
        else:
            assert False, "45% should be flagged as low confidence"

    def test_display_logic_for_normal_confidence(self):
        """
        Test that normal confidence displays normally in UI.
        """
        score = 62.0
        is_unreliable = is_low_confidence(score)
        
        if not is_unreliable:
            # UI should show normally with color gradient
            assert True
        else:
            assert False, "62% should not be flagged as low confidence"

    def test_confidence_color_mapping(self):
        """
        Test mapping of confidence scores to UI colors.
        """
        # Define confidence color mapping
        def get_confidence_color(score: float) -> str:
            if is_low_confidence(score):
                return "red"  # Low confidence warning
            elif score < 55:
                return "yellow"  # Cautious
            else:
                return "green"  # Normal confidence
        
        assert get_confidence_color(35.0) == "red"
        assert get_confidence_color(52.0) == "yellow"
        assert get_confidence_color(62.0) == "green"

    def test_multiple_zones_confidence_capping(self):
        """
        Test that multiple zones all have confidence capped.
        """
        zones = [
            {"confidence": 100.0},
            {"confidence": 85.0},
            {"confidence": 65.0},
            {"confidence": 50.0},
            {"confidence": 25.0},
        ]

        for zone in zones:
            zone["confidence"] = validate_confidence_score(zone["confidence"])

        expected = [65.0, 65.0, 65.0, 50.0, 25.0]
        actual = [z["confidence"] for z in zones]
        assert actual == expected

    def test_confidence_comparison_after_capping(self):
        """
        Test that confidence scores can still be compared after capping.
        """
        high_score = validate_confidence_score(85.0)
        medium_score = validate_confidence_score(60.0)
        low_score = validate_confidence_score(40.0)

        # All should be capped, so high_score will be 65
        assert high_score == 65.0
        assert medium_score == 60.0
        assert low_score == 40.0

        # Original relative order: high > medium > low
        # After capping: 65 > 60 > 40 (still maintains order)

    def test_percentile_calculation_with_capping(self):
        """
        Test that percentile representation makes sense with capping.
        """
        # A 65% capped score should show as 65% confidence, not 100%
        capped_score = validate_confidence_score(95.0)
        assert capped_score == 65.0
        
        # Display as "65% confidence" not "95% confidence"
        display_text = f"{capped_score:.0f}% confidence"
        assert display_text == "65% confidence"

    def test_edge_cases_confidence(self):
        """
        Test edge cases for confidence scoring.
        """
        edge_cases = [
            (0.0, 0.0),
            (0.1, 0.1),
            (1.0, 1.0),
            (50.0, 50.0),
            (64.9, 64.9),
            (65.0, 65.0),
            (65.1, 65.0),
            (100.0, 65.0),
            (1000.0, 65.0),
        ]

        for input_score, expected_output in edge_cases:
            capped = validate_confidence_score(input_score)
            assert capped == expected_output, f"Input {input_score} expected {expected_output}, got {capped}"

    def test_confidence_persistence_across_requests(self):
        """
        Test that confidence capping is applied consistently across requests.
        """
        # Simulate multiple requests
        for i in range(5):
            score = validate_confidence_score(90.0)
            assert score == 65.0, f"Request {i+1}: confidence not capped correctly"
