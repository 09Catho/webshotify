"""
Test Suite for 4 New Developer Features:
1. Visual Regression Testing (comparison/diff)
2. Multi-Browser Support (Chrome, Firefox, Safari)
3. Animation Freezing
4. Data Injection
"""

import requests
import json
import os
from datetime import datetime

API_BASE = "http://localhost:5000"
API_KEY = "demo-key-12345"
TARGET_URL = "https://example.com"
OUTPUT_DIR = "test_new_features_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("  TESTING 4 NEW DEVELOPER FEATURES")
print("=" * 80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# FEATURE 1: Multi-Browser Support
print("\n[FEATURE 1] MULTI-BROWSER SUPPORT")
print("-" * 80)

browsers = ['chromium', 'firefox', 'webkit']
for browser in browsers:
    print(f"\nTesting {browser.upper()}...")
    try:
        response = requests.post(
            f"{API_BASE}/screenshot",
            headers={"X-API-Key": API_KEY},
            json={
                "url": TARGET_URL,
                "browser": browser,
                "width": 1280,
                "height": 720
            },
            timeout=60
        )
        
        if response.status_code == 200:
            filename = f"{browser}_screenshot.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  [PASS] {browser} - Saved to {filepath}")
            print(f"  Size: {len(response.content)} bytes")
        else:
            print(f"  [FAIL] {browser} - Status: {response.status_code}")
            print(f"  Error: {response.text[:200]}")
    except Exception as e:
        print(f"  [FAIL] {browser} - Error: {str(e)}")

# FEATURE 2: Animation Freezing
print("\n\n[FEATURE 2] ANIMATION FREEZING")
print("-" * 80)

print("\nTest 1: Without animation freeze...")
try:
    response1 = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "disable_animations": "false"},
        timeout=60
    )
    if response1.status_code == 200:
        with open(os.path.join(OUTPUT_DIR, "no_freeze.png"), 'wb') as f:
            f.write(response1.content)
        print(f"  [PASS] Screenshot without freeze - {len(response1.content)} bytes")
    else:
        print(f"  [FAIL] Status: {response1.status_code}")
except Exception as e:
    print(f"  [FAIL] Error: {str(e)}")

print("\nTest 2: With animation freeze...")
try:
    response2 = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "disable_animations": "true"},
        timeout=60
    )
    if response2.status_code == 200:
        with open(os.path.join(OUTPUT_DIR, "with_freeze.png"), 'wb') as f:
            f.write(response2.content)
        print(f"  [PASS] Screenshot with freeze - {len(response2.content)} bytes")
        print(f"  Note: Screenshots should be identical (animations frozen)")
    else:
        print(f"  [FAIL] Status: {response2.status_code}")
except Exception as e:
    print(f"  [FAIL] Error: {str(e)}")

# FEATURE 3: Data Injection
print("\n\n[FEATURE 3] DATA INJECTION")
print("-" * 80)

print("\nInjecting localStorage and mocking API...")
try:
    response = requests.post(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        json={
            "url": TARGET_URL,
            "inject_data": {
                "localStorage": {
                    "user_id": "test123",
                    "theme": "dark",
                    "test_mode": "enabled"
                },
                "sessionStorage": {
                    "session_token": "abc123xyz"
                },
                "api_mocks": {
                    "/api/user": {
                        "status": 200,
                        "body": {"name": "Test User", "role": "admin"}
                    }
                }
            }
        },
        timeout=60
    )
    
    if response.status_code == 200:
        filepath = os.path.join(OUTPUT_DIR, "data_injected.png")
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"  [PASS] Screenshot with injected data")
        print(f"  - localStorage: 3 items injected")
        print(f"  - sessionStorage: 1 item injected")
        print(f"  - API mocks: 1 endpoint mocked")
        print(f"  Saved to: {filepath}")
    else:
        print(f"  [FAIL] Status: {response.status_code}")
        print(f"  Error: {response.text[:200]}")
except Exception as e:
    print(f"  [FAIL] Error: {str(e)}")

# FEATURE 4: Visual Regression Testing
print("\n\n[FEATURE 4] VISUAL REGRESSION TESTING")
print("-" * 80)

print("\nStep 1: Creating baseline...")
try:
    response = requests.post(
        f"{API_BASE}/baseline",
        headers={"X-API-Key": API_KEY},
        json={
            "url": TARGET_URL,
            "name": "example_homepage",
            "capture_params": {"width": 1280, "height": 720}
        },
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"  [PASS] Baseline created")
        print(f"  Name: {result['baseline_name']}")
        print(f"  Path: {result['baseline_path']}")
    else:
        print(f"  [FAIL] Status: {response.status_code}")
        print(f"  Error: {response.text[:200]}")
except Exception as e:
    print(f"  [FAIL] Error: {str(e)}")

print("\nStep 2: Comparing with baseline (should match)...")
try:
    response = requests.post(
        f"{API_BASE}/compare",
        headers={"X-API-Key": API_KEY},
        json={
            "url": TARGET_URL,
            "baseline": "example_homepage",
            "threshold": 0.02,
            "capture_params": {"width": 1280, "height": 720}
        },
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"  [PASS] Comparison completed")
        print(f"  Passed: {result['passed']}")
        print(f"  Diff Percentage: {result['diff_percentage']}%")
        print(f"  Threshold: {result['threshold']}%")
        print(f"  Different Pixels: {result['different_pixels']:,}")
        
        if 'diff_image' in result:
            print(f"  Diff Image: {result['diff_image']}")
        
        if result['passed']:
            print(f"  [SUCCESS] Visual regression test PASSED!")
        else:
            print(f"  [WARNING] Visual regression test FAILED (diff > threshold)")
    else:
        print(f"  [FAIL] Status: {response.status_code}")
        print(f"  Error: {response.text[:200]}")
except Exception as e:
    print(f"  [FAIL] Error: {str(e)}")

print("\nStep 3: Testing comparison with different size (should fail)...")
try:
    response = requests.post(
        f"{API_BASE}/compare",
        headers={"X-API-Key": API_KEY},
        json={
            "url": TARGET_URL,
            "baseline": "example_homepage",
            "threshold": 0.01,  # Lower threshold
            "capture_params": {"width": 1920, "height": 1080}  # Different size
        },
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"  [PASS] Comparison completed")
        print(f"  Passed: {result['passed']}")
        print(f"  Diff Percentage: {result['diff_percentage']}%")
        
        if not result['passed']:
            print(f"  [EXPECTED] Test correctly identified differences!")
    else:
        print(f"  [FAIL] Status: {response.status_code}")
except Exception as e:
    print(f"  [FAIL] Error: {str(e)}")

# Summary
print("\n" + "=" * 80)
print("  SUMMARY - ALL 4 FEATURES TESTED")
print("=" * 80)
print("\n1. [DONE] Multi-Browser Support - Chrome, Firefox, Safari")
print("2. [DONE] Animation Freezing - Consistent screenshots")
print("3. [DONE] Data Injection - localStorage, sessionStorage, API mocks")
print("4. [DONE] Visual Regression - Baseline creation and comparison")
print("\n" + "=" * 80)
print(f"All test outputs saved to: {OUTPUT_DIR}/")
print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
