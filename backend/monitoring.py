"""
Monitoring and performance metrics service

PERF-01: Track response times <5s (new) and <500ms (cached)
PERF-02: Monitor API timeouts
PERF-03: Log all analyses
PERF-04: Monitor cache hit rate
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class AnalysisMetrics:
    """Metrics for a single analysis request"""
    timestamp: datetime
    duration_ms: float  # Total duration
    vision_duration_ms: float  # Time for Vision API
    reasoning_duration_ms: float  # Time for Reasoning API
    cache_hit: bool
    image_hash: str
    pair: Optional[str]
    timeframe: Optional[str]
    success: bool
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/storage"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "vision_duration_ms": self.vision_duration_ms,
            "reasoning_duration_ms": self.reasoning_duration_ms,
            "cache_hit": self.cache_hit,
            "image_hash": self.image_hash,
            "pair": self.pair,
            "timeframe": self.timeframe,
            "success": self.success,
            "error_message": self.error_message,
        }


class MetricsService:
    """Track and report performance metrics"""

    def __init__(self):
        self.metrics: list[AnalysisMetrics] = []
        self.durations_cache_hit: list[float] = []
        self.durations_cache_miss: list[float] = []
        self.start_time = datetime.utcnow()
        
        # Counters
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.vision_timeouts = 0
        self.reasoning_timeouts = 0

    def record_analysis(self, metric: AnalysisMetrics) -> None:
        """Record metrics for completed analysis"""
        self.metrics.append(metric)
        self.total_requests += 1

        if metric.success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        if metric.cache_hit:
            self.cache_hits += 1
            self.durations_cache_hit.append(metric.duration_ms)
        else:
            self.cache_misses += 1
            self.durations_cache_miss.append(metric.duration_ms)

        # Check for timeouts
        if "timeout" in (metric.error_message or "").lower():
            if metric.vision_duration_ms > 10000:
                self.vision_timeouts += 1
            if metric.reasoning_duration_ms > 10000:
                self.reasoning_timeouts += 1

        logger.info(
            f"Analysis recorded: {metric.pair}/{metric.timeframe} "
            f"({metric.duration_ms:.0f}ms, cache_hit={metric.cache_hit})"
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        if not self.metrics:
            return {
                "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "cache_hit_rate": 0.0,
            }

        cache_hit_rate = self.cache_hits / self.total_requests if self.total_requests > 0 else 0

        # Calculate percentiles for cache hits
        cache_hit_avg = sum(self.durations_cache_hit) / len(self.durations_cache_hit) if self.durations_cache_hit else 0
        cache_miss_avg = sum(self.durations_cache_miss) / len(self.durations_cache_miss) if self.durations_cache_miss else 0

        return {
            "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0,
            "cache_hit_rate": cache_hit_rate,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "avg_duration_ms_cached": cache_hit_avg,
            "avg_duration_ms_new": cache_miss_avg,
            "vision_timeouts": self.vision_timeouts,
            "reasoning_timeouts": self.reasoning_timeouts,
        }

    def get_percentile(self, percentile: float = 95.0) -> Dict[str, float]:
        """
        Get response time percentiles (e.g., p95, p99)
        
        Args:
            percentile: Percentile to calculate (0-100)
        
        Returns:
            Dict with cached and new analysis percentiles
        """
        def calc_percentile(values: list[float], p: float) -> float:
            if not values:
                return 0.0
            sorted_values = sorted(values)
            index = int((p / 100) * len(sorted_values))
            return sorted_values[min(index, len(sorted_values) - 1)]

        return {
            "cached": calc_percentile(self.durations_cache_hit, percentile),
            "new": calc_percentile(self.durations_cache_miss, percentile),
        }

    def check_sla(self) -> Dict[str, bool]:
        """
        Check if SLA targets are met
        
        Returns:
            Dict with SLA status for each metric
        """
        p95_new = self.get_percentile(95.0)["new"]
        p95_cached = self.get_percentile(95.0)["cached"]
        cache_hit_rate = self.cache_hits / self.total_requests if self.total_requests > 0 else 0

        return {
            "new_analysis_p95": p95_new < 5000,  # <5s
            "cached_analysis_p95": p95_cached < 500,  # <500ms
            "cache_hit_rate": cache_hit_rate > 0.3,  # >30%
            "success_rate": (self.successful_requests / self.total_requests) > 0.95 if self.total_requests > 0 else False,
        }

    def get_timeline(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get metrics grouped by hour for the last N hours
        
        Args:
            hours: Number of hours to look back
        
        Returns:
            Timeline of metrics
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_metrics = [m for m in self.metrics if m.timestamp > cutoff]

        # Group by hour
        hourly = defaultdict(lambda: {
            "count": 0,
            "cache_hits": 0,
            "avg_duration": 0,
            "errors": 0,
        })

        total_duration = 0
        for metric in recent_metrics:
            hour_key = metric.timestamp.strftime("%Y-%m-%d %H:00")
            hourly[hour_key]["count"] += 1
            if metric.cache_hit:
                hourly[hour_key]["cache_hits"] += 1
            if not metric.success:
                hourly[hour_key]["errors"] += 1
            total_duration += metric.duration_ms

        # Calculate averages
        for hour_key in hourly:
            if hourly[hour_key]["count"] > 0:
                hourly[hour_key]["avg_duration"] = (
                    total_duration / len(recent_metrics) if recent_metrics else 0
                )

        return {
            "period_hours": hours,
            "total_metrics": len(recent_metrics),
            "hourly": dict(hourly),
        }

    def reset(self) -> None:
        """Reset all metrics (for testing)"""
        self.metrics.clear()
        self.durations_cache_hit.clear()
        self.durations_cache_miss.clear()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.vision_timeouts = 0
        self.reasoning_timeouts = 0
        self.start_time = datetime.utcnow()


# Global metrics instance
metrics_service = MetricsService()
