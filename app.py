"""
Webpage Screenshot API
A REST API service for capturing webpage screenshots with caching, authentication, and rate limiting.
"""

from flask import Flask, request, jsonify, send_file, render_template, render_template_string
from functools import wraps
from datetime import datetime, timedelta
import hashlib
import json
import os
import time
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

from screenshot_service import ScreenshotService
from auth_service import AuthService
from rate_limiter import RateLimiter
from cache_service import CacheService
from comparison_service import ComparisonService
from webhook_service import WebhookService
from dashboard_service import DashboardService

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
app.config['START_TIME'] = time.time()  # Track startup time for uptime calculation

# Initialize services
screenshot_service = ScreenshotService()
auth_service = AuthService()
rate_limiter = RateLimiter()
cache_service = CacheService()
comparison_service = ComparisonService()
webhook_service = WebhookService()
dashboard_service = DashboardService()

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/api_requests.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(api_key)s] - %(url)s - %(status)s - %(message)s'
))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            log_request(None, None, 401, "Missing API key")
            return jsonify({
                'error': 'API key is required',
                'message': 'Please provide an API key using X-API-Key header or api_key parameter'
            }), 401
        
        if not auth_service.validate_api_key(api_key):
            log_request(api_key, None, 401, "Invalid API key")
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 401
        
        # Check rate limit
        if not rate_limiter.check_rate_limit(api_key):
            log_request(api_key, None, 429, "Rate limit exceeded")
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'You have exceeded your rate limit. Please try again later.',
                'retry_after': rate_limiter.get_retry_after(api_key)
            }), 429
        
        return f(*args, **kwargs)
    
    return decorated_function


def log_request(api_key, url, status, message=""):
    """Log API request details"""
    extra = {
        'api_key': api_key or 'N/A',
        'url': url or 'N/A',
        'status': status
    }
    app.logger.info(message, extra=extra)


@app.route('/')
def home():
    """
    Landing page - Beautiful homepage with live demo
    """
    return render_template('landing.html')


@app.route('/api')
def api_info():
    """
    API information endpoint (JSON)
    """
    return jsonify({
        'name': 'Webpage Screenshot API',
        'version': '1.0',
        'status': 'operational',
        'endpoints': [
            '/screenshot (GET/POST) - Capture screenshot',
            '/screenshot/async (POST) - Async screenshot with webhook',
            '/jobs/{id} (GET) - Check job status',
            '/batch (POST) - Batch screenshot processing',
            '/compare (POST) - Compare screenshots',
            '/baseline (POST) - Create baseline screenshot',
            '/devices (GET) - List device presets',
            '/dashboard (GET) - Usage dashboard',
            '/health (GET) - API health check',
            '/docs (GET) - API documentation'
        ],
        'documentation': '/docs',
        'dashboard': '/dashboard',
        'github': 'https://github.com/your-repo'
    })


