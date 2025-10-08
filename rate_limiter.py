"""
Rate Limiter Service
Handles rate limiting per API key
"""

import time
from collections import defaultdict, deque
from datetime import datetime, timedelta


class RateLimiter:
    """Service for rate limiting API requests"""
    
    def __init__(self, requests_per_minute=10, requests_per_hour=60):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute (int): Maximum requests per minute per API key
            requests_per_hour (int): Maximum requests per hour per API key
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Store request timestamps for each API key
        self.minute_requests = defaultdict(deque)
        self.hour_requests = defaultdict(deque)
    
    def check_rate_limit(self, api_key):
        """
        Check if request is within rate limits
        
        Args:
            api_key (str): The API key to check
        
        Returns:
            bool: True if within limits, False if exceeded
        """
        current_time = time.time()
        
        # Clean up old entries and check minute limit
        self._cleanup_old_requests(api_key, current_time)
        
        minute_count = len(self.minute_requests[api_key])
        hour_count = len(self.hour_requests[api_key])
        
        # Check if limits are exceeded
        if minute_count >= self.requests_per_minute:
            return False
        
        if hour_count >= self.requests_per_hour:
            return False
        
        # Record this request
        self.minute_requests[api_key].append(current_time)
        self.hour_requests[api_key].append(current_time)
        
        return True
    
    def _cleanup_old_requests(self, api_key, current_time):
        """Remove requests older than the time windows"""
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        
        # Clean minute requests
        while (self.minute_requests[api_key] and 
               self.minute_requests[api_key][0] < minute_ago):
            self.minute_requests[api_key].popleft()
        
        # Clean hour requests
        while (self.hour_requests[api_key] and 
               self.hour_requests[api_key][0] < hour_ago):
            self.hour_requests[api_key].popleft()
    
    def get_retry_after(self, api_key):
        """
        Get seconds until the next available request slot
        
        Args:
            api_key (str): The API key to check
        
        Returns:
            int: Seconds to wait before retrying
        """
        current_time = time.time()
        self._cleanup_old_requests(api_key, current_time)
        
        # Check minute limit
        if len(self.minute_requests[api_key]) >= self.requests_per_minute:
            oldest_minute = self.minute_requests[api_key][0]
            return int(60 - (current_time - oldest_minute)) + 1
        
        # Check hour limit
        if len(self.hour_requests[api_key]) >= self.requests_per_hour:
            oldest_hour = self.hour_requests[api_key][0]
            return int(3600 - (current_time - oldest_hour)) + 1
        
        return 0
    
    def get_remaining_requests(self, api_key):
        """
        Get remaining requests for an API key
        
        Args:
            api_key (str): The API key to check
        
        Returns:
            dict: Remaining requests per minute and per hour
        """
        current_time = time.time()
        self._cleanup_old_requests(api_key, current_time)
        
        return {
            'per_minute': max(0, self.requests_per_minute - len(self.minute_requests[api_key])),
            'per_hour': max(0, self.requests_per_hour - len(self.hour_requests[api_key]))
        }
    
    def reset_limits(self, api_key):
        """
        Reset rate limits for an API key
        
        Args:
            api_key (str): The API key to reset
        """
        if api_key in self.minute_requests:
            del self.minute_requests[api_key]
        if api_key in self.hour_requests:
            del self.hour_requests[api_key]
