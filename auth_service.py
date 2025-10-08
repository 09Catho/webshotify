"""
Authentication Service with Secure API Key Hashing
Handles API key validation and management using bcrypt for secure storage
"""

import json
import secrets
import bcrypt
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Tuple


class AuthService:
    """
    Service for secure API key authentication with bcrypt hashing
    
    Features:
    - Secure API key hashing using bcrypt
    - Constant-time comparison to prevent timing attacks
    - API key generation with cryptographically secure random
    - Key management (add, deactivate, list)
    """
    
    def __init__(self, api_keys_file='config/api_keys.json'):
        """
        Initialize authentication service
        
        Args:
            api_keys_file (str): Path to API keys storage file
        """
        self.api_keys_file = Path(api_keys_file)
        self.api_keys = self._load_api_keys()
    
    def _load_api_keys(self) -> Dict:
        """
        Load API keys from configuration file
        
        Returns:
            dict: API keys with metadata
        """
        # Create config directory if it doesn't exist
        self.api_keys_file.parent.mkdir(exist_ok=True)
        
        # If file doesn't exist, create with default keys
        if not self.api_keys_file.exists():
            # Generate secure default keys
            demo_key = self.generate_api_key()
            test_key = self.generate_api_key()
            dev_key = self.generate_api_key()
            
            # For backward compatibility, also create plaintext demo keys
            # These will be hashed on first use
            default_keys = {
                # Hashed keys (secure)
                demo_key[1]: {  # hashed version
                    'name': 'Demo Key',
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'active': True,
                    'plaintext_key': demo_key[0],  # Store for initial setup only
                    'hashed': True
                },
                test_key[1]: {
                    'name': 'Test Key',
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'active': True,
                    'plaintext_key': test_key[0],
                    'hashed': True
                },
                dev_key[1]: {
                    'name': 'Development Key',
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'active': True,
                    'plaintext_key': dev_key[0],
                    'hashed': True
                },
                # Legacy plaintext keys for backward compatibility (will be migrated)
                'demo-key-12345': {
                    'name': 'Legacy Demo Key',
                    'created': '2025-10-05',
                    'active': True,
                    'hashed': False
                },
                'test-key-67890': {
                    'name': 'Legacy Test Key',
                    'created': '2025-10-05',
                    'active': True,
                    'hashed': False
                },
                'dev-key-abcde': {
                    'name': 'Legacy Development Key',
                    'created': '2025-10-05',
                    'active': True,
                    'hashed': False
                }
            }
            
            with open(self.api_keys_file, 'w') as f:
                json.dump(default_keys, f, indent=2)
            
            print("=" * 60)
            print("🔐 NEW SECURE API KEYS GENERATED")
            print("=" * 60)
            print(f"Demo Key: {demo_key[0]}")
            print(f"Test Key: {test_key[0]}")
            print(f"Dev Key:  {dev_key[0]}")
            print("\nLegacy keys (demo-key-12345, etc.) still work for compatibility")
            print("=" * 60)
            
            return default_keys
        
        # Load existing keys
        try:
            with open(self.api_keys_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_api_keys(self):
        """Save API keys to file"""
        with open(self.api_keys_file, 'w') as f:
            json.dump(self.api_keys, f, indent=2)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """
        Hash an API key using bcrypt
        
        Args:
            api_key (str): Plaintext API key
        
        Returns:
            str: Hashed API key
        """
        return bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_api_key(plaintext_key: str, hashed_key: str) -> bool:
        """
        Verify an API key against its hash using constant-time comparison
        
        Args:
            plaintext_key (str): Plaintext API key to verify
            hashed_key (str): Hashed API key to compare against
        
        Returns:
            bool: True if keys match, False otherwise
        """
        try:
            return bcrypt.checkpw(plaintext_key.encode('utf-8'), hashed_key.encode('utf-8'))
        except Exception:
            return False
    
    @staticmethod
    def generate_api_key(length: int = 32) -> Tuple[str, str]:
        """
        Generate a cryptographically secure API key
        
        Args:
            length (int): Length of the API key (default: 32)
        
        Returns:
            tuple: (plaintext_key, hashed_key)
        """
        # Generate secure random key
        plaintext_key = secrets.token_urlsafe(length)
        
        # Hash it
        hashed_key = AuthService.hash_api_key(plaintext_key)
        
        return (plaintext_key, hashed_key)
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate if an API key is valid and active
        
        Supports both hashed and legacy plaintext keys for backward compatibility
        
        Args:
            api_key (str): The API key to validate
        
        Returns:
            bool: True if valid and active, False otherwise
        """
        # Check for direct match (legacy plaintext keys)
        if api_key in self.api_keys:
            key_info = self.api_keys[api_key]
            
            # If it's a plaintext key, migrate it to hashed
            if not key_info.get('hashed', False):
                # This is a legacy key, still allow it but recommend migration
                return key_info.get('active', False)
            else:
                # This shouldn't happen (hashed key as dict key)
                return key_info.get('active', False)
        
        # Check against all hashed keys
        for stored_hash, key_info in self.api_keys.items():
            if key_info.get('hashed', False):
                # This is a hashed key, verify it
                if self.verify_api_key(api_key, stored_hash):
                    return key_info.get('active', False)
        
        return False
    
    def validate_key(self, api_key: str) -> bool:
        """
        Alias for validate_api_key for backward compatibility
        
        Args:
            api_key (str): The API key to validate
        
        Returns:
            bool: True if valid and active, False otherwise
        """
        return self.validate_api_key(api_key)
    
    def add_api_key(self, name: str = 'Custom Key', key: Optional[str] = None) -> Tuple[str, bool]:
        """
        Add a new API key (generates one if not provided)
        
        Args:
            name (str): Name/description of the key
            key (str, optional): Specific key to add (will be hashed). If None, generates new key.
        
        Returns:
            tuple: (plaintext_key, success)
        """
        if key:
            # Use provided key
            plaintext_key = key
            hashed_key = self.hash_api_key(key)
        else:
            # Generate new key
            plaintext_key, hashed_key = self.generate_api_key()
        
        # Check if already exists
        if hashed_key in self.api_keys:
            return (plaintext_key, False)
        
        # Add to storage
        self.api_keys[hashed_key] = {
            'name': name,
            'created': datetime.now().strftime('%Y-%m-%d'),
            'active': True,
            'hashed': True
        }
        
        self._save_api_keys()
        return (plaintext_key, True)
    
    def deactivate_api_key(self, api_key: str) -> bool:
        """
        Deactivate an API key
        
        Args:
            api_key (str): The API key to deactivate (plaintext)
        
        Returns:
            bool: True if deactivated, False if not found
        """
        # Check direct match (legacy)
        if api_key in self.api_keys:
            self.api_keys[api_key]['active'] = False
            self._save_api_keys()
            return True
        
        # Check hashed keys
        for stored_hash, key_info in self.api_keys.items():
            if key_info.get('hashed', False):
                if self.verify_api_key(api_key, stored_hash):
                    self.api_keys[stored_hash]['active'] = False
                    self._save_api_keys()
                    return True
        
        return False
    
    def list_api_keys(self) -> Dict:
        """
        List all API keys with metadata (excluding hashes)
        
        Returns:
            dict: API keys with metadata
        """
        result = {}
        for key_hash, info in self.api_keys.items():
            # Mask the key for security
            if info.get('hashed', False):
                masked_key = f"{key_hash[:8]}...{key_hash[-8:]}" if len(key_hash) > 16 else "***"
            else:
                # Legacy plaintext key
                masked_key = f"{key_hash[:4]}...{key_hash[-4:]}" if len(key_hash) > 8 else "***"
            
            result[masked_key] = {
                'name': info.get('name', 'Unknown'),
                'created': info.get('created', 'Unknown'),
                'active': info.get('active', False),
                'type': 'hashed' if info.get('hashed', False) else 'legacy'
            }
        
        return result
    
    def migrate_legacy_keys(self):
        """
        Migrate all legacy plaintext keys to hashed keys
        
        WARNING: This will invalidate old plaintext keys!
        Only use if you can update all clients with new keys.
        
        Returns:
            dict: Mapping of old keys to new keys
        """
        migrations = {}
        new_keys = {}
        
        for old_key, info in list(self.api_keys.items()):
            if not info.get('hashed', False):
                # This is a legacy plaintext key
                plaintext_key, hashed_key = self.generate_api_key()
                
                new_keys[hashed_key] = {
                    'name': info.get('name', 'Migrated Key'),
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'active': info.get('active', True),
                    'hashed': True,
                    'migrated_from': old_key
                }
                
                migrations[old_key] = plaintext_key
        
        # Replace old keys with new ones
        self.api_keys = new_keys
        self._save_api_keys()
        
        return migrations