@app.route('/screenshot', methods=['GET', 'POST'])
@require_api_key
def screenshot():
    """
    Capture screenshot of a webpage with advanced features
    
    Parameters:
        url (str, required): URL of the webpage to capture
        width (int, optional): Viewport width (default: 1920)
        height (int, optional): Viewport height (default: 1080)
        fullpage (bool, optional): Capture full page (default: false)
        delay (int, optional): Delay before capture in milliseconds (default: 0)
        format (str, optional): Image format - 'png', 'jpeg', or 'pdf' (default: 'png')
        quality (int, optional): JPEG quality 1-100 (default: 80)
        selector (str, optional): CSS selector to capture specific element
        device (str, optional): Device preset (iphone13, ipad_pro, etc.)
        user_agent (str, optional): Custom user agent string
        dark_mode (bool, optional): Emulate dark mode (default: false)
        wait_for_selector (str, optional): Wait for element before capture
        script (str, optional): JavaScript to execute before capture
        block_ads (bool, optional): Block ads and trackers (default: false)
        scroll_page (bool, optional): Scroll page for lazy loading (default: false)
        media_type (str, optional): Emulate media type ('screen' or 'print')
    
    Returns:
        Image file, PDF, or error message
    """
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    # Get parameters
    if request.method == 'POST':
        data = request.get_json() or {}
        url = data.get('url') or request.form.get('url')
        width = data.get('width', 1920)
        height = data.get('height', 1080)
        fullpage = data.get('fullpage', False)
        delay = data.get('delay', 0)
        image_format = data.get('format', 'png').lower()
        quality = data.get('quality', 80)
        selector = data.get('selector')
        device = data.get('device')
        user_agent = data.get('user_agent')
        dark_mode = data.get('dark_mode', False)
        wait_for_selector = data.get('wait_for_selector')
        custom_script = data.get('script')
        block_ads = data.get('block_ads', False)
        scroll_page = data.get('scroll_page', False)
        media_type = data.get('media_type')
        extra_headers = data.get('headers')
        cookies = data.get('cookies')
        geolocation = data.get('geolocation')
        timezone = data.get('timezone')
        browser_type = data.get('browser', 'chromium')
        disable_animations = data.get('disable_animations', False)
        inject_data = data.get('inject_data')
    else:
        url = request.args.get('url')
        width = int(request.args.get('width', 1920))
        height = int(request.args.get('height', 1080))
        fullpage = request.args.get('fullpage', 'false').lower() in ('true', '1', 'yes')
        delay = int(request.args.get('delay', 0))
        image_format = request.args.get('format', 'png').lower()
        quality = int(request.args.get('quality', 80))
        selector = request.args.get('selector')
        device = request.args.get('device')
        user_agent = request.args.get('user_agent')
        dark_mode = request.args.get('dark_mode', 'false').lower() in ('true', '1', 'yes')
        wait_for_selector = request.args.get('wait_for_selector')
        custom_script = request.args.get('script')
        block_ads = request.args.get('block_ads', 'false').lower() in ('true', '1', 'yes')
        scroll_page = request.args.get('scroll_page', 'false').lower() in ('true', '1', 'yes')
        media_type = request.args.get('media_type')
        extra_headers = None
        cookies = None
        geolocation = None
        timezone = request.args.get('timezone')
        browser_type = request.args.get('browser', 'chromium')
        disable_animations = request.args.get('disable_animations', 'false').lower() in ('true', '1', 'yes')
        inject_data = None  # Only available via POST
    
    # Validate URL
    if not url:
        log_request(api_key, None, 400, "Missing URL parameter")
        return jsonify({
            'error': 'Missing required parameter',
            'message': 'URL parameter is required'
        }), 400
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        log_request(api_key, url, 400, "Invalid URL format")
        return jsonify({
            'error': 'Invalid URL',
            'message': 'URL must start with http:// or https://'
        }), 400
    
    # Validate image format
    if image_format not in ['png', 'jpeg', 'jpg', 'pdf']:
        log_request(api_key, url, 400, "Invalid image format")
        return jsonify({
            'error': 'Invalid format',
            'message': 'Format must be "png", "jpeg", or "pdf"'
        }), 400
    
    # Normalize jpeg format
    if image_format == 'jpg':
        image_format = 'jpeg'
    
    # Validate viewport dimensions
    if width < 100 or width > 3840 or height < 100 or height > 2160:
        log_request(api_key, url, 400, "Invalid viewport dimensions")
        return jsonify({
            'error': 'Invalid viewport dimensions',
            'message': 'Width must be between 100-3840 and height between 100-2160'
        }), 400
    
    # Validate quality
    if quality < 1 or quality > 100:
        log_request(api_key, url, 400, "Invalid quality")
        return jsonify({
            'error': 'Invalid quality',
            'message': 'Quality must be between 1-100'
        }), 400
    
    # Generate cache key (include all relevant parameters)
    cache_params = f"{selector}|{device}|{user_agent}|{dark_mode}|{wait_for_selector}|{block_ads}|{scroll_page}|{media_type}|{timezone}"
    cache_key = cache_service.generate_cache_key(url, width, height, fullpage, image_format, quality, delay)
    # Extend cache key with advanced params
    import hashlib
    cache_key = hashlib.sha256(f"{cache_key}|{cache_params}".encode()).hexdigest()
    
    cached_file = cache_service.get_cached_screenshot(cache_key)
    
    if cached_file:
        log_request(api_key, url, 200, "Screenshot served from cache")
        if image_format == 'pdf':
            mimetype = 'application/pdf'
        elif image_format == 'jpeg':
            mimetype = 'image/jpeg'
        else:
            mimetype = 'image/png'
        return send_file(cached_file, mimetype=mimetype, as_attachment=False)
    
    # Capture screenshot or PDF
    try:
        if image_format == 'pdf':
            # PDF export
            screenshot_path = screenshot_service.capture_pdf(
                url=url,
                width=width,
                height=height,
                landscape=fullpage,
                extra_headers=extra_headers
            )
        else:
            # Image screenshot
            screenshot_path = screenshot_service.capture_screenshot(
                url=url,
                width=width,
                height=height,
                fullpage=fullpage,
                delay=delay,
                image_format=image_format,
                quality=quality,
                selector=selector,
                device=device,
                user_agent=user_agent,
                dark_mode=dark_mode,
                wait_for_selector=wait_for_selector,
                custom_script=custom_script,
                block_ads=block_ads,
                scroll_page=scroll_page,
                media_type=media_type,
                extra_headers=extra_headers,
                cookies=cookies,
                geolocation=geolocation,
                timezone=timezone,
                browser_type=browser_type,
                disable_animations=disable_animations,
                inject_data=inject_data
            )
        
        # Cache the screenshot
        cache_service.cache_screenshot(cache_key, screenshot_path)
        
        log_request(api_key, url, 200, "Screenshot captured successfully")
        
        if image_format == 'pdf':
            mimetype = 'application/pdf'
        elif image_format == 'jpeg':
            mimetype = 'image/jpeg'
        else:
            mimetype = 'image/png'
        
        # Add rate limit headers
        response = send_file(screenshot_path, mimetype=mimetype, as_attachment=False)
        remaining = rate_limiter.get_remaining_requests(api_key)
        response.headers['X-RateLimit-Remaining-Minute'] = str(remaining['per_minute'])
        response.headers['X-RateLimit-Remaining-Hour'] = str(remaining['per_hour'])
        return response
        
    except Exception as e:
        log_request(api_key, url, 500, f"Error: {str(e)}")
        return jsonify({
            'error': 'Screenshot capture failed',
            'message': str(e)
        }), 500


