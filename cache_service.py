"""
Cache Service
Handles screenshot caching with 24-hour expiration
"""

import hashlib
import json
import time
from pathlib import Path
from datetime import datetime, timedelta


class CacheService:
    """Service for caching screenshots"""
    
    def __init__(self, cache_duration_hours=24):
        """
        Initialize cache service
        
        Args:
            cache_duration_hours (int): Cache duration in hours
        """
        self.cache_duration_hours = cache_duration_hours
        self.cache_dir = Path('cache')
        self.cache_dir.mkdir(exist_ok=True)
        
        self.cache_index_file = self.cache_dir / 'cache_index.json'
        self.cache_index = self._load_cache_index()
    
    def _load_cache_index(self):
        """Load cache index from file"""
        if not self.cache_index_file.exists():
            return {}
        
        try:
            with open(self.cache_index_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_cache_index(self):
        """Save cache index to file"""
        try:
            with open(self.cache_index_file, 'w') as f:
                json.dump(self.cache_index, f, indent=2)
        except Exception as e:
            print(f"Error saving cache index: {e}")
    
    def generate_cache_key(self, url, width, height, fullpage, image_format, quality, delay=0):
        """
        Generate a unique cache key based on parameters
        
        Args:
            url (str): URL of the webpage
            width (int): Viewport width
            height (int): Viewport height
            fullpage (bool): Full page capture flag
            image_format (str): Image format
            quality (int): Image quality
            delay (int): Delay before capture in milliseconds
        
        Returns:
            str: Cache key hash
        """
        key_string = f"{url}|{width}|{height}|{fullpage}|{image_format}|{quality}|{delay}"
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def get_cached_screenshot(self, cache_key):
        """
        Get cached screenshot if it exists and is not expired
        
        Args:
            cache_key (str): Cache key
        
        Returns:
            str or None: Path to cached file if valid, None otherwise
        """
        # Check if cache entry exists
        if cache_key not in self.cache_index:
            return None
        
        cache_entry = self.cache_index[cache_key]
        cached_file = Path(cache_entry['file_path'])
        
        # Check if file exists
        if not cached_file.exists():
            # Remove invalid entry
            del self.cache_index[cache_key]
            self._save_cache_index()
            return None
        
        # Check if cache is expired
        cached_time = datetime.fromisoformat(cache_entry['timestamp'])
        expiry_time = cached_time + timedelta(hours=self.cache_duration_hours)
        
        if datetime.now() > expiry_time:
            # Cache expired, remove it
            try:
                cached_file.unlink()
            except Exception:
                pass
            del self.cache_index[cache_key]
            self._save_cache_index()
            return None
        
        return str(cached_file)
    
    def cache_screenshot(self, cache_key, screenshot_path):
        """
        Cache a screenshot
        
        Args:
            cache_key (str): Cache key
            screenshot_path (str): Path to screenshot file
        
        Returns:
            str: Path to cached file
        """
        source_path = Path(screenshot_path)
        
        # Determine file extension
        extension = source_path.suffix
        
        # Create cached file path
        cached_filename = f"{cache_key}{extension}"
        cached_filepath = self.cache_dir / cached_filename
        
        # Copy file to cache directory
        try:
            import shutil
            shutil.copy2(source_path, cached_filepath)
            
            # Update cache index
            self.cache_index[cache_key] = {
                'file_path': str(cached_filepath),
                'timestamp': datetime.now().isoformat(),
                'original_path': str(source_path)
            }
            
            self._save_cache_index()
            
            return str(cached_filepath)
        
        except Exception as e:
            print(f"Error caching screenshot: {e}")
            return str(source_path)
    
    def cleanup_expired_cache(self):
        """Remove all expired cache entries"""
        current_time = datetime.now()
        expired_keys = []
        
        for cache_key, cache_entry in self.cache_index.items():
            cached_time = datetime.fromisoformat(cache_entry['timestamp'])
            expiry_time = cached_time + timedelta(hours=self.cache_duration_hours)
            
            if current_time > expiry_time:
                expired_keys.append(cache_key)
                # Try to remove the file
                try:
                    Path(cache_entry['file_path']).unlink()
                except Exception:
                    pass
        
        # Remove expired entries from index
        for key in expired_keys:
            del self.cache_index[key]
        
        if expired_keys:
            self._save_cache_index()
        
        return len(expired_keys)
    
    def clear_all_cache(self):
        """Clear all cached screenshots"""
        # Remove all cached files
        for cache_entry in self.cache_index.values():
            try:
                Path(cache_entry['file_path']).unlink()
            except Exception:
                pass
        
        # Clear index
        self.cache_index = {}
        self._save_cache_index()
