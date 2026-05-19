"""
Cache service for storing and retrieving analysis results
Uses Redis for 48-hour TTL image hash caching

PERF-04: Cache by image hash with 48h TTL
PERF-01: <5s response time (new analysis), <500ms (cached)
"""

import logging
import json
from typing import Optional
from datetime import timedelta
import redis
from redis.exceptions import RedisError, ConnectionError

logger = logging.getLogger(__name__)

# Cache TTL: 48 hours
CACHE_TTL_SECONDS = 48 * 60 * 60


class CacheService:
    """Handles caching of analysis results by image hash"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        try:
            self.redis = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis.ping()
            logger.info("Redis cache initialized successfully")
        except (ConnectionError, RedisError) as e:
            logger.warning(f"Redis not available: {e}. Caching disabled.")
            self.redis = None

    async def get(self, image_hash: str) -> Optional[dict]:
        """
        Retrieve cached analysis by image hash.
        
        PERF-04: Cache by image hash (48h TTL)
        PERF-01: Cache hit response <500ms
        
        Args:
            image_hash: SHA256 hash of uploaded image
        
        Returns:
            Cached analysis result or None if not found/expired
        """
        if not self.redis:
            return None
        
        try:
            cache_key = f"analysis:{image_hash}"
            value = self.redis.get(cache_key)
            
            if value:
                logger.info(f"Cache HIT: {image_hash}")
                return json.loads(value)
            else:
                logger.info(f"Cache MISS: {image_hash}")
                return None
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"Cache GET error: {e}")
            return None

    async def set(self, image_hash: str, analysis_result: dict) -> bool:
        """
        Store analysis result in cache with 48-hour TTL.
        
        Args:
            image_hash: SHA256 hash of uploaded image
            analysis_result: Analysis result to cache
        
        Returns:
            Success status
        """
        if not self.redis:
            return False
        
        try:
            cache_key = f"analysis:{image_hash}"
            self.redis.setex(
                cache_key,
                CACHE_TTL_SECONDS,
                json.dumps(analysis_result)
            )
            logger.info(f"Cache SET: {image_hash} (TTL: 48h)")
            return True
        except (RedisError, TypeError) as e:
            logger.error(f"Cache SET error: {e}")
            return False

    async def invalidate(self, image_hash: str) -> bool:
        """
        Invalidate cached analysis result.
        
        Args:
            image_hash: SHA256 hash of uploaded image
        
        Returns:
            Success status
        """
        if not self.redis:
            return False
        
        try:
            cache_key = f"analysis:{image_hash}"
            deleted = self.redis.delete(cache_key)
            if deleted:
                logger.info(f"Cache INVALIDATED: {image_hash}")
            return bool(deleted)
        except RedisError as e:
            logger.error(f"Cache INVALIDATE error: {e}")
            return False

    async def clear_expired(self) -> int:
        """
        Cleanup expired cache entries (automated job).
        
        Note: Redis automatically expires keys with TTL, so this is mainly
        for manual cleanup if needed.
        
        Returns:
            Number of entries deleted (0 for automatic expiration)
        """
        if not self.redis:
            return 0
        
        try:
            # Redis automatically handles TTL expiration
            # This method scans for manually invalidated entries
            deleted = 0
            cursor = 0
            
            # Scan all keys matching pattern analysis:*
            while True:
                cursor, keys = self.redis.scan(cursor, match="analysis:*", count=100)
                
                for key in keys:
                    # Check TTL
                    ttl = self.redis.ttl(key)
                    if ttl < 0:  # Key has no TTL or is deleted
                        deleted += self.redis.delete(key)
                
                if cursor == 0:
                    break
            
            logger.info(f"Cache cleanup: removed {deleted} expired entries")
            return deleted
        except RedisError as e:
            logger.error(f"Cache cleanup error: {e}")
            return 0

    def get_stats(self) -> dict:
        """
        Get cache statistics for monitoring.
        
        Returns:
            Dict with cache hit/miss counts and memory usage
        """
        if not self.redis:
            return {"enabled": False}
        
        try:
            info = self.redis.info()
            keys_count = self.redis.dbsize()
            
            return {
                "enabled": True,
                "total_keys": keys_count,
                "memory_used": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
            }
        except RedisError as e:
            logger.error(f"Cache stats error: {e}")
            return {"enabled": False, "error": str(e)}
