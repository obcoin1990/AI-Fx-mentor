-- 001_audit_logs.sql
-- Initial schema for AI Chart Mentor MVP
-- Creates audit_logs table (JSON only, no image storage - PRIVACY-01)

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Only store analysis JSON output (no images) - PRIVACY-02
    analysis_json JSONB NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Auto-expiry after 30 days - PRIVACY-04
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days'
);

-- Index for efficient cleanup of expired records - PRIVACY-04
CREATE INDEX IF NOT EXISTS idx_audit_logs_expires_at ON audit_logs(expires_at);

-- Index for recent query optimization
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- Cache keys table for image hash caching (48h TTL) - PERF-04
CREATE TABLE IF NOT EXISTS cache_keys (
    key VARCHAR(256) PRIMARY KEY,
    
    -- Cache stores analysis result JSON
    value JSONB NOT NULL,
    
    -- TTL in seconds (48 hours = 172800 seconds) - PERF-04
    ttl_seconds INT DEFAULT 172800,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Auto-expiry time (computed from ttl_seconds)
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP + INTERVAL '172800 seconds'
);

-- Index for efficient cache cleanup
CREATE INDEX IF NOT EXISTS idx_cache_keys_expires_at ON cache_keys(expires_at);

-- Index for quick cache key lookups
CREATE INDEX IF NOT EXISTS idx_cache_keys_created_at ON cache_keys(created_at DESC);

-- Comment documenting privacy requirements
COMMENT ON TABLE audit_logs IS 'Stores analysis results only (JSONB). NO chart images stored. Auto-deletes after 30 days per PRIVACY-01 and PRIVACY-04.';
COMMENT ON TABLE cache_keys IS 'Image hash cache with 48h TTL for performance optimization (PERF-04).';
COMMENT ON COLUMN audit_logs.analysis_json IS 'Contains: trend, zones, patterns, trade scenarios, confidence scores. No uploaded images.';
COMMENT ON COLUMN cache_keys.key IS 'SHA256 hash of uploaded image (hex string).';
