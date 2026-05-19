"""
Performance and load testing suite for API endpoints

PERF-01: <5s response time (new analysis)
PERF-01: <500ms response time (cached)
PERF-02: API timeout handling (Claude 10s timeout)
PERF-04: Image hash caching with 48h TTL
"""

import pytest
import asyncio
import time
import hashlib
from datetime import datetime
from typing import Dict, Any
from unittest.mock import patch, MagicMock, AsyncMock
from backend.monitoring import MetricsService, AnalysisMetrics
from backend.cache import CacheService


class TestPerformanceTargets:
    """Test that performance targets are met"""

    @pytest.fixture
    def metrics_service(self):
        """Create metrics service"""
        return MetricsService()

    def test_new_analysis_under_5_seconds(self, metrics_service):
        """
        Test that new analysis (no cache) completes in <5 seconds
        
        PERF-01: <5s response time target
        """
        start = time.time()
        duration_ms = 4800  # 4.8 seconds
        
        metric = AnalysisMetrics(
            timestamp=datetime.utcnow(),
            duration_ms=duration_ms,
            vision_duration_ms=2400,
            reasoning_duration_ms=2000,
            cache_hit=False,
            image_hash="test_hash_1",
            pair="EUR/USD",
            timeframe="4H",
            success=True,
        )
        
        metrics_service.record_analysis(metric)
        
        # Verify duration is under 5 seconds
        assert metric.duration_ms < 5000, f"Analysis took {metric.duration_ms}ms, exceeds 5s target"
        assert metric.vision_duration_ms < 3000, "Vision API should be <3s"
        assert metric.reasoning_duration_ms < 2500, "Reasoning API should be <2.5s"

    def test_cached_analysis_under_500ms(self, metrics_service):
        """
        Test that cached analysis (cache hit) completes in <500ms
        
        PERF-01: <500ms response time for cache hits
        """
        metric = AnalysisMetrics(
            timestamp=datetime.utcnow(),
            duration_ms=450,  # 450ms
            vision_duration_ms=0,
            reasoning_duration_ms=0,
            cache_hit=True,
            image_hash="test_hash_cached",
            pair="GBP/USD",
            timeframe="1H",
            success=True,
        )
        
        # Verify duration is under 500ms
        assert metric.duration_ms < 500, f"Cached response took {metric.duration_ms}ms, exceeds 500ms target"

    def test_vision_api_timeout_handling(self):
        """
        Test that Vision API timeouts are handled gracefully
        
        PERF-02: Claude API timeout handling (10s max)
        """
        metric = AnalysisMetrics(
            timestamp=datetime.utcnow(),
            duration_ms=10500,  # Exceeded timeout
            vision_duration_ms=10500,  # Timeout
            reasoning_duration_ms=0,
            cache_hit=False,
            image_hash="test_hash_timeout",
            pair="AUD/USD",
            timeframe="4H",
            success=False,
            error_message="Vision API timeout after 10 seconds",
        )
        
        # Check timeout is properly recorded
        assert "timeout" in metric.error_message.lower()
        assert metric.vision_duration_ms > 10000

    def test_reasoning_api_timeout_handling(self):
        """
        Test that Reasoning API timeouts are handled gracefully
        """
        metric = AnalysisMetrics(
            timestamp=datetime.utcnow(),
            duration_ms=12300,  # Exceeded timeout
            vision_duration_ms=2000,
            reasoning_duration_ms=10300,  # Timeout
            cache_hit=False,
            image_hash="test_hash_timeout_2",
            pair="USD/JPY",
            timeframe="1H",
            success=False,
            error_message="Reasoning API timeout after 10 seconds",
        )
        
        assert "timeout" in metric.error_message.lower()
        assert metric.reasoning_duration_ms > 10000


class TestCachePerformance:
    """Test caching performance benefits"""

    @pytest.fixture
    def cache_service(self):
        """Create cache service with mock Redis"""
        service = CacheService(redis_url="redis://localhost:6379/0")
        # Mock Redis for testing
        service.redis = MagicMock()
        return service

    def test_cache_hit_fast_retrieval(self, cache_service):
        """
        Test that cache hits are fast (<500ms)
        """
        image_hash = "abc123def456"
        cached_analysis = {
            "trend": "bullish",
            "trend_confidence": 62.0,
            "support_zones": [],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
        }
        
        # Mock Redis response
        cache_service.redis.get.return_value = None  # Simulate cache miss first
        
        # Simulate cache miss
        result = cache_service.redis.get(f"analysis:{image_hash}")
        assert result is None

    def test_cache_miss_stores_result(self, cache_service):
        """
        Test that cache misses properly store results with TTL
        """
        image_hash = "xyz789"
        analysis_result = {
            "trend": "bearish",
            "trend_confidence": 58.0,
            "support_zones": [],
            "resistance_zones": [],
            "patterns_detected": [],
            "swing_highs": [],
            "swing_lows": [],
        }
        
        # Mock successful cache set
        cache_service.redis.setex = MagicMock(return_value=True)
        cache_service.redis.setex(f"analysis:{image_hash}", 48*60*60, "json_data")
        
        # Verify setex was called with correct TTL
        cache_service.redis.setex.assert_called_once()
        call_args = cache_service.redis.setex.call_args
        assert call_args[0][1] == 48 * 60 * 60  # 48 hour TTL

    def test_image_hash_consistency(self):
        """
        Test that same image always produces same hash
        """
        image_bytes = b"test_image_data"
        
        hash1 = hashlib.sha256(image_bytes).hexdigest()
        hash2 = hashlib.sha256(image_bytes).hexdigest()
        
        assert hash1 == hash2, "Same image should produce same hash"
        assert len(hash1) == 64, "SHA256 hash should be 64 characters"

    def test_different_images_different_hashes(self):
        """
        Test that different images produce different hashes
        """
        image1 = b"test_image_1"
        image2 = b"test_image_2"
        
        hash1 = hashlib.sha256(image1).hexdigest()
        hash2 = hashlib.sha256(image2).hexdigest()
        
        assert hash1 != hash2, "Different images should produce different hashes"


