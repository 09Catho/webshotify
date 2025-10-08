"""
Test Script for Webpage Screenshot API
Demonstrates various API features and validates functionality
"""

import requests
import time
import os

# Configuration
API_BASE_URL = "http://localhost:5000"
API_KEY = "demo-key-12345"
OUTPUT_DIR = "test_outputs"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health_check():
    """Test the health endpoint"""
    print_section("Test 1: Health Check")
    
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print("✅ Health check passed!")

def test_missing_api_key():
    """Test request without API key"""
    print_section("Test 2: Missing API Key")
    
    response = requests.get(f"{API_BASE_URL}/screenshot?url=https://example.com")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401
    print("✅ Authentication validation passed!")

def test_invalid_api_key():
    """Test request with invalid API key"""
    print_section("Test 3: Invalid API Key")
    
    headers = {"X-API-Key": "invalid-key-xyz"}
    response = requests.get(f"{API_BASE_URL}/screenshot?url=https://example.com", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401
    print("✅ Invalid API key rejected!")

def test_missing_url():
    """Test request without URL parameter"""
    print_section("Test 4: Missing URL Parameter")
    
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{API_BASE_URL}/screenshot", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 400
    print("✅ Missing URL validation passed!")

def test_basic_screenshot():
    """Test basic screenshot capture"""
    print_section("Test 5: Basic Screenshot (PNG)")
    
    headers = {"X-API-Key": API_KEY}
    params = {
        "url": "https://example.com",
        "width": 1280,
        "height": 720
    }
    
    start_time = time.time()
    response = requests.get(f"{API_BASE_URL}/screenshot", headers=headers, params=params)
    elapsed = time.time() - start_time
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Content-Length: {len(response.content)} bytes")
    print(f"Time Taken: {elapsed:.2f} seconds")
    
    if response.status_code == 200:
        output_file = os.path.join(OUTPUT_DIR, "test_basic.png")
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✅ Screenshot saved to: {output_file}")
    else:
        print(f"❌ Error: {response.json()}")

def test_jpeg_screenshot():
    """Test JPEG screenshot with quality"""
    print_section("Test 6: JPEG Screenshot")
    
    headers = {"X-API-Key": API_KEY}
    params = {
        "url": "https://example.com",
        "format": "jpeg",
        "quality": 90
    }
    
    response = requests.get(f"{API_BASE_URL}/screenshot", headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Content-Length: {len(response.content)} bytes")
    
    if response.status_code == 200:
        output_file = os.path.join(OUTPUT_DIR, "test_jpeg.jpg")
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✅ JPEG screenshot saved to: {output_file}")

def test_fullpage_screenshot():
    """Test full page screenshot"""
    print_section("Test 7: Full Page Screenshot")
    
    headers = {"X-API-Key": API_KEY}
    params = {
        "url": "https://example.com",
        "fullpage": "true",
        "width": 1920,
        "height": 1080
    }
    
    response = requests.get(f"{API_BASE_URL}/screenshot", headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        output_file = os.path.join(OUTPUT_DIR, "test_fullpage.png")
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✅ Full page screenshot saved to: {output_file}")

def test_post_request():
    """Test POST request with JSON body"""
    print_section("Test 8: POST Request with JSON")
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "url": "https://example.com",
        "width": 800,
        "height": 600,
        "format": "png"
    }
    
    response = requests.post(f"{API_BASE_URL}/screenshot", headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        output_file = os.path.join(OUTPUT_DIR, "test_post.png")
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✅ POST request screenshot saved to: {output_file}")

def test_caching():
    """Test caching functionality"""
    print_section("Test 9: Caching Performance")
    
    headers = {"X-API-Key": API_KEY}
    params = {
        "url": "https://example.com",
        "width": 1024,
        "height": 768
    }
    
    # First request (should capture)
    print("Making first request (will capture screenshot)...")
    start_time = time.time()
    response1 = requests.get(f"{API_BASE_URL}/screenshot", headers=headers, params=params)
    time1 = time.time() - start_time
    print(f"First request time: {time1:.2f} seconds")
    
    # Second request (should use cache)
    print("Making second request (should use cache)...")
    start_time = time.time()
    response2 = requests.get(f"{API_BASE_URL}/screenshot", headers=headers, params=params)
    time2 = time.time() - start_time
    print(f"Second request time: {time2:.2f} seconds")
    
    if time2 < time1:
        speedup = time1 / time2
        print(f"✅ Cache speedup: {speedup:.2f}x faster!")
    else:
        print("⚠️  Cache may not be working optimally")

def test_rate_limiting():
    """Test rate limiting"""
    print_section("Test 10: Rate Limiting")
    
    headers = {"X-API-Key": API_KEY}
    params = {"url": "https://example.com"}
    
    print("Sending 12 rapid requests to test rate limiting...")
    success_count = 0
    rate_limited = False
    
    for i in range(12):
        response = requests.get(f"{API_BASE_URL}/screenshot", headers=headers, params=params)
        if response.status_code == 200:
            success_count += 1
            print(f"Request {i+1}: ✅ Success")
        elif response.status_code == 429:
            rate_limited = True
            print(f"Request {i+1}: ⚠️  Rate limited")
            retry_after = response.json().get('retry_after')
            print(f"  Retry after: {retry_after} seconds")
            break
        else:
            print(f"Request {i+1}: ❌ Error {response.status_code}")
        
        time.sleep(0.1)  # Small delay between requests
    
    if rate_limited:
        print(f"✅ Rate limiting working! {success_count} requests succeeded before limit")
    else:
        print(f"⚠️  All {success_count} requests succeeded (rate limit not triggered)")

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Webpage Screenshot API Test Suite" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        test_health_check()
        test_missing_api_key()
        test_invalid_api_key()
        test_missing_url()
        test_basic_screenshot()
        test_jpeg_screenshot()
        test_fullpage_screenshot()
        test_post_request()
        test_caching()
        test_rate_limiting()
        
        print_section("🎉 All Tests Completed!")
        print(f"\nScreenshots saved to: {os.path.abspath(OUTPUT_DIR)}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server!")
        print("Make sure the API is running at http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
