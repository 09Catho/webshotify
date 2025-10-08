# 🚀 Advanced Features Guide

Your Screenshot API now includes enterprise-grade features! Here's everything you can do:

## 📋 Quick Feature Overview

✅ **Element-Specific Screenshots** - Capture specific DOM elements  
✅ **Device Emulation** - iPhone, iPad, Android presets  
✅ **Custom User Agent** - Emulate any browser  
✅ **Dark Mode** - Capture dark theme versions  
✅ **Wait for Elements** - Wait for specific content to load  
✅ **Custom JavaScript** - Execute code before capture  
✅ **Batch Processing** - Multiple URLs in one request  
✅ **PDF Export** - Export pages as PDF  
✅ **Custom Headers & Cookies** - Authenticate to protected pages  
✅ **Geolocation & Timezone** - Spoof location and time  
✅ **Block Ads** - Remove ads and trackers  
✅ **Lazy Loading** - Scroll to trigger lazy-loaded content  
✅ **Print Media** - Capture print-optimized layouts  
✅ **Rate Limit Headers** - Monitor your usage  

---

## 1️⃣ Element-Specific Screenshots

Capture only a specific part of the page using CSS selectors.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&selector=.main-content
```

### POST Request:
```json
{
  "url": "https://example.com",
  "selector": "#header",
  "format": "png"
}
```

**Use Cases:**
- Capture specific charts or graphs
- Extract product images
- Screenshot navigation menus
- Grab specific UI components

---

## 2️⃣ Device Emulation

Use device presets for perfect mobile screenshots.

### Available Devices:
- `iphone13` - iPhone 13 (390x844)
- `iphone13_pro` - iPhone 13 Pro (428x926)
- `ipad_pro` - iPad Pro (1024x1366)
- `samsung_galaxy` - Samsung Galaxy (360x740)
- `pixel_5` - Google Pixel 5 (393x851)
- `desktop_1080p` - Desktop 1080p (1920x1080)
- `desktop_4k` - Desktop 4K (3840x2160)

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&device=iphone13
```

### POST Request:
```json
{
  "url": "https://example.com",
  "device": "ipad_pro",
  "format": "png"
}
```

**List All Devices:**
```
GET http://localhost:5000/devices
```

---

## 3️⃣ Dark Mode

Capture the dark theme version of websites.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&dark_mode=true
```

### POST Request:
```json
{
  "url": "https://example.com",
  "dark_mode": true,
  "format": "png"
}
```

---

## 4️⃣ Wait for Specific Elements

Wait for dynamic content to load before capturing.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&wait_for_selector=.loaded-content
```

### POST Request:
```json
{
  "url": "https://example.com",
  "wait_for_selector": "#dynamic-content",
  "delay": 2000
}
```

**Use Cases:**
- Wait for AJAX content
- Let animations complete
- Ensure images are loaded
- Wait for user-generated content

---

## 5️⃣ Custom JavaScript Execution

Execute custom JavaScript before taking the screenshot.

### POST Request:
```json
{
  "url": "https://example.com",
  "script": "document.querySelector('.popup').remove()",
  "format": "png"
}
```

**Examples:**

**Hide Cookie Banners:**
```javascript
"script": "document.querySelector('.cookie-banner').style.display='none'"
```

**Scroll to Element:**
```javascript
"script": "document.querySelector('#target').scrollIntoView()"
```

**Trigger Click:**
```javascript
"script": "document.querySelector('.show-more').click()"
```

---

## 6️⃣ Batch Processing

Capture multiple URLs in a single request.

### POST Request:
```json
{
  "urls": [
    "https://example.com",
    "https://google.com",
    "https://github.com"
  ],
  "settings": {
    "width": 1280,
    "height": 720,
    "format": "png",
    "device": "desktop_1080p"
  }
}
```

**Response:**
```json
{
  "total": 3,
  "results": [
    {
      "url": "https://example.com",
      "status": "success",
      "data": "data:image/png;base64,..."
    },
    ...
  ]
}
```

**Limits:**
- Maximum 10 URLs per batch
- Images returned as base64 data URIs

---

## 7️⃣ PDF Export

Export webpages as PDF documents.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&format=pdf
```

### POST Request:
```json
{
  "url": "https://example.com",
  "format": "pdf",
  "fullpage": true
}
```

**Use Cases:**
- Documentation archival
- Invoice generation
- Report creation
- Legal records

---

## 8️⃣ Custom Headers & Cookies

Access authenticated or protected pages.

### POST Request Only:
```json
{
  "url": "https://protected-site.com",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN",
    "Custom-Header": "value"
  },
  "cookies": [
    {
      "name": "session_id",
      "value": "abc123",
      "domain": "protected-site.com",
      "path": "/"
    }
  ]
}
```

---

## 9️⃣ Geolocation & Timezone

Spoof location and timezone for location-based content.

### POST Request:
```json
{
  "url": "https://example.com",
  "geolocation": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "timezone": "America/Los_Angeles"
}
```

### Browser Usage (Timezone Only):
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&timezone=America/New_York
```