@app.route('/compare', methods=['POST'])
@require_api_key
def compare_screenshots():
    """
    Compare two screenshots for visual regression testing
    
    POST Body:
    Option 1 - Compare two existing images:
    {
        "baseline": "path/to/baseline.png",
        "current": "path/to/current.png",
        "threshold": 0.02
    }
    
    Option 2 - Capture and compare with baseline:
    {
        "url": "https://example.com",
        "baseline": "baseline_name",
        "capture_params": {...}
    }
    """
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    data = request.get_json() or {}
    
    try:
        # Option 1: Compare two existing images
        if 'baseline' in data and 'current' in data and 'url' not in data:
            baseline_path = data['baseline']
            current_path = data['current']
            threshold = data.get('threshold', 0.02)
            
            result = comparison_service.compare_images(
                baseline_path,
                current_path,
                threshold=threshold
            )
            
            log_request(api_key, "Comparison", 200, "Images compared")
            return jsonify(result)
        
        # Option 2: Capture new screenshot and compare
        elif 'url' in data and 'baseline' in data:
            url = data['url']
            baseline_name = data['baseline']
            capture_params = data.get('capture_params', {})
            threshold = data.get('threshold', 0.02)
            
            # Get baseline
            baseline_path = comparison_service.get_baseline(baseline_name)
            if not baseline_path:
                log_request(api_key, url, 404, "Baseline not found")
                return jsonify({
                    'error': 'Baseline not found',
                    'message': f'No baseline named "{baseline_name}" exists'
                }), 404
            
            # Capture new screenshot
            screenshot_path = screenshot_service.capture_screenshot(
                url=url,
                **capture_params
            )
            
            # Compare
            result = comparison_service.compare_images(
                baseline_path,
                screenshot_path,
                threshold=threshold
            )
            result['current_screenshot'] = screenshot_path
            result['baseline_screenshot'] = baseline_path
            
            log_request(api_key, url, 200, f"Comparison: {result['diff_percentage']}% diff")
            return jsonify(result)
        
        else:
            log_request(api_key, None, 400, "Invalid comparison request")
            return jsonify({
                'error': 'Invalid request',
                'message': 'Provide either (baseline + current) or (url + baseline)'
            }), 400
            
    except Exception as e:
        log_request(api_key, None, 500, f"Comparison error: {str(e)}")
        return jsonify({
            'error': 'Comparison failed',
            'message': str(e)
        }), 500


