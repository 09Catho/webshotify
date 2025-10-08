#!/usr/bin/env python3
"""
Test Device Emulation Feature
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
API_KEY = "demo-key-12345"

def test_device_emulation():
    """Test device emulation with different presets"""
    
    devices = [
        'iphone13',
        'iphone13_pro',
        'ipad_pro',
        'samsung_galaxy',
        'pixel_5',
        'desktop_1080p',
        'desktop_4k'
    ]
    
    test_url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"
    
    print("=" * 60)
    print("DEVICE EMULATION TEST")
    print("=" * 60)
    print()
    
    for device in devices:
        print(f"Testing device: {device}")
        
        # Test with GET request
        response = requests.get(
            f"{BASE_URL}/screenshot",
            params={
                'url': test_url,
                'device': device,
                'api_key': API_KEY
            }
        )
        
        if response.status_code == 200:
            filename = f"test_device_{device}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Screenshot saved: {filename}")
            print(f"  Size: {len(response.content)} bytes")
        else:
            print(f"  ❌ Error: {response.status_code}")
            print(f"  {response.text}")
        
        print()
    
    print("=" * 60)
    print("Test complete! Check the generated screenshots.")
    print("=" * 60)

def test_device_vs_manual():
    """Compare device preset vs manual viewport"""
    
    print("\n" + "=" * 60)
    print("DEVICE PRESET VS MANUAL VIEWPORT")
    print("=" * 60)
    print()
    
    test_url = "https://www.whatismybrowser.com/detect/what-is-my-viewport-size"
    
    # Test 1: Using device preset
    print("Test 1: Using device='iphone13'")
    response1 = requests.get(
        f"{BASE_URL}/screenshot",
        params={
            'url': test_url,
            'device': 'iphone13',
            'api_key': API_KEY
        }
    )
    
    if response1.status_code == 200:
        with open('test_iphone13_preset.png', 'wb') as f:
            f.write(response1.content)
        print("  ✅ Screenshot saved: test_iphone13_preset.png")
        print(f"  Expected: 390x844")
    
    print()
    
    # Test 2: Manual viewport (same dimensions as iPhone 13)
    print("Test 2: Using width=390, height=844 (manual)")
    response2 = requests.get(
        f"{BASE_URL}/screenshot",
        params={
            'url': test_url,
            'width': 390,
            'height': 844,
            'api_key': API_KEY
        }
    )
    
    if response2.status_code == 200:
        with open('test_iphone13_manual.png', 'wb') as f:
            f.write(response2.content)
        print("  ✅ Screenshot saved: test_iphone13_manual.png")
        print(f"  Expected: 390x844")
    
    print()
    print("Compare the two screenshots:")
    print("  - test_iphone13_preset.png (should show mobile user agent)")
    print("  - test_iphone13_manual.png (should show desktop user agent)")
    print()

if __name__ == '__main__':
    test_device_emulation()
    test_device_vs_manual()
