"""
API Key Management Script
Utility for managing API keys
"""

import sys
from auth_service import AuthService

def print_header():
    """Print script header"""
    print("\n" + "=" * 60)
    print("  API Key Management")
    print("=" * 60 + "\n")

def list_keys():
    """List all API keys"""
    auth = AuthService()
    print("\n📋 Current API Keys:\n")
    
    if not auth.api_keys:
        print("  No API keys found.")
        return
    
    for key, info in auth.api_keys.items():
        status = "✅ Active" if info.get('active', False) else "❌ Inactive"
        print(f"  {status}")
        print(f"    Key: {key}")
        print(f"    Name: {info.get('name', 'N/A')}")
        print(f"    Created: {info.get('created', 'N/A')}")
        print()

def generate_key():
    """Generate a new API key"""
    auth = AuthService()
    
    name = input("Enter name for this API key: ").strip()
    if not name:
        name = "Custom Key"
    
    prefix = input("Enter prefix (default: 'key'): ").strip()
    if not prefix:
        prefix = "key"
    
    new_key = auth.generate_api_key(prefix=prefix)
    success = auth.add_api_key(new_key, name=name)
    
    if success:
        print(f"\n✅ New API key created successfully!\n")
        print(f"  Key: {new_key}")
        print(f"  Name: {name}")
        print(f"\n⚠️  Save this key securely - it won't be shown again!")
    else:
        print("\n❌ Failed to create API key (key already exists)")

def add_custom_key():
    """Add a custom API key"""
    auth = AuthService()
    
    key = input("Enter the API key: ").strip()
    if not key:
        print("❌ API key cannot be empty")
        return
    
    name = input("Enter name for this API key: ").strip()
    if not name:
        name = "Custom Key"
    
    success = auth.add_api_key(key, name=name)
    
    if success:
        print(f"\n✅ API key added successfully!")
        print(f"  Key: {key}")
        print(f"  Name: {name}")
    else:
        print("\n❌ Failed to add API key (key already exists)")

def deactivate_key():
    """Deactivate an API key"""
    auth = AuthService()
    
    key = input("Enter the API key to deactivate: ").strip()
    if not key:
        print("❌ API key cannot be empty")
        return
    
    success = auth.deactivate_api_key(key)
    
    if success:
        print(f"\n✅ API key deactivated successfully!")
    else:
        print("\n❌ Failed to deactivate key (key not found)")

def show_menu():
    """Show main menu"""
    print("\nOptions:")
    print("  1. List all API keys")
    print("  2. Generate new API key")
    print("  3. Add custom API key")
    print("  4. Deactivate API key")
    print("  5. Exit")
    print()

def main():
    """Main function"""
    print_header()
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            list_keys()
        elif choice == '2':
            generate_key()
        elif choice == '3':
            add_custom_key()
        elif choice == '4':
            deactivate_key()
        elif choice == '5':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