@app.route('/baseline', methods=['POST'])
@require_api_key
def create_baseline():
    """
    Create a baseline screenshot for future comparisons
    
    POST Body:
    {
        "url": "https://example.com",
        "name": "homepage_baseline",
        "capture_params": {...}
    }
    """
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    data = request.get_json() or {}
    url = data.get('url')
    baseline_name = data.get('name')
    capture_params = data.get('capture_params', {})
    
    if not url or not baseline_name:
        log_request(api_key, None, 400, "Missing url or name")
        return jsonify({
            'error': 'Missing required parameters',
            'message': 'Both url and name are required'
        }), 400
    
    try:
        # Capture screenshot
        screenshot_path = screenshot_service.capture_screenshot(url=url, **capture_params)
        
        # Save as baseline
        baseline_path = comparison_service.create_baseline(screenshot_path, baseline_name)
        
        log_request(api_key, url, 200, f"Baseline created: {baseline_name}")
        return jsonify({
            'success': True,
            'baseline_name': baseline_name,
            'baseline_path': baseline_path,
            'screenshot_path': screenshot_path
        })
        
    except Exception as e:
        log_request(api_key, url, 500, f"Baseline error: {str(e)}")
        return jsonify({
            'error': 'Baseline creation failed',
            'message': str(e)
        }), 500


@app.route('/screenshot/async', methods=['POST'])
@require_api_key
def screenshot_async():
    """
    Async screenshot capture with webhook notification
    
    POST Body:
    {
        "url": "https://example.com",
        "webhook_url": "https://yourapp.com/callback",
        "webhook_secret": "your-secret",
        "params": {...}
    }
    """
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    data = request.get_json() or {}
    url = data.get('url')
    webhook_url = data.get('webhook_url')
    webhook_secret = data.get('webhook_secret')
    params = data.get('params', {})
    
    if not url:
        return jsonify({
            'error': 'Missing URL',
            'message': 'URL parameter is required'
        }), 400
    
    try:
        # Create async job
        job_id = webhook_service.create_job(
            job_type='screenshot',
            params={'url': url, **params},
            webhook_url=webhook_url,
            webhook_secret=webhook_secret
        )
        
        # Process job asynchronously
        webhook_service.process_job_async(
            job_id,
            screenshot_service.capture_screenshot,
            url=url,
            **params
        )
        
        log_request(api_key, url, 202, f"Async job created: {job_id}")
        
        return jsonify({
            'job_id': job_id,
            'status': 'pending',
            'message': 'Job created successfully',
            'status_url': f'/jobs/{job_id}'
        }), 202
        
    except Exception as e:
        log_request(api_key, url, 500, f"Async job error: {str(e)}")
        return jsonify({
            'error': 'Failed to create async job',
            'message': str(e)
        }), 500


