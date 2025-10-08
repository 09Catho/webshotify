"""
Test script for advanced features
"""
import requests
import json

API_BASE = "http://localhost:5000"
API_KEY = "demo-key-12345"

print("=" * 60)
print("  Testing Advanced Screenshot API Features")
print("=" * 60)

# Test 1: Device Emulation
print("\n1. Testing iPhone 13 emulation...")
response = requests.get(
    f"{API_BASE}/screenshot",
    headers={"X-API-Key": API_KEY},
    params={
        "url": "https://example.com",
        "device": "iphone13",
        "format": "png"
    }
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    with open("test_iphone13.png", "wb") as f:
        f.write(response.content)
    print(f"   ✓ Saved as test_iphone13.png")

# Test 2: Dark Mode
print("\n2. Testing dark mode...")
response = requests.get(
    f"{API_BASE}/screenshot",
    headers={"X-API-Key": API_KEY},
    params={
        "url": "https://example.com",
        "dark_mode": "true",
        "format": "png"
    }
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    with open("test_darkmode.png", "wb") as f:
        f.write(response.content)
    print(f"   ✓ Saved as test_darkmode.png")

# Test 3: Element-specific screenshot
print("\n3. Testing element selector...")
response = requests.post(
    f"{API_BASE}/screenshot",
    headers={"X-API-Key": API_KEY},
    json={
        "url": "https://example.com",
        "selector": "h1",
        "format": "png"
    }
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    with open("test_element.png", "wb") as f:
        f.write(response.content)
    print(f"   ✓ Saved as test_element.png")

# Test 4: Custom JavaScript
print("\n4. Testing custom JavaScript execution...")
response = requests.post(
    f"{API_BASE}/screenshot",
    headers={"X-API-Key": API_KEY},
    json={
        "url": "https://example.com",
        "script": "document.body.style.backgroundColor='lightblue'",
        "format": "png"
    }
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    with open("test_custom_js.png", "wb") as f:
        f.write(response.content)
    print(f"   ✓ Saved as test_custom_js.png")

# Test 5: PDF Export
print("\n5. Testing PDF export...")
response = requests.get(
    f"{API_BASE}/screenshot",
    headers={"X-API-Key": API_KEY},
    params={
        "url": "https://example.com",
        "format": "pdf"
    }
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    with open("test_export.pdf", "wb") as f:
        f.write(response.content)
    print(f"   ✓ Saved as test_export.pdf")

# Test 6: Batch Processing
print("\n6. Testing batch processing...")
response = requests.post(
    f"{API_BASE}/batch",
    headers={"X-API-Key": API_KEY},
    json={
        "urls": [
            "https://example.com",
            "https://example.org"
        ],
        "settings": {
            "width": 800,
            "height": 600,
            "format": "png"
        }
    }
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"   ✓ Processed {result['total']} URLs")
    for r in result['results']:
        print(f"     - {r['url']}: {r['status']}")

# Test 7: Device List
print("\n7. Fetching available devices...")
response = requests.get(f"{API_BASE}/devices")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    devices = response.json()
    print(f"   ✓ Available devices: {', '.join(devices['devices'])}")

# Test 8: Rate Limit Headers
print("\n8. Checking rate limit headers...")
response = requests.get(
    f"{API_BASE}/screenshot",
    headers={"X-API-Key": API_KEY},
    params={"url": "https://example.com"}
)
if response.status_code == 200:
    print(f"   ✓ Remaining this minute: {response.headers.get('X-RateLimit-Remaining-Minute', 'N/A')}")
    print(f"   ✓ Remaining this hour: {response.headers.get('X-RateLimit-Remaining-Hour', 'N/A')}")

print("\n" + "=" * 60)
print("  Advanced Features Test Complete!")
print("=" * 60)
print("\nAll test files saved to current directory.")
print("Check out ADVANCED_FEATURES.md for complete documentation!")
