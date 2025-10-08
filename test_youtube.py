"""
Comprehensive Unit Testing for All API Features
Target: YouTube.com
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
API_BASE = "http://localhost:5000"
API_KEY = "demo-key-12345"
TARGET_URL = "https://youtube.com"
OUTPUT_DIR = "test_results_youtube"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Test results tracking
test_results = {
    'passed': 0,
    'failed': 0,
    'tests': []
}

def log_test(name, status, details=""):
    """Log test result"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    result = {
        'name': name,
        'status': status,
        'details': details,
        'timestamp': timestamp
    }
    test_results['tests'].append(result)
    
    if status == 'PASS':
        test_results['passed'] += 1
        print(f"[{timestamp}] [PASS] {name}")
    else:
        test_results['failed'] += 1
        print(f"[{timestamp}] [FAIL] {name}")
    
    if details:
        print(f"          {details}")

def save_screenshot(response, filename):
    """Save screenshot if successful"""
    if response.status_code == 200:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    return None

print("=" * 80)
print(f"  COMPREHENSIVE API TESTING - Target: {TARGET_URL}")
print("=" * 80)
print(f"Output Directory: {OUTPUT_DIR}")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# Test 1: Basic Screenshot
print("\n[TEST 1] Basic Screenshot")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "format": "png"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "01_basic.png")
        log_test("Basic Screenshot", "PASS", f"Size: {len(response.content)} bytes, Saved: {path}")
    else:
        log_test("Basic Screenshot", "FAIL", f"Status: {response.status_code}, {response.text[:100]}")
except Exception as e:
    log_test("Basic Screenshot", "FAIL", str(e))

time.sleep(1)