@app.route('/jobs/<job_id>', methods=['GET'])
@require_api_key
def get_job_status(job_id):
    """
    Get status of async job
    
    Returns:
    {
        "job_id": "...",
        "status": "pending|processing|completed|failed",
        "result": {...}
    }
    """
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    try:
        status = webhook_service.get_job_status(job_id)
        
        if not status:
            log_request(api_key, f"Job: {job_id}", 404, "Job not found")
            return jsonify({
                'error': 'Job not found',
                'message': f'No job with ID {job_id}'
            }), 404
        
        log_request(api_key, f"Job: {job_id}", 200, f"Status: {status['status']}")
        return jsonify(status)
        
    except Exception as e:
        log_request(api_key, f"Job: {job_id}", 500, f"Error: {str(e)}")
        return jsonify({
            'error': 'Failed to get job status',
            'message': str(e)
        }), 500


@app.route('/batch', methods=['POST'])
@require_api_key
def batch_screenshot():
    """
    Capture multiple screenshots in one request
    
    POST Body:
    {
        "urls": ["url1", "url2", "url3"],
        "settings": {"width": 1280, "height": 720, "format": "png"}
    }
    """
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    data = request.get_json() or {}
    urls = data.get('urls', [])
    settings = data.get('settings', {})
    
    if not urls or not isinstance(urls, list):
        log_request(api_key, None, 400, "Invalid batch request")
        return jsonify({
            'error': 'Invalid request',
            'message': 'urls must be a non-empty array'
        }), 400
    
    if len(urls) > 10:
        log_request(api_key, None, 400, "Too many URLs in batch")
        return jsonify({
            'error': 'Too many URLs',
            'message': 'Maximum 10 URLs per batch request'
        }), 400
    
    results = []
    
    for url in urls:
        try:
            # Merge settings with defaults
            params = {
                'url': url,
                'width': settings.get('width', 1920),
                'height': settings.get('height', 1080),
                'fullpage': settings.get('fullpage', False),
                'delay': settings.get('delay', 0),
                'image_format': settings.get('format', 'png'),
                'quality': settings.get('quality', 80),
                'selector': settings.get('selector'),
                'device': settings.get('device'),
                'dark_mode': settings.get('dark_mode', False),
            }
            
            screenshot_path = screenshot_service.capture_screenshot(**params)
            
            # Return base64 encoded image for batch
            import base64
            with open(screenshot_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            results.append({
                'url': url,
                'status': 'success',
                'data': f"data:image/{params['image_format']};base64,{image_data}"
            })
            
        except Exception as e:
            results.append({
                'url': url,
                'status': 'error',
                'message': str(e)
            })
    
    log_request(api_key, f"Batch: {len(urls)} URLs", 200, "Batch processing completed")
    
    return jsonify({
        'total': len(urls),
        'results': results
    })


@app.route('/dashboard')
def dashboard():
    """
    Usage Dashboard - Web UI for API management
    """
    try:
        # Get overall statistics
        stats = dashboard_service.get_api_usage_stats(days=30)
        
        # Get API key statistics
        api_keys = dashboard_service.get_api_key_stats(auth_service)
        
        # Get recent requests
        recent_requests = dashboard_service.get_recent_requests(limit=50)
        
        # Get system health
        health = dashboard_service.get_system_health()
        
        return render_template(
            'dashboard.html',
            stats=stats,
            api_keys=api_keys,
            recent_requests=recent_requests,
            health=health
        )
    except Exception as e:
        return jsonify({
            'error': 'Dashboard error',
            'message': str(e)
        }), 500


@app.route('/devices')
def devices():
    """
    List available device presets
    """
    return jsonify({
        'devices': list(screenshot_service.DEVICE_PRESETS.keys())
    })


@app.route('/health')
def health():
    """
    Health check endpoint
    
    Returns API health status, uptime, and system metrics
    """
    import psutil
    from datetime import datetime
    
    # Calculate uptime (approximate - since app start)
    uptime_seconds = int(time.time() - app.config.get('START_TIME', time.time()))
    
    # Get system metrics
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        system_metrics = {
            'cpu_usage_percent': round(cpu_percent, 2),
            'memory_usage_percent': round(memory.percent, 2),
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_usage_percent': round(disk.percent, 2),
            'disk_free_gb': round(disk.free / (1024**3), 2)
        }
    except Exception:
        system_metrics = {
            'cpu_usage_percent': 0,
            'memory_usage_percent': 0,
            'memory_available_gb': 0,
            'disk_usage_percent': 0,
            'disk_free_gb': 0
        }
    
    # Check service health
    services_healthy = True
    service_status = {}
    
    try:
        # Test screenshot service
        service_status['screenshot_service'] = 'healthy' if screenshot_service else 'unavailable'
    except Exception:
        service_status['screenshot_service'] = 'error'
        services_healthy = False
    
    try:
        # Test auth service
        service_status['auth_service'] = 'healthy' if auth_service else 'unavailable'
    except Exception:
        service_status['auth_service'] = 'error'
        services_healthy = False
    
    try:
        # Test cache service
        service_status['cache_service'] = 'healthy' if cache_service else 'unavailable'
    except Exception:
        service_status['cache_service'] = 'error'
        services_healthy = False
    
    # Overall status
    overall_status = 'healthy' if services_healthy else 'degraded'
    
    response = {
        'status': overall_status,
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': uptime_seconds,
        'uptime_human': f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s",
        'version': '1.0.0',
        'services': service_status,
        'system': system_metrics
    }
    
    status_code = 200 if overall_status == 'healthy' else 503
    return jsonify(response), status_code


@app.route('/docs')
def docs():
    """API documentation endpoint"""
    doc_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Webpage Screenshot API - Documentation</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            h3 { color: #7f8c8d; }
            code {
                background: #ecf0f1;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            pre {
                background: #2c3e50;
                color: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .endpoint {
                background: #e8f4f8;
                padding: 15px;
                margin: 15px 0;
                border-left: 4px solid #3498db;
                border-radius: 4px;
            }
            .method {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #3498db; color: white; }
            .post { background: #2ecc71; color: white; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #34495e;
                color: white;
            }
            .warning {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 15px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📸 Webpage Screenshot API Documentation</h1>
            <p>A powerful REST API for capturing webpage screenshots with advanced features including caching, authentication, and rate limiting.</p>
            
            <h2>🔑 Authentication</h2>
            <p>All requests require API key authentication. Provide your API key in one of two ways:</p>
            <ul>
                <li>Header: <code>X-API-Key: your_api_key_here</code></li>
                <li>Query parameter: <code>?api_key=your_api_key_here</code></li>
            </ul>
            
            <div class="warning">
                <strong>⚠️ Note:</strong> For security, use the header method in production environments.
            </div>
            
            <h2>📊 Rate Limiting</h2>
            <p>Each API key is limited to:</p>
            <ul>
                <li><strong>60 requests per hour</strong></li>
                <li><strong>10 requests per minute</strong></li>
            </ul>
            <p>When rate limit is exceeded, you'll receive a 429 status code with retry-after information.</p>
            
            <h2>🛠️ Endpoints</h2>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span><span class="method post">POST</span> /screenshot</h3>
                <p>Capture a screenshot of any webpage.</p>
                
                <h4>Parameters</h4>
                <table>
                    <tr>
                        <th>Parameter</th>
                        <th>Type</th>
                        <th>Required</th>
                        <th>Default</th>
                        <th>Description</th>
                    </tr>
                    <tr>
                        <td><code>url</code></td>
                        <td>string</td>
                        <td>Yes</td>
                        <td>-</td>
                        <td>The URL of the webpage to capture (must start with http:// or https://)</td>
                    </tr>
                    <tr>
                        <td><code>width</code></td>
                        <td>integer</td>
                        <td>No</td>
                        <td>1920</td>
                        <td>Viewport width in pixels (100-3840)</td>
                    </tr>
                    <tr>
                        <td><code>height</code></td>
                        <td>integer</td>
                        <td>No</td>
                        <td>1080</td>
                        <td>Viewport height in pixels (100-2160)</td>
                    </tr>
                    <tr>
                        <td><code>fullpage</code></td>
                        <td>boolean</td>
                        <td>No</td>
                        <td>false</td>
                        <td>Capture the entire page (true/false)</td>
                    </tr>
                    <tr>
                        <td><code>delay</code></td>
                        <td>integer</td>
                        <td>No</td>
                        <td>0</td>
                        <td>Delay before capture in milliseconds (0-30000)</td>
                    </tr>
                    <tr>
                        <td><code>format</code></td>
                        <td>string</td>
                        <td>No</td>
                        <td>png</td>
                        <td>Image format: "png" or "jpeg"</td>
                    </tr>
                    <tr>
                        <td><code>quality</code></td>
                        <td>integer</td>
                        <td>No</td>
                        <td>80</td>
                        <td>JPEG quality (1-100, only for JPEG format)</td>
                    </tr>
                </table>
                
                <h4>Example Requests</h4>
                
                <p><strong>GET Request:</strong></p>
                <pre>curl -H "X-API-Key: your_api_key" \
  "http://localhost:5000/screenshot?url=https://example.com&width=1280&height=720&format=png"</pre>
                
                <p><strong>POST Request:</strong></p>
                <pre>curl -X POST http://localhost:5000/screenshot \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "width": 1280,
    "height": 720,
    "fullpage": true,
    "format": "jpeg",
    "quality": 90
  }'</pre>
                
                <h4>Response</h4>
                <p>On success: Binary image data (PNG or JPEG)</p>
                <p>On error: JSON error object</p>
                <pre>{
  "error": "Error type",
  "message": "Detailed error message"
}</pre>
            </div>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span> /health</h3>
                <p>Check API health status (no authentication required).</p>
                
                <h4>Response</h4>
                <pre>{
  "status": "healthy",
  "timestamp": "2025-10-05T15:51:29.000000"
}</pre>
            </div>
            
            <h2>💾 Caching</h2>
            <p>Screenshots are cached for 24 hours based on URL and parameters. Identical requests within this window will return cached results instantly, reducing server load and improving response times.</p>
            
            <h2>📝 Response Codes</h2>
            <table>
                <tr>
                    <th>Code</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>200</td>
                    <td>Success - Screenshot returned</td>
                </tr>
                <tr>
                    <td>400</td>
                    <td>Bad Request - Invalid parameters</td>
                </tr>
                <tr>
                    <td>401</td>
                    <td>Unauthorized - Missing or invalid API key</td>
                </tr>
                <tr>
                    <td>429</td>
                    <td>Too Many Requests - Rate limit exceeded</td>
                </tr>
                <tr>
                    <td>500</td>
                    <td>Internal Server Error - Screenshot capture failed</td>
                </tr>
            </table>
            
            <h2>🔐 Default API Keys</h2>
            <p>For testing purposes, the following API keys are pre-configured:</p>
            <ul>
                <li><code>demo-key-12345</code></li>
                <li><code>test-key-67890</code></li>
                <li><code>dev-key-abcde</code></li>
            </ul>
            
            <div class="warning">
                <strong>⚠️ Production Note:</strong> Replace these with secure, randomly generated keys before deployment.
            </div>
            
            <h2>🚀 Quick Start</h2>
            <ol>
                <li>Choose an API key (or use a demo key for testing)</li>
                <li>Make a request to <code>/screenshot</code> with your URL</li>
                <li>Receive your screenshot image instantly</li>
            </ol>
            
            <p style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d;">
                <strong>Webpage Screenshot API v1.0.0</strong><br>
                Need help? Check the logs at <code>logs/api_requests.log</code>
            </p>
        </div>
    </body>
    </html>
    """
    return render_template_string(doc_html)


if __name__ == '__main__':
    print("=" * 60)
    print("Webpage Screenshot API")
    print("=" * 60)
    print(f"Starting server on http://localhost:5000")
    print(f"Documentation: http://localhost:5000/docs")
    print(f"Default API Keys: demo-key-12345, test-key-67890, dev-key-abcde")
    print("=" * 60)
    # Disable reloader to prevent conflicts with Playwright
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
