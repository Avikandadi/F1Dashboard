"""
Cache service for data caching
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Any
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Simple SQLite-based cache service"""
    
    def __init__(self):
        self.db_path = "cache.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize the cache database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error initializing cache database: {e}")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not settings.enable_cache:
            return None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT value, expires_at FROM cache WHERE key = ?",
                (key,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result is None:
                return None
            
            value, expires_at = result
            expires_at = datetime.fromisoformat(expires_at)
            
            # Check if expired
            if expires_at < datetime.now():
                await self.delete(key)
                return None
            
            return json.loads(value)
            
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl_hours: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not settings.enable_cache:
            return False
        
        try:
            ttl_hours = ttl_hours or settings.cache_ttl_hours
            expires_at = datetime.now() + timedelta(hours=ttl_hours)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
                (key, json.dumps(value, default=str), expires_at.isoformat())
            )
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    async def clear_expired(self) -> int:
        """Clear expired cache entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM cache WHERE expires_at < ?",
                (datetime.now().isoformat(),)
            )
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            logger.info(f"Cleared {deleted_count} expired cache entries")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")
            return 0


# Global cache instance
cache_service = CacheService()
