"""
Performance Monitoring for Learning Path Advisor
Tracks request timing, algorithm performance, and system metrics
"""
import time
import logging
from functools import wraps
from typing import Callable, Dict, Any, Optional
from collections import defaultdict
from statistics import mean, stdev
from datetime import datetime, timezone
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class PerformanceMetric:
    """Single performance metric"""
    def __init__(self, name: str, value: float, unit: str = "ms"):
        self.name = name
        self.value = value
        self.unit = unit
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'value': f"{self.value:.2f}",
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat()
        }


class PerformanceMonitor:
    """
    Thread-safe performance monitoring system
    Tracks timing for functions, endpoints, and algorithms
    """
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics: Dict[str, list] = defaultdict(list)
        self.endpoints: Dict[str, list] = defaultdict(list)
        self.algorithms: Dict[str, list] = defaultdict(list)
    
    def record_metric(self, name: str, value: float, unit: str = "ms") -> None:
        """Record a performance metric"""
        metric = PerformanceMetric(name, value, unit)
        self.metrics[name].append(metric)
        
        # Trim history if needed
        if len(self.metrics[name]) > self.max_history:
            self.metrics[name] = self.metrics[name][-self.max_history:]
        
        logger.debug(f"Metric recorded: {name} = {value:.2f}{unit}")
    
    def record_endpoint(self, endpoint: str, method: str, duration: float, 
                       status_code: int = 200, error: Optional[str] = None) -> None:
        """Record endpoint request metrics"""
        key = f"{method} {endpoint}"
        self.endpoints[key].append({
            'duration': duration,
            'status_code': status_code,
            'error': error,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        # Trim history
        if len(self.endpoints[key]) > self.max_history:
            self.endpoints[key] = self.endpoints[key][-self.max_history:]
    
    def record_algorithm(self, algorithm_name: str, input_size: int, 
                        duration: float, success: bool = True) -> None:
        """Record algorithm performance"""
        key = algorithm_name
        self.algorithms[key].append({
            'input_size': input_size,
            'duration': duration,
            'success': success,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        # Trim history
        if len(self.algorithms[key]) > self.max_history:
            self.algorithms[key] = self.algorithms[key][-self.max_history:]
    
    def get_metric_stats(self, name: str) -> Dict[str, Any]:
        """Get statistics for a metric"""
        if name not in self.metrics or not self.metrics[name]:
            return None
        
        values = [m.value for m in self.metrics[name]]
        
        return {
            'metric': name,
            'count': len(values),
            'min': f"{min(values):.2f}",
            'max': f"{max(values):.2f}",
            'mean': f"{mean(values):.2f}",
            'stdev': f"{stdev(values):.2f}" if len(values) > 1 else "N/A",
            'unit': 'ms'
        }
    
    def get_endpoint_stats(self, endpoint: str = None) -> Dict[str, Any]:
        """Get statistics for endpoint(s)"""
        if endpoint:
            if endpoint not in self.endpoints:
                return None
            data = self.endpoints[endpoint]
        else:
            data = []
            for ep_data in self.endpoints.values():
                data.extend(ep_data)
        
        if not data:
            return None
        
        durations = [d['duration'] for d in data]
        success_count = sum(1 for d in data if d['status_code'] == 200)
        
        return {
            'total_requests': len(data),
            'successful': success_count,
            'failed': len(data) - success_count,
            'min_duration': f"{min(durations):.2f}ms",
            'max_duration': f"{max(durations):.2f}ms",
            'mean_duration': f"{mean(durations):.2f}ms",
            'stdev_duration': f"{stdev(durations):.2f}ms" if len(durations) > 1 else "N/A"
        }
    
    def get_algorithm_stats(self, algorithm_name: str = None) -> Dict[str, Any]:
        """Get statistics for algorithm(s)"""
        if algorithm_name:
            if algorithm_name not in self.algorithms:
                return None
            data = self.algorithms[algorithm_name]
        else:
            data = []
            for algo_data in self.algorithms.values():
                data.extend(algo_data)
        
        if not data:
            return None
        
        durations = [d['duration'] for d in data]
        success_count = sum(1 for d in data if d['success'])
        
        return {
            'total_runs': len(data),
            'successful': success_count,
            'failed': len(data) - success_count,
            'min_duration': f"{min(durations):.2f}ms",
            'max_duration': f"{max(durations):.2f}ms",
            'mean_duration': f"{mean(durations):.2f}ms",
            'stdev_duration': f"{stdev(durations):.2f}ms" if len(durations) > 1 else "N/A"
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_metrics': sum(len(v) for v in self.metrics.values()),
            'total_endpoint_requests': sum(len(v) for v in self.endpoints.values()),
            'total_algorithm_runs': sum(len(v) for v in self.algorithms.values()),
            'endpoints_tracked': len(self.endpoints),
            'algorithms_tracked': len(self.algorithms)
        }
    
    def clear(self) -> None:
        """Clear all metrics"""
        self.metrics.clear()
        self.endpoints.clear()
        self.algorithms.clear()
        logger.info("Performance metrics cleared")


# Global monitor instance
_global_monitor = PerformanceMonitor()


def timed(name: Optional[str] = None, record_as: str = "metric"):
    """
    Decorator for timing function execution
    
    Usage:
        @timed(name="expensive_function")
        def my_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        func_name = name or func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration_ms = (time.time() - start_time) * 1000
                _global_monitor.record_metric(func_name, duration_ms)
                logger.debug(f"Timed {func_name}: {duration_ms:.2f}ms")
        
        return wrapper
    
    return decorator


def timed_algorithm(algorithm_name: str):
    """
    Decorator for timing algorithm execution with size tracking
    
    Usage:
        @timed_algorithm("dijkstra")
        def find_path(graph, size):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                success = False
                raise
            finally:
                duration_ms = (time.time() - start_time) * 1000
                # Try to get input size from args
                input_size = len(args[0]) if args and hasattr(args[0], '__len__') else 0
                _global_monitor.record_algorithm(algorithm_name, input_size, duration_ms, success)
                logger.debug(f"Algorithm {algorithm_name} completed in {duration_ms:.2f}ms")
        
        return wrapper
    
    return decorator


def get_global_monitor() -> PerformanceMonitor:
    """Get the global performance monitor"""
    return _global_monitor


def get_performance_summary() -> Dict[str, Any]:
    """Get summary of all performance metrics"""
    return _global_monitor.get_summary()


def get_performance_stats(category: str = "all") -> Dict[str, Any]:
    """
    Get detailed performance statistics
    
    Args:
        category: "all", "endpoints", "algorithms", or specific name
    """
    if category == "all":
        return {
            'summary': _global_monitor.get_summary(),
            'endpoints': {k: _global_monitor.get_endpoint_stats(k) 
                         for k in _global_monitor.endpoints.keys()},
            'algorithms': {k: _global_monitor.get_algorithm_stats(k) 
                          for k in _global_monitor.algorithms.keys()}
        }
    elif category == "endpoints":
        return {k: _global_monitor.get_endpoint_stats(k) 
               for k in _global_monitor.endpoints.keys()}
    elif category == "algorithms":
        return {k: _global_monitor.get_algorithm_stats(k) 
               for k in _global_monitor.algorithms.keys()}
    else:
        # Try to find specific metric
        return _global_monitor.get_metric_stats(category)


def clear_performance_stats() -> None:
    """Clear all performance statistics"""
    _global_monitor.clear()