# Test 2: Custom Viewport Size
print("\n[TEST 2] Custom Viewport Size (1280x720)")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "width": 1280, "height": 720},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "02_custom_size.png")
        log_test("Custom Viewport", "PASS", f"1280x720, Saved: {path}")
    else:
        log_test("Custom Viewport", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Custom Viewport", "FAIL", str(e))

time.sleep(1)

# Test 3: Full Page Screenshot
print("\n[TEST 3] Full Page Screenshot")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "fullpage": "true"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "03_fullpage.png")
        log_test("Full Page", "PASS", f"Size: {len(response.content)} bytes, Saved: {path}")
    else:
        log_test("Full Page", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Full Page", "FAIL", str(e))

time.sleep(1)

# Test 4: With Delay
print("\n[TEST 4] Screenshot with 5-second Delay")
try:
    start = time.time()
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "delay": 5000},
        timeout=60
    )
    elapsed = time.time() - start
    if response.status_code == 200:
        path = save_screenshot(response, "04_delay_5s.png")
        log_test("Delay Feature", "PASS", f"Took {elapsed:.1f}s (expected >5s), Saved: {path}")
    else:
        log_test("Delay Feature", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Delay Feature", "FAIL", str(e))

time.sleep(1)

# Test 5: JPEG Format
print("\n[TEST 5] JPEG Format with Quality 90")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "format": "jpeg", "quality": 90},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "05_jpeg_q90.jpg")
        content_type = response.headers.get('Content-Type')
        log_test("JPEG Format", "PASS", f"Type: {content_type}, Saved: {path}")
    else:
        log_test("JPEG Format", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("JPEG Format", "FAIL", str(e))

time.sleep(1)

# Test 6: PDF Export
print("\n[TEST 6] PDF Export")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "format": "pdf"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "06_export.pdf")
        content_type = response.headers.get('Content-Type')
        log_test("PDF Export", "PASS", f"Type: {content_type}, Saved: {path}")
    else:
        log_test("PDF Export", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("PDF Export", "FAIL", str(e))

time.sleep(1)

# Test 7: Device Emulation - iPhone 13
print("\n[TEST 7] Device Emulation (iPhone 13)")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "device": "iphone13"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "07_iphone13.png")
        log_test("iPhone 13 Emulation", "PASS", f"Saved: {path}")
    else:
        log_test("iPhone 13 Emulation", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("iPhone 13 Emulation", "FAIL", str(e))

time.sleep(1)

# Test 8: Device Emulation - iPad Pro
print("\n[TEST 8] Device Emulation (iPad Pro)")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "device": "ipad_pro"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "08_ipad_pro.png")
        log_test("iPad Pro Emulation", "PASS", f"Saved: {path}")
    else:
        log_test("iPad Pro Emulation", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("iPad Pro Emulation", "FAIL", str(e))

time.sleep(1)

# Test 9: Dark Mode
print("\n[TEST 9] Dark Mode")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "dark_mode": "true"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "09_dark_mode.png")
        log_test("Dark Mode", "PASS", f"Saved: {path}")
    else:
        log_test("Dark Mode", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Dark Mode", "FAIL", str(e))

time.sleep(1)

# Test 10: Block Ads
print("\n[TEST 10] Block Ads and Trackers")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "block_ads": "true"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "10_block_ads.png")
        log_test("Block Ads", "PASS", f"Saved: {path}")
    else:
        log_test("Block Ads", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Block Ads", "FAIL", str(e))

time.sleep(1)

# Test 11: Scroll Page for Lazy Loading
print("\n[TEST 11] Scroll Page for Lazy Loading")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "scroll_page": "true", "fullpage": "true"},
        timeout=90
    )
    if response.status_code == 200:
        path = save_screenshot(response, "11_scroll_lazy.png")
        log_test("Scroll & Lazy Load", "PASS", f"Saved: {path}")
    else:
        log_test("Scroll & Lazy Load", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Scroll & Lazy Load", "FAIL", str(e))

time.sleep(1)

# Test 12: Element Selector
print("\n[TEST 12] Element-Specific Screenshot (logo)")
try:
    response = requests.post(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        json={"url": TARGET_URL, "selector": "#logo"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "12_element_logo.png")
        log_test("Element Selector", "PASS", f"Selector: #logo, Saved: {path}")
    else:
        log_test("Element Selector", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Element Selector", "FAIL", str(e))

time.sleep(1)

# Test 13: Custom JavaScript
print("\n[TEST 13] Custom JavaScript Execution")
try:
    response = requests.post(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        json={
            "url": TARGET_URL,
            "script": "document.body.style.backgroundColor='lightblue'"
        },
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "13_custom_js.png")
        log_test("Custom JavaScript", "PASS", f"Saved: {path}")
    else:
        log_test("Custom JavaScript", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Custom JavaScript", "FAIL", str(e))

time.sleep(1)

# Test 14: Wait for Selector
print("\n[TEST 14] Wait for Selector")
try:
    response = requests.post(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        json={"url": TARGET_URL, "wait_for_selector": "body"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "14_wait_selector.png")
        log_test("Wait for Selector", "PASS", f"Saved: {path}")
    else:
        log_test("Wait for Selector", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Wait for Selector", "FAIL", str(e))

time.sleep(1)

# Test 15: Print Media Type
print("\n[TEST 15] Print Media Emulation")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL, "media_type": "print"},
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "15_print_media.png")
        log_test("Print Media", "PASS", f"Saved: {path}")
    else:
        log_test("Print Media", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Print Media", "FAIL", str(e))

time.sleep(1)

# Test 16: Combined Features
print("\n[TEST 16] Combined Features (Mobile + Dark + Block Ads)")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={
            "url": TARGET_URL,
            "device": "iphone13",
            "dark_mode": "true",
            "block_ads": "true"
        },
        timeout=60
    )
    if response.status_code == 200:
        path = save_screenshot(response, "16_combined.png")
        log_test("Combined Features", "PASS", f"Saved: {path}")
    else:
        log_test("Combined Features", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Combined Features", "FAIL", str(e))

time.sleep(1)

# Test 17: Rate Limit Headers
print("\n[TEST 17] Rate Limit Headers")
try:
    response = requests.get(
        f"{API_BASE}/screenshot",
        headers={"X-API-Key": API_KEY},
        params={"url": TARGET_URL},
        timeout=60
    )
    minute = response.headers.get('X-RateLimit-Remaining-Minute', 'N/A')
    hour = response.headers.get('X-RateLimit-Remaining-Hour', 'N/A')
    if minute != 'N/A' or hour != 'N/A':
        log_test("Rate Limit Headers", "PASS", f"Minute: {minute}, Hour: {hour}")
    else:
        log_test("Rate Limit Headers", "FAIL", "Headers not found")
except Exception as e:
    log_test("Rate Limit Headers", "FAIL", str(e))

time.sleep(1)

# Test 18: Batch Processing
print("\n[TEST 18] Batch Processing (2 URLs)")
try:
    response = requests.post(
        f"{API_BASE}/batch",
        headers={"X-API-Key": API_KEY},
        json={
            "urls": [TARGET_URL, "https://example.com"],
            "settings": {"width": 800, "height": 600, "format": "png"}
        },
        timeout=120
    )
    if response.status_code == 200:
        result = response.json()
        log_test("Batch Processing", "PASS", f"Processed {result['total']} URLs")
    else:
        log_test("Batch Processing", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Batch Processing", "FAIL", str(e))

time.sleep(1)

# Test 19: Device List Endpoint
print("\n[TEST 19] Device List Endpoint")
try:
    response = requests.get(f"{API_BASE}/devices", timeout=10)
    if response.status_code == 200:
        devices = response.json()
        log_test("Device List", "PASS", f"Found {len(devices.get('devices', []))} devices")
    else:
        log_test("Device List", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Device List", "FAIL", str(e))

# Test 20: Health Check
print("\n[TEST 20] Health Check Endpoint")
try:
    response = requests.get(f"{API_BASE}/health", timeout=10)
    if response.status_code == 200:
        health = response.json()
        log_test("Health Check", "PASS", f"Status: {health.get('status')}")
    else:
        log_test("Health Check", "FAIL", f"Status: {response.status_code}")
except Exception as e:
    log_test("Health Check", "FAIL", str(e))

# Generate Report
print("\n" + "=" * 80)
print("  TEST SUMMARY")
print("=" * 80)
print(f"Total Tests: {test_results['passed'] + test_results['failed']}")
print(f"[PASS] Passed: {test_results['passed']}")
print(f"[FAIL] Failed: {test_results['failed']}")
print(f"Success Rate: {(test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100):.1f}%")
print("=" * 80)

# Save detailed report
report_file = os.path.join(OUTPUT_DIR, "test_report.json")
with open(report_file, 'w') as f:
    json.dump(test_results, f, indent=2)

print(f"\n[REPORT] Detailed report saved to: {report_file}")
print(f"[FILES] All screenshots saved to: {OUTPUT_DIR}/")
print(f"\n[DONE] Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
