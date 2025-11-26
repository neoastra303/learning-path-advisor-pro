"""
Caching Layer for Learning Path Advisor
Provides multi-level caching: in-memory LRU cache and function-level caching
"""
import time
import logging
from functools import wraps
from typing import Callable, Any, Dict, Optional, Tuple
from collections import OrderedDict
from threading import Lock
import json

logger = logging.getLogger(__name__)


class CacheConfig:
    """Configuration for cache behavior"""
    DEFAULT_TTL = 3600  # 1 hour in seconds
    DEFAULT_MAX_SIZE = 1000
    CACHE_STATS_ENABLED = True


class CacheEntry:
    """Single cache entry with TTL and metadata"""
    def __init__(self, value: Any, ttl: Optional[int] = None):
        self.value = value
        self.ttl = ttl or CacheConfig.DEFAULT_TTL
        self.created_at = time.time()
        self.accessed_at = time.time()
        self.access_count = 0
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return (time.time() - self.created_at) > self.ttl
    
    def access(self) -> Any:
        """Record access and return value"""
        self.accessed_at = time.time()
        self.access_count += 1
        return self.value


class InMemoryCache:
    """
    Thread-safe in-memory LRU cache with TTL support
    """
    def __init__(self, max_size: int = CacheConfig.DEFAULT_MAX_SIZE):
        self.max_size = max_size
        self.cache: Dict[str, CacheEntry] = OrderedDict()
        self.lock = Lock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'expirations': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key not in self.cache:
                self.stats['misses'] += 1
                return None
            
            entry = self.cache[key]
            
            # Check expiration
            if entry.is_expired():
                del self.cache[key]
                self.stats['expirations'] += 1
                logger.debug(f"Cache expired: {key}")
                return None
            
            # Move to end (LRU)
            self.cache.move_to_end(key)
            
            self.stats['hits'] += 1
            return entry.access()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        with self.lock:
            # Remove if exists (will re-add to end)
            if key in self.cache:
                del self.cache[key]
            
            # Check size and evict if needed
            if len(self.cache) >= self.max_size:
                evicted_key, _ = self.cache.popitem(last=False)
                self.stats['evictions'] += 1
                logger.debug(f"Cache evicted: {evicted_key}")
            
            # Add new entry
            self.cache[key] = CacheEntry(value, ttl)
            logger.debug(f"Cache set: {key}")
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"Cache deleted: {key}")
                return True
            return False
    
    def clear(self) -> None:
        """Clear entire cache"""
        with self.lock:
            self.cache.clear()
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'evictions': self.stats['evictions'],
                'expirations': self.stats['expirations'],
                'hit_rate': f"{hit_rate:.2f}%"
            }
    
    def reset_stats(self) -> None:
        """Reset cache statistics"""
        with self.lock:
            self.stats = {
                'hits': 0,
                'misses': 0,
                'evictions': 0,
                'expirations': 0
            }


# Global cache instance
_global_cache = InMemoryCache()


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from function args and kwargs"""
    key_parts = [str(arg) for arg in args]
    for k, v in sorted(kwargs.items()):
        if isinstance(v, (list, dict)):
            key_parts.append(f"{k}={json.dumps(v, sort_keys=True)}")
        else:
            key_parts.append(f"{k}={v}")
    return "|".join(key_parts)


def cached(ttl: Optional[int] = None, cache_instance: Optional[InMemoryCache] = None):
    """
    Decorator for caching function results
    
    Usage:
        @cached(ttl=300)  # 5 minute TTL
        def expensive_function(arg1, arg2):
            ...
    """
    cache = cache_instance or _global_cache
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = cache.get(key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {key}")
                return cached_value
            
            # Call function and cache result
            logger.debug(f"Cache miss: {key}")
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        # Attach cache utilities to wrapper
        wrapper.cache_clear = lambda: cache.delete(f"{func.__name__}:")
        wrapper.cache_stats = lambda: cache.get_stats()
        
        return wrapper
    
    return decorator


def get_global_cache() -> InMemoryCache:
    """Get the global cache instance"""
    return _global_cache


def clear_global_cache() -> None:
    """Clear the global cache"""
    _global_cache.clear()


def get_cache_stats() -> Dict[str, Any]:
    """Get global cache statistics"""
    return _global_cache.get_stats()


def cache_warming(func: Callable) -> Callable:
    """
    Decorator for cache warming (pre-populate cache)
    Useful for expensive startup operations
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Warming cache with {func.__name__}")
        return func(*args, **kwargs)
    
    return wrapper
