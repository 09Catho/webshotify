"""
Dashboard Service
Handles usage statistics, analytics, and API key management
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
from collections import defaultdict


class DashboardService:
    """Service for dashboard analytics and statistics"""
    
    def __init__(self, log_file='logs/api_requests.log'):
        self.log_file = Path(log_file)
        self.stats_cache = {}
        self.cache_time = None
        self.cache_duration = 300  # 5 minutes
    
    def get_api_usage_stats(self, api_key=None, days=30):
        """
        Get usage statistics for dashboard
        
        Args:
            api_key (str): Filter by specific API key (None for all)
            days (int): Number of days to analyze
        
        Returns:
            dict: Usage statistics
        """
        # Check cache
        cache_key = f"{api_key}_{days}"
        if self._is_cache_valid(cache_key):
            return self.stats_cache.get(cache_key)
        
        stats = self._analyze_logs(api_key, days)
        
        # Update cache
        self.stats_cache[cache_key] = stats
        self.cache_time = datetime.now()
        
        return stats
    
    def _is_cache_valid(self, cache_key):
        """Check if cache is still valid"""
        if not self.cache_time or cache_key not in self.stats_cache:
            return False
        
        age = (datetime.now() - self.cache_time).total_seconds()
        return age < self.cache_duration
    
    def _analyze_logs(self, api_key, days):
        """Analyze log file for statistics"""
        if not self.log_file.exists():
            return self._empty_stats()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cached_requests': 0,
            'requests_by_day': defaultdict(int),
            'requests_by_hour': defaultdict(int),
            'requests_by_status': defaultdict(int),
            'requests_by_endpoint': defaultdict(int),
            'top_urls': defaultdict(int),
            'average_response_time': 0,
            'total_screenshots': 0,
            'total_pdfs': 0,
            'total_comparisons': 0,
            'browsers_used': defaultdict(int),
            'devices_used': defaultdict(int),
            'formats_used': defaultdict(int)
        }
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    try:
                        # Parse log line
                        if ' - ' not in line:
                            continue
                        
                        # Extract timestamp
                        timestamp_str = line.split('[')[1].split(']')[0] if '[' in line else None
                        if not timestamp_str:
                            continue
                        
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                        
                        if timestamp < cutoff_date:
                            continue
                        
                        # Filter by API key if specified
                        if api_key and api_key not in line:
                            continue
                        
                        # Count requests
                        stats['total_requests'] += 1
                        
                        # Count by day
                        day_key = timestamp.strftime('%Y-%m-%d')
                        stats['requests_by_day'][day_key] += 1
                        
                        # Count by hour
                        hour_key = timestamp.hour
                        stats['requests_by_hour'][hour_key] += 1
                        
                        # Extract status code
                        if ' 200 ' in line or 'successfully' in line.lower():
                            stats['successful_requests'] += 1
                            stats['requests_by_status']['200'] += 1
                        elif ' 400 ' in line:
                            stats['failed_requests'] += 1
                            stats['requests_by_status']['400'] += 1
                        elif ' 401 ' in line:
                            stats['failed_requests'] += 1
                            stats['requests_by_status']['401'] += 1
                        elif ' 429 ' in line:
                            stats['failed_requests'] += 1
                            stats['requests_by_status']['429'] += 1
                        elif ' 500 ' in line:
                            stats['failed_requests'] += 1
                            stats['requests_by_status']['500'] += 1
                        
                        # Count cached requests
                        if 'cache' in line.lower():
                            stats['cached_requests'] += 1
                        
                        # Count by endpoint
                        if '/screenshot' in line:
                            stats['requests_by_endpoint']['screenshot'] += 1
                            stats['total_screenshots'] += 1
                        if '/batch' in line:
                            stats['requests_by_endpoint']['batch'] += 1
                        if '/compare' in line:
                            stats['requests_by_endpoint']['compare'] += 1
                            stats['total_comparisons'] += 1
                        if 'pdf' in line.lower():
                            stats['total_pdfs'] += 1
                            stats['formats_used']['pdf'] += 1
                        if 'png' in line.lower():
                            stats['formats_used']['png'] += 1
                        if 'jpeg' in line.lower():
                            stats['formats_used']['jpeg'] += 1
                        
                        # Extract URL if present
                        if 'URL:' in line or 'url=' in line:
                            # Simple URL extraction (can be improved)
                            pass
                        
                    except Exception as e:
                        # Skip malformed log lines
                        continue
        
        except Exception as e:
            print(f"Error analyzing logs: {e}")
        
        # Calculate derived stats
        if stats['total_requests'] > 0:
            stats['success_rate'] = round((stats['successful_requests'] / stats['total_requests']) * 100, 2)
            stats['cache_hit_rate'] = round((stats['cached_requests'] / stats['total_requests']) * 100, 2)
        else:
            stats['success_rate'] = 0
            stats['cache_hit_rate'] = 0
        
        return stats
    
    def _empty_stats(self):
        """Return empty statistics structure"""
        return {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cached_requests': 0,
            'requests_by_day': {},
            'requests_by_hour': {},
            'requests_by_status': {},
            'requests_by_endpoint': {},
            'success_rate': 0,
            'cache_hit_rate': 0,
            'total_screenshots': 0,
            'total_pdfs': 0,
            'total_comparisons': 0
        }
    
    def get_api_key_stats(self, auth_service):
        """
        Get statistics for all API keys
        
        Args:
            auth_service: AuthService instance
        
        Returns:
            list: List of API key statistics
        """
        api_keys = auth_service.api_keys.get('keys', [])
        
        key_stats = []
        for key_data in api_keys:
            key = key_data.get('key')
            stats = self.get_api_usage_stats(api_key=key, days=30)
            
            key_stats.append({
                'key': key[:10] + '...' + key[-4:],  # Masked for security
                'full_key': key,
                'description': key_data.get('description', 'No description'),
                'active': key_data.get('active', True),
                'created': key_data.get('created', 'Unknown'),
                'total_requests': stats['total_requests'],
                'success_rate': stats['success_rate'],
                'last_used': key_data.get('last_used', 'Never')
            })
        
        return key_stats
    
    def get_recent_requests(self, limit=50):
        """
        Get recent API requests
        
        Args:
            limit (int): Maximum number of requests to return
        
        Returns:
            list: Recent requests
        """
        if not self.log_file.exists():
            return []
        
        requests = []
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                # Get last N lines
                for line in lines[-limit:]:
                    try:
                        if ' - ' not in line:
                            continue
                        
                        # Parse log line
                        timestamp_str = line.split('[')[1].split(']')[0] if '[' in line else 'Unknown'
                        
                        # Extract info
                        request_info = {
                            'timestamp': timestamp_str,
                            'message': line.split('] ')[-1].strip() if '] ' in line else line.strip(),
                            'status': 'success' if '200' in line or 'success' in line.lower() else 'error'
                        }
                        
                        requests.append(request_info)
                        
                    except Exception:
                        continue
        
        except Exception as e:
            print(f"Error reading recent requests: {e}")
        
        return list(reversed(requests))  # Most recent first
    
    def get_system_health(self):
        """
        Get system health metrics
        
        Returns:
            dict: System health information
        """
        import psutil
        import os
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_total_mb = memory.total / (1024 * 1024)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024 * 1024 * 1024)
            
            # Uptime (if possible)
            try:
                uptime_seconds = time.time() - psutil.boot_time()
                uptime_hours = uptime_seconds / 3600
            except:
                uptime_hours = 0
            
            return {
                'status': 'healthy' if cpu_percent < 80 and memory_percent < 90 else 'warning',
                'cpu_usage': round(cpu_percent, 1),
                'memory_usage': round(memory_percent, 1),
                'memory_used_mb': round(memory_used_mb, 1),
                'memory_total_mb': round(memory_total_mb, 1),
                'disk_usage': round(disk_percent, 1),
                'disk_free_gb': round(disk_free_gb, 1),
                'uptime_hours': round(uptime_hours, 1)
            }
        
        except Exception as e:
            return {
                'status': 'unknown',
                'error': str(e)
            }
