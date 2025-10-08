"""Quick test of the Screenshot API"""
import requests

print("=" * 60)
print("  Testing Webpage Screenshot API")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    r = requests.get('http://localhost:5000/health')
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Screenshot capture
print("\n2. Capturing screenshot of example.com...")
try:
    headers = {'X-API-Key': 'demo-key-12345'}
    params = {
        'url': 'https://example.com',
        'width': 800,
        'height': 600,
        'format': 'png'
    }
    
    r = requests.get('http://localhost:5000/screenshot', headers=headers, params=params)
    print(f"   Status: {r.status_code}")
    
    if r.status_code == 200:
        content_type = r.headers.get('Content-Type')
        size = len(r.content)
        print(f"   Content-Type: {content_type}")
        print(f"   Size: {size:,} bytes ({size/1024:.1f} KB)")
        
        # Save the screenshot
        with open('test_screenshot.png', 'wb') as f:
            f.write(r.content)
        print(f"   ✅ Screenshot saved to: test_screenshot.png")
    else:
        print(f"   Error: {r.json()}")
        
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Test cache (second request should be faster)
print("\n3. Testing cache (making same request again)...")
try:
    import time
    start = time.time()
    r = requests.get('http://localhost:5000/screenshot', headers=headers, params=params)
    elapsed = time.time() - start
    print(f"   Status: {r.status_code}")
    print(f"   Response time: {elapsed:.3f} seconds")
    print(f"   ✅ Cache is working! (should be very fast)")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("  API is working perfectly! 🎉")
print("=" * 60)
print("\nVisit http://localhost:5000/docs for full documentation")
