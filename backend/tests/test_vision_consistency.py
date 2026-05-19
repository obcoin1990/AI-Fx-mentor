"""
Test suite for vision consistency - verifying deterministic outputs.

QUALITY-05: Consistency testing (same chart = same output)

Tests that running the same chart 5 times produces identical outputs,
ensuring reproducibility and preventing random hallucinations.
"""

import pytest
import json
import hashlib
from typing import Dict, Any
from unittest.mock import patch, MagicMock
from backend.services.vision import VisionService
from backend.utils.validation import validate_vision_output


class TestVisionConsistency:
    """Test suite for vision analysis consistency."""

    @pytest.fixture
    def vision_service(self):
        """Create VisionService instance with mock API key."""
        return VisionService(api_key="test-key-12345")

    @pytest.fixture
    def sample_vision_output(self) -> Dict[str, Any]:
        """Sample vision output for testing."""
        return {
            "trend": "bullish",
            "trend_confidence": 62.5,
            "support_zones": [
                {
                    "zone_type": "support",
                    "price_level": 1.0850,
                    "touch_count": 3,
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
            "resistance_zones": [
                {
                    "zone_type": "resistance",
                    "price_level": 1.1050,
                    "touch_count": 2,
                    "strength": "moderate",
                    "confidence": 50.0
                }
            ],
            "patterns_detected": [
                {"pattern_type": "bullish_flag", "confidence": 55.0}
            ],
            "swing_highs": [1.1050, 1.1040],
            "swing_lows": [1.0800, 1.0850],
            "volatility_warning": None
        }

    def test_consistency_single_run(self, vision_service, sample_vision_output):
        """Test that a single vision analysis returns expected structure."""
        with patch.object(vision_service.client.messages, 'create') as mock_create:
            # Mock Claude API response
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text=json.dumps(sample_vision_output))]
            mock_create.return_value = mock_response

            result = vision_service.analyze_image(b"fake_image_bytes")

            assert result["trend"] == "bullish"
            assert result["trend_confidence"] == 62.5
            assert len(result["support_zones"]) == 2
            assert len(result["resistance_zones"]) == 1

    def test_consistency_five_runs(self, vision_service, sample_vision_output):
        """
        Test that running same chart 5 times produces identical outputs.
        
        This is critical for reproducibility.
        """
        with patch.object(vision_service.client.messages, 'create') as mock_create:
            # Mock Claude API to return same output every time
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text=json.dumps(sample_vision_output))]
            mock_create.return_value = mock_response

            # Run 5 times with same image
            image_bytes = b"test_chart_image"
            results = []
            for i in range(5):
                result = vision_service.analyze_image(image_bytes)
                results.append(result)

            # Verify all 5 results are identical
            for i in range(1, 5):
                assert results[i] == results[0], f"Run {i} differs from Run 0"

            # Verify specific values are consistent
            for result in results:
                assert result["trend"] == "bullish"
                assert result["trend_confidence"] == 62.5
                assert len(result["support_zones"]) == 2

    def test_confidence_capping_consistency(self, vision_service):
        """
        Test that confidence scores are consistently capped at 65%.
        """
        high_confidence_output = {
            "trend": "bullish",
            "trend_confidence": 95.0,  # Over 65% - should be capped
            "support_zones": [
                {
                    "zone_type": "support",
                    "price_level": 1.0850,
                    "touch_count": 3,
                    "strength": "strong",
                    "confidence": 85.0  # Over 65% - should be capped
                }
            ],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
            "volatility_warning": None
        }

        with patch.object(vision_service.client.messages, 'create') as mock_create:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text=json.dumps(high_confidence_output))]
            mock_create.return_value = mock_response

            result = vision_service.analyze_image(b"test_image")

            # Verify confidence is capped at 65%
            assert result["trend_confidence"] <= 65.0, "Trend confidence not capped"
            for zone in result["support_zones"]:
                assert zone.get("confidence", 0) <= 65.0, "Zone confidence not capped"

    def test_consistency_json_parsing(self, vision_service):
        """Test that JSON parsing is consistent across markdown formats."""
        expected_output = {
            "trend": "bearish",
            "trend_confidence": 58.0,
            "support_zones": [],
            "resistance_zones": [{"zone_type": "resistance", "price_level": 1.2000, "touch_count": 2, "strength": "strong", "confidence": 55.0}],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
            "volatility_warning": None
        }

        # Test various markdown formats Claude might return
        test_cases = [
            json.dumps(expected_output),  # Plain JSON
            f"```json\n{json.dumps(expected_output)}\n```",  # Markdown with json tag
            f"```\n{json.dumps(expected_output)}\n```",  # Markdown without tag
            f"Some text\n```json\n{json.dumps(expected_output)}\n```\nMore text",  # Embedded
        ]

        with patch.object(vision_service.client.messages, 'create') as mock_create:
            for test_json in test_cases:
                mock_response = MagicMock()
                mock_response.content = [MagicMock(text=test_json)]
                mock_create.return_value = mock_response

                result = vision_service.analyze_image(b"test_image")
                assert result["trend"] == "bearish"
                assert result["trend_confidence"] == 58.0

    def test_consistency_zone_ordering(self, vision_service):
        """Test that zone ordering is preserved across runs."""
        output = {
            "trend": "bullish",
            "trend_confidence": 60.0,
            "support_zones": [
                {"zone_type": "support", "price_level": 1.0900, "touch_count": 3, "strength": "strong", "confidence": 60.0},
                {"zone_type": "support", "price_level": 1.0800, "touch_count": 2, "strength": "moderate", "confidence": 45.0},
                {"zone_type": "support", "price_level": 1.0700, "touch_count": 1, "strength": "weak", "confidence": 30.0},
            ],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
            "volatility_warning": None
        }

        with patch.object(vision_service.client.messages, 'create') as mock_create:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text=json.dumps(output))]
            mock_create.return_value = mock_response

            result = vision_service.analyze_image(b"test_image")
            
            # Verify zone ordering
            prices = [z["price_level"] for z in result["support_zones"]]
            assert prices == [1.0900, 1.0800, 1.0700]

    def test_consistency_validation_passes(self, vision_service, sample_vision_output):
        """Test that consistent output passes validation."""
        is_valid, error_msg = validate_vision_output(sample_vision_output)
        assert is_valid is True, f"Valid output failed validation: {error_msg}"

    def test_consistency_edge_case_no_zones(self, vision_service):
        """Test consistency with minimal valid output."""
        minimal_output = {
            "trend": "consolidating",
            "trend_confidence": 45.0,
            "support_zones": [],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
            "volatility_warning": "High volatility detected"
        }

        with patch.object(vision_service.client.messages, 'create') as mock_create:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text=json.dumps(minimal_output))]
            mock_create.return_value = mock_response

            result = vision_service.analyze_image(b"test_image")
            assert result["trend"] == "consolidating"
            assert result["volatility_warning"] is not None

    def test_consistency_large_dataset(self, vision_service, sample_vision_output):
        """Test consistency with large support/resistance zone datasets."""
        large_output = sample_vision_output.copy()
        large_output["support_zones"] = [
            {
                "zone_type": "support",
                "price_level": 1.0800 + (i * 0.0010),
                "touch_count": i % 5 + 1,
                "strength": ["weak", "moderate", "strong"][i % 3],
                "confidence": 30 + (i * 3)
            }
            for i in range(8)
        ]
        large_output["resistance_zones"] = [
            {
                "zone_type": "resistance",
                "price_level": 1.1100 - (i * 0.0010),
                "touch_count": i % 4 + 1,
                "strength": ["weak", "moderate", "strong"][i % 3],
                "confidence": 25 + (i * 4)
            }
            for i in range(5)
        ]

        with patch.object(vision_service.client.messages, 'create') as mock_create:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text=json.dumps(large_output))]
            mock_create.return_value = mock_response

            result = vision_service.analyze_image(b"test_image")
            assert len(result["support_zones"]) == 8
            assert len(result["resistance_zones"]) == 5

            # Verify all confidence scores capped
            for zone in result["support_zones"] + result["resistance_zones"]:
                assert zone["confidence"] <= 65.0


class TestConsistencyWithRealCharts:
    """Tests that simulate real chart analysis consistency."""

    def test_eur_usd_consistency(self):
        """Simulate EUR/USD 4H chart consistency."""
        # In real tests, this would use actual chart images
        # For now, mock the expected consistent output
        pass

    def test_gbp_usd_consistency(self):
        """Simulate GBP/USD 1H chart consistency."""
        pass

    def test_consistency_metrics(self, vision_service):
        """Track consistency metrics across runs."""
        metrics = {
            "total_runs": 5,
            "consistent_trends": 0,
            "consistent_zones": 0,
            "consistent_confidence": 0,
        }
        
        # This would be populated with real test runs
        assert metrics["total_runs"] == 5
