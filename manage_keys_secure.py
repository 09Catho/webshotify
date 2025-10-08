#!/usr/bin/env python3
"""
Secure API Key Management Utility
Manage API keys with bcrypt hashing
"""

import sys
from auth_service import AuthService


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def list_keys():
    """List all API keys"""
    auth = AuthService()
    keys = auth.list_api_keys()
    
    print_header("API KEYS")
    
    if not keys:
        print("No API keys found.")
        return
    
    print(f"\n{'Key (Masked)':<30} {'Name':<20} {'Type':<10} {'Status':<10}")
    print("-" * 70)
    
    for masked_key, info in keys.items():
        status = "Active" if info['active'] else "Inactive"
        key_type = info['type']
        print(f"{masked_key:<30} {info['name']:<20} {key_type:<10} {status:<10}")
    
    print(f"\nTotal: {len(keys)} keys")


def add_key():
    """Add a new API key"""
    auth = AuthService()
    
    print_header("ADD NEW API KEY")
    
    name = input("\nEnter key name (e.g., 'Production Key'): ").strip()
    if not name:
        name = "Custom Key"
    
    plaintext_key, success = auth.add_api_key(name=name)
    
    if success:
        print("\n✅ API Key created successfully!")
        print("\n" + "=" * 60)
        print("🔑 SAVE THIS KEY - IT WILL NOT BE SHOWN AGAIN!")
        print("=" * 60)
        print(f"\nAPI Key: {plaintext_key}")
        print(f"Name: {name}")
        print("\n⚠️  Store this key securely. The hashed version is saved.")
        print("=" * 60)
    else:
        print("\n❌ Failed to create key (already exists)")


def deactivate_key():
    """Deactivate an API key"""
    auth = AuthService()
    
    print_header("DEACTIVATE API KEY")
    
    # First show current keys
    list_keys()
    
    print("\n⚠️  You need the PLAINTEXT key to deactivate it.")
    key = input("\nEnter the plaintext API key to deactivate: ").strip()
    
    if not key:
        print("❌ No key provided")
        return
    
    if auth.deactivate_api_key(key):
        print("\n✅ API key deactivated successfully")
    else:
        print("\n❌ API key not found")


def validate_key():
    """Validate an API key"""
    auth = AuthService()
    
    print_header("VALIDATE API KEY")
    
    key = input("\nEnter API key to validate: ").strip()
    
    if not key:
        print("❌ No key provided")
        return
    
    if auth.validate_api_key(key):
        print("\n✅ API key is VALID and ACTIVE")
    else:
        print("\n❌ API key is INVALID or INACTIVE")


def migrate_keys():
    """Migrate legacy plaintext keys to hashed keys"""
    auth = AuthService()
    
    print_header("MIGRATE LEGACY KEYS")
    
    print("\n⚠️  WARNING: This will replace all legacy plaintext keys with new hashed keys!")
    print("⚠️  You will need to update all clients with the new keys!")
    print("\nCurrent keys:")
    list_keys()
    
    confirm = input("\nAre you sure you want to migrate? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("\n❌ Migration cancelled")
        return
    
    migrations = auth.migrate_legacy_keys()
    
    if migrations:
        print("\n✅ Migration completed!")
        print("\n" + "=" * 60)
        print("🔑 NEW KEYS - UPDATE YOUR CLIENTS!")
        print("=" * 60)
        
        for old_key, new_key in migrations.items():
            print(f"\nOld: {old_key}")
            print(f"New: {new_key}")
        
        print("\n⚠️  Save these new keys! Old keys are now invalid.")
        print("=" * 60)
    else:
        print("\n✅ No legacy keys to migrate")


def show_menu():
    """Show main menu"""
    print_header("SECURE API KEY MANAGEMENT")
    
    print("\n1. List all API keys")
    print("2. Add new API key")
    print("3. Deactivate API key")
    print("4. Validate API key")
    print("5. Migrate legacy keys to hashed")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    return choice


def main():
    """Main function"""
    while True:
        choice = show_menu()
        
        if choice == '1':
            list_keys()
        elif choice == '2':
            add_key()
        elif choice == '3':
            deactivate_key()
        elif choice == '4':
            validate_key()
        elif choice == '5':
            migrate_keys()
        elif choice == '6':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
