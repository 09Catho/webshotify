"""
Screenshot Service
Handles webpage screenshot capture using Playwright with advanced features
"""

import os
import asyncio
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from PIL import Image
import io


class ScreenshotService:
    """Service for capturing webpage screenshots with advanced features"""
    
    # Device presets for emulation
    DEVICE_PRESETS = {
        'iphone13': {'width': 390, 'height': 844, 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', 'mobile': True},
        'iphone13_pro': {'width': 428, 'height': 926, 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15', 'mobile': True},
        'ipad_pro': {'width': 1024, 'height': 1366, 'user_agent': 'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15', 'mobile': True},
        'samsung_galaxy': {'width': 360, 'height': 740, 'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36', 'mobile': True},
        'pixel_5': {'width': 393, 'height': 851, 'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36', 'mobile': True},
        'desktop_1080p': {'width': 1920, 'height': 1080, 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'mobile': False},
        'desktop_4k': {'width': 3840, 'height': 2160, 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'mobile': False},
    }
    
    def __init__(self):
        self.screenshots_dir = Path('screenshots')
        self.screenshots_dir.mkdir(exist_ok=True)
    
    def capture_screenshot(self, url, width=1920, height=1080, fullpage=False, 
                          delay=0, image_format='png', quality=80, selector=None,
                          device=None, user_agent=None, dark_mode=False, 
                          wait_for_selector=None, custom_script=None, 
                          block_ads=False, scroll_page=False, media_type=None,
                          extra_headers=None, cookies=None, geolocation=None,
                          timezone=None, browser_type='chromium', disable_animations=False,
                          inject_data=None):
        """
        Capture a screenshot of a webpage with advanced options
        
        Args:
            url (str): URL of the webpage
            width (int): Viewport width
            height (int): Viewport height
            fullpage (bool): Capture full page
            delay (int): Delay before capture in milliseconds
            image_format (str): Image format ('png' or 'jpeg')
            quality (int): JPEG quality (1-100)
            selector (str): CSS selector to capture specific element
            device (str): Device preset name (e.g., 'iphone13')
            user_agent (str): Custom user agent string
            dark_mode (bool): Emulate dark mode
            wait_for_selector (str): Wait for this selector before capture
            custom_script (str): JavaScript to execute before capture
            block_ads (bool): Block ads and trackers
            scroll_page (bool): Scroll through page for lazy loading
            media_type (str): Emulate media type ('screen' or 'print')
            extra_headers (dict): Additional HTTP headers
            cookies (list): Cookies to set
            geolocation (dict): Geolocation {'latitude': float, 'longitude': float}
            timezone (str): Timezone ID (e.g., 'America/New_York')
            browser_type (str): Browser engine ('chromium', 'firefox', 'webkit')
            disable_animations (bool): Freeze all animations and transitions
            inject_data (dict): Data to inject (localStorage, sessionStorage, api_mocks)
        
        Returns:
            str: Path to the saved screenshot
        
        Raises:
            Exception: If screenshot capture fails
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f'screenshot_{timestamp}.{image_format}'
        filepath = self.screenshots_dir / filename
        
        try:
            with sync_playwright() as playwright:
                # Launch browser based on browser_type
                browser_engines = {
                    'chromium': playwright.chromium,
                    'firefox': playwright.firefox,
                    'webkit': playwright.webkit
                }
                
                browser_engine = browser_engines.get(browser_type.lower(), playwright.chromium)
                browser = browser_engine.launch(headless=True)
                
                # Prepare context options
                context_options = {
                    'ignore_https_errors': True,
                    'java_script_enabled': True,
                }
                
                # Device emulation
                if device and device in self.DEVICE_PRESETS:
                    preset = self.DEVICE_PRESETS[device]
                    context_options['viewport'] = {'width': preset['width'], 'height': preset['height']}
                    context_options['user_agent'] = preset['user_agent']
                    context_options['is_mobile'] = preset.get('mobile', False)
                else:
                    context_options['viewport'] = {'width': width, 'height': height}
                    if user_agent:
                        context_options['user_agent'] = user_agent
                
                # Dark mode
                if dark_mode:
                    context_options['color_scheme'] = 'dark'
                
                # Geolocation
                if geolocation:
                    context_options['geolocation'] = geolocation
                    context_options['permissions'] = ['geolocation']
                
                # Timezone
                if timezone:
                    context_options['timezone_id'] = timezone
                
                # Extra headers
                if extra_headers:
                    context_options['extra_http_headers'] = extra_headers
                
                # Create context
                context = browser.new_context(**context_options)
                
                # Set cookies
                if cookies:
                    context.add_cookies(cookies)
                
                # Block ads and trackers
                if block_ads:
                    context.route("**/*", lambda route: route.abort() 
                                 if route.request.resource_type in ["image", "media", "font"] 
                                 or any(ad in route.request.url for ad in ['ads', 'tracking', 'analytics', 'doubleclick'])
                                 else route.continue_())
                
                # Create new page
                page = context.new_page()
                
                # Emulate media type
                if media_type == 'print':
                    page.emulate_media(media='print')
                elif media_type == 'screen':
                    page.emulate_media(media='screen')
                
                # Set timeout
                page.set_default_timeout(60000)  # 60 seconds for advanced features
                
                # Navigate to URL
                try:
                    page.goto(url, wait_until='networkidle', timeout=45000)
                except PlaywrightTimeoutError:
                    # Fallback to domcontentloaded if networkidle times out
                    page.goto(url, wait_until='domcontentloaded', timeout=45000)
                
                # Inject data (localStorage, sessionStorage, API mocks)
                if inject_data:
                    self._inject_test_data(page, inject_data)
                
                # Disable animations for consistent screenshots
                if disable_animations:
                    self._freeze_animations(page)
                
                # Scroll page for lazy loading
                if scroll_page:
                    self._scroll_page(page)
                
                # Wait for specific selector
                if wait_for_selector:
                    try:
                        page.wait_for_selector(wait_for_selector, timeout=30000)
                    except PlaywrightTimeoutError:
                        pass  # Continue even if selector not found
                
                # Execute custom JavaScript
                if custom_script:
                    try:
                        page.evaluate(custom_script)
                    except Exception as e:
                        print(f"JavaScript execution warning: {e}")
                
                # Wait for specified delay
                if delay > 0:
                    page.wait_for_timeout(min(delay, 30000))  # Max 30 seconds
                
                # Capture screenshot
                screenshot_options = {
                    'path': str(filepath),
                    'full_page': fullpage
                }
                
                if image_format == 'jpeg':
                    screenshot_options['type'] = 'jpeg'
                    screenshot_options['quality'] = quality
                else:
                    screenshot_options['type'] = 'png'
                
                # Element-specific screenshot
                if selector:
                    try:
                        element = page.query_selector(selector)
                        if element:
                            element.screenshot(**screenshot_options)
                        else:
                            page.screenshot(**screenshot_options)
                    except Exception:
                        page.screenshot(**screenshot_options)
                else:
                    page.screenshot(**screenshot_options)
                
                # Close browser
                context.close()
                browser.close()
            
            return str(filepath)
        
        except PlaywrightTimeoutError as e:
            raise Exception(f"Timeout while loading page: {str(e)}")
        except Exception as e:
            # Clean up file if it was created
            if filepath.exists():
                filepath.unlink()
            raise Exception(f"Failed to capture screenshot: {str(e)}")
    
    def _scroll_page(self, page):
        """
        Scroll through the entire page to trigger lazy loading
        
        Args:
            page: Playwright page object
        """
        try:
            page.evaluate("""
                async () => {
                    await new Promise((resolve) => {
                        let totalHeight = 0;
                        const distance = 100;
                        const timer = setInterval(() => {
                            const scrollHeight = document.body.scrollHeight;
                            window.scrollBy(0, distance);
                            totalHeight += distance;
                            
                            if(totalHeight >= scrollHeight){
                                clearInterval(timer);
                                window.scrollTo(0, 0);
                                resolve();
                            }
                        }, 100);
                    });
                }
            """)
        except Exception as e:
            print(f"Scroll warning: {e}")
    
    def _freeze_animations(self, page):
        """
        Freeze all CSS animations, transitions, and animated images
        
        Args:
            page: Playwright page object
        """
        try:
            animation_freeze_css = """
                <style id="animation-freeze">
                    *, *::before, *::after {
                        animation-duration: 0s !important;
                        animation-delay: 0s !important;
                        transition-duration: 0s !important;
                        transition-delay: 0s !important;
                        animation-play-state: paused !important;
                    }
                    
                    /* Freeze GIF animations */
                    img {
                        animation: none !important;
                    }
                    
                    /* Disable scroll animations */
                    html {
                        scroll-behavior: auto !important;
                    }
                </style>
            """
            page.evaluate(f"""
                () => {{
                    const style = document.createElement('style');
                    style.id = 'animation-freeze';
                    style.innerHTML = `{animation_freeze_css}`;
                    document.head.appendChild(style);
                    
                    // Pause all video elements
                    document.querySelectorAll('video').forEach(v => v.pause());
                    
                    // Stop all Web Animations API animations
                    document.getAnimations().forEach(a => a.pause());
                }}
            """)
        except Exception as e:
            print(f"Animation freeze warning: {e}")
    
    def _inject_test_data(self, page, inject_data):
        """
        Inject test data into localStorage, sessionStorage, and mock API responses
        
        Args:
            page: Playwright page object
            inject_data (dict): Data to inject with keys: localStorage, sessionStorage, api_mocks
        """
        try:
            # Inject localStorage
            if 'localStorage' in inject_data and inject_data['localStorage']:
                for key, value in inject_data['localStorage'].items():
                    page.evaluate(f"""
                        () => {{
                            localStorage.setItem('{key}', '{value}');
                        }}
                    """)
            
            # Inject sessionStorage
            if 'sessionStorage' in inject_data and inject_data['sessionStorage']:
                for key, value in inject_data['sessionStorage'].items():
                    page.evaluate(f"""
                        () => {{
                            sessionStorage.setItem('{key}', '{value}');
                        }}
                    """)
            
            # Mock API responses (intercept fetch)
            if 'api_mocks' in inject_data and inject_data['api_mocks']:
                import json
                mocks_json = json.dumps(inject_data['api_mocks'])
                page.evaluate(f"""
                    (mocks) => {{
                        const originalFetch = window.fetch;
                        window.fetch = function(url, options) {{
                            // Check if this URL should be mocked
                            for (const [mockUrl, mockResponse] of Object.entries(mocks)) {{
                                if (url.includes(mockUrl)) {{
                                    return Promise.resolve({{
                                        ok: mockResponse.status < 400,
                                        status: mockResponse.status || 200,
                                        json: () => Promise.resolve(mockResponse.body || {{}}),
                                        text: () => Promise.resolve(JSON.stringify(mockResponse.body || {{}})),
                                        headers: new Headers(mockResponse.headers || {{}})
                                    }});
                                }}
                            }}
                            return originalFetch(url, options);
                        }};
                    }}
                """, mocks_json)
                
        except Exception as e:
            print(f"Data injection warning: {e}")
    
    def capture_pdf(self, url, width=1920, height=1080, landscape=False, 
                   print_background=True, scale=1.0, extra_headers=None):
        """
        Capture webpage as PDF
        
        Args:
            url (str): URL of the webpage
            width (int): Page width in pixels
            height (int): Page height in pixels
            landscape (bool): Landscape orientation
            print_background (bool): Include background graphics
            scale (float): Scale of the webpage rendering (0.1 - 2.0)
            extra_headers (dict): Additional HTTP headers
        
        Returns:
            str: Path to the saved PDF
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f'screenshot_{timestamp}.pdf'
        filepath = self.screenshots_dir / filename
        
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                
                context_options = {
                    'ignore_https_errors': True,
                    'viewport': {'width': width, 'height': height}
                }
                
                if extra_headers:
                    context_options['extra_http_headers'] = extra_headers
                
                context = browser.new_context(**context_options)
                page = context.new_page()
                
                page.emulate_media(media='print')
                page.goto(url, wait_until='networkidle', timeout=45000)
                
                pdf_options = {
                    'path': str(filepath),
                    'landscape': landscape,
                    'print_background': print_background,
                    'scale': scale,
                    'format': 'A4'
                }
                
                page.pdf(**pdf_options)
                
                context.close()
                browser.close()
            
            return str(filepath)
        
        except Exception as e:
            if filepath.exists():
                filepath.unlink()
            raise Exception(f"Failed to generate PDF: {str(e)}")
    
    def cleanup_old_screenshots(self, max_age_hours=48):
        """
        Remove screenshots older than specified hours
        
        Args:
            max_age_hours (int): Maximum age in hours
        """
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for screenshot_file in self.screenshots_dir.glob('screenshot_*'):
            if screenshot_file.is_file():
                file_age = current_time - screenshot_file.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        screenshot_file.unlink()
                    except Exception:
                        pass  # Ignore cleanup errors