**Use Cases:**
- Test location-based features
- Capture region-specific content
- Test timezone-sensitive displays

---

## 🔟 Block Ads & Trackers

Remove advertising and tracking scripts for cleaner screenshots.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&block_ads=true
```

### POST Request:
```json
{
  "url": "https://example.com",
  "block_ads": true
}
```

**Blocks:**
- Image ads
- Video ads
- Analytics scripts
- Tracking pixels
- Third-party fonts

---

## 1️⃣1️⃣ Lazy Loading Support

Scroll through the page to trigger lazy-loaded images and content.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&scroll_page=true&fullpage=true
```

### POST Request:
```json
{
  "url": "https://example.com",
  "scroll_page": true,
  "fullpage": true
}
```

---

## 1️⃣2️⃣ Print Media Emulation

Capture print-optimized layouts.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&media_type=print
```

### POST Request:
```json
{
  "url": "https://example.com",
  "media_type": "print",
  "format": "pdf"
}
```

---

## 1️⃣3️⃣ Custom User Agent

Use custom user agent strings.

### Browser Usage:
```
http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345&user_agent=CustomBot/1.0
```

### POST Request:
```json
{
  "url": "https://example.com",
  "user_agent": "Mozilla/5.0 (Custom Bot)"
}
```

---

## 1️⃣4️⃣ Rate Limit Information

All responses now include rate limit headers.

**Response Headers:**
```
X-RateLimit-Remaining-Minute: 8
X-RateLimit-Remaining-Hour: 55
```

---

## 🎯 Advanced Combinations

### Mobile + Dark Mode + No Ads
```json
{
  "url": "https://example.com",
  "device": "iphone13",
  "dark_mode": true,
  "block_ads": true
}
```

### Element Screenshot + Custom Script
```json
{
  "url": "https://example.com",
  "selector": "#chart",
  "script": "document.querySelector('.tooltip').remove()",
  "wait_for_selector": ".chart-loaded"
}
```

### Full Page + Lazy Load + PDF
```json
{
  "url": "https://example.com",
  "fullpage": true,
  "scroll_page": true,
  "format": "pdf",
  "delay": 3000
}
```

### Authenticated Page Screenshot
```json
{
  "url": "https://app.example.com/dashboard",
  "headers": {
    "Authorization": "Bearer token123"
  },
  "cookies": [
    {"name": "session", "value": "xyz", "domain": "example.com"}
  ],
  "wait_for_selector": ".dashboard-loaded"
}
```

---

## 📊 Parameter Reference

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `url` | string | - | **Required** - Page URL |
| `width` | integer | 100-3840 | Viewport width |
| `height` | integer | 100-2160 | Viewport height |
| `fullpage` | boolean | true/false | Capture full page |
| `delay` | integer | 0-30000 | Wait time in ms |
| `format` | string | png/jpeg/pdf | Output format |
| `quality` | integer | 1-100 | JPEG quality |
| `selector` | string | CSS | Element selector |
| `device` | string | preset name | Device emulation |
| `user_agent` | string | - | Custom UA |
| `dark_mode` | boolean | true/false | Dark theme |
| `wait_for_selector` | string | CSS | Wait for element |
| `script` | string | JS code | Custom JavaScript |
| `block_ads` | boolean | true/false | Block ads |
| `scroll_page` | boolean | true/false | Scroll for lazy load |
| `media_type` | string | screen/print | Media emulation |
| `headers` | object | - | HTTP headers (POST) |
| `cookies` | array | - | Cookies (POST) |
| `geolocation` | object | - | Location (POST) |
| `timezone` | string | IANA ID | Timezone |

---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/screenshot` | GET/POST | Capture single screenshot |
| `/batch` | POST | Capture multiple screenshots |
| `/devices` | GET | List device presets |
| `/health` | GET | Health check |
| `/docs` | GET | Documentation |

---

## 💡 Pro Tips

1. **Combine Features** - Use multiple features together for powerful results
2. **Cache Awareness** - Different parameters create different cache entries
3. **Batch Processing** - Use for multiple URLs with same settings
4. **Wait Strategically** - Use `wait_for_selector` instead of fixed delays when possible
5. **Test Locally** - Try features on http://localhost:5000/docs

---

## 🐛 Troubleshooting

**Timeout Errors:**
- Increase `delay` parameter
- Use `wait_for_selector` for dynamic content
- Check if site blocks automated browsers

**Element Not Found:**
- Verify CSS selector is correct
- Wait for element with `wait_for_selector`
- Check if element loads after JavaScript

**Authentication Issues:**
- Ensure cookies have correct domain
- Check header format
- Verify token/session is valid

---

## 📞 Support

Visit http://localhost:5000/docs for interactive documentation and examples!

**Your API is now feature-complete and ready for production! 🚀**