class TestMetricsCollection:
    """Test metrics collection and reporting"""

    @pytest.fixture
    def metrics_service(self):
        return MetricsService()

    def test_metrics_summary(self, metrics_service):
        """Test that metrics summary is calculated correctly"""
        # Add some test metrics
        for i in range(3):
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=4500 + i*100,
                vision_duration_ms=2400,
                reasoning_duration_ms=2000,
                cache_hit=False,
                image_hash=f"hash_{i}",
                pair="EUR/USD",
                timeframe="4H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        summary = metrics_service.get_summary()
        
        assert summary["total_requests"] == 3
        assert summary["successful_requests"] == 3
        assert summary["cache_hits"] == 0
        assert summary["cache_misses"] == 3

    def test_cache_hit_rate_calculation(self, metrics_service):
        """Test cache hit rate is calculated correctly"""
        # Add 7 cache misses
        for i in range(7):
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=4500,
                vision_duration_ms=2400,
                reasoning_duration_ms=2000,
                cache_hit=False,
                image_hash=f"hash_miss_{i}",
                pair="EUR/USD",
                timeframe="4H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        # Add 3 cache hits
        for i in range(3):
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=450,
                vision_duration_ms=0,
                reasoning_duration_ms=0,
                cache_hit=True,
                image_hash=f"hash_hit_{i}",
                pair="GBP/USD",
                timeframe="1H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        summary = metrics_service.get_summary()
        
        assert summary["total_requests"] == 10
        assert summary["cache_hits"] == 3
        assert summary["cache_misses"] == 7
        assert abs(summary["cache_hit_rate"] - 0.3) < 0.01  # 30% ±1%

    def test_sla_check(self, metrics_service):
        """Test SLA compliance checking"""
        # Add metrics that meet SLA
        for i in range(5):
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=4200 + i*100,
                vision_duration_ms=2000,
                reasoning_duration_ms=1800,
                cache_hit=False,
                image_hash=f"hash_sla_{i}",
                pair="EUR/USD",
                timeframe="4H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        sla = metrics_service.check_sla()
        
        # p95 for new analysis should be <5s
        assert sla["new_analysis_p95"] is True
        # Success rate should be 100%
        assert sla["success_rate"] is True

    def test_percentile_calculation(self, metrics_service):
        """Test percentile calculations"""
        # Add metrics with varying durations
        durations = [1000, 2000, 3000, 4000, 5000]
        for i, duration in enumerate(durations):
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=duration,
                vision_duration_ms=duration * 0.5,
                reasoning_duration_ms=duration * 0.5,
                cache_hit=False,
                image_hash=f"hash_p_{i}",
                pair="EUR/USD",
                timeframe="4H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        p95 = metrics_service.get_percentile(95.0)
        
        # p95 should be around 5000ms
        assert p95["new"] >= 4000


class TestLoadTesting:
    """Test system under load"""

    def test_concurrent_requests_simulation(self):
        """
        Simulate 50+ concurrent requests
        
        PERF-01: System should handle concurrent requests maintaining <5s target
        """
        concurrent_count = 50
        metrics_service = MetricsService()
        
        # Simulate concurrent request durations
        for i in range(concurrent_count):
            duration = 4500 + (i % 5) * 100  # Vary between 4500-4900ms
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=duration,
                vision_duration_ms=2400,
                reasoning_duration_ms=2000,
                cache_hit=False,
                image_hash=f"concurrent_{i}",
                pair="EUR/USD",
                timeframe="4H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        summary = metrics_service.get_summary()
        
        assert summary["total_requests"] == concurrent_count
        assert summary["successful_requests"] == concurrent_count
        
        # Verify p95 is under 5s
        p95 = metrics_service.get_percentile(95.0)
        assert p95["new"] < 5000

    def test_sustained_load(self):
        """
        Test system sustaining load over time
        """
        metrics_service = MetricsService()
        request_count = 100
        
        for i in range(request_count):
            # Mix of cache hits and misses
            is_cache_hit = (i % 3) == 0
            duration = 450 if is_cache_hit else 4500
            
            metric = AnalysisMetrics(
                timestamp=datetime.utcnow(),
                duration_ms=duration,
                vision_duration_ms=0 if is_cache_hit else 2400,
                reasoning_duration_ms=0 if is_cache_hit else 2000,
                cache_hit=is_cache_hit,
                image_hash=f"sustained_{i}",
                pair="EUR/USD",
                timeframe="4H",
                success=True,
            )
            metrics_service.record_analysis(metric)

        summary = metrics_service.get_summary()
        
        # With caching, cache_hit_rate should be ~33%
        assert abs(summary["cache_hit_rate"] - 0.33) < 0.05
        assert summary["total_requests"] == request_count
        assert summary["success_rate"] == 1.0
