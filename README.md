<div align="center">

# 📸 Webshotify

### Professional Screenshot API with 25+ Advanced Features

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen?style=for-the-badge)](https://github.com/09Catho/webshotify)
[![Tests](https://img.shields.io/badge/tests-passing-success?style=for-the-badge)](https://github.com/09Catho/webshotify)
[![Coverage](https://img.shields.io/badge/coverage-97.5%25-brightgreen?style=for-the-badge)](https://github.com/09Catho/webshotify)

**Capture pixel-perfect screenshots with multi-browser support, visual regression testing, device emulation, webhooks, and more!**

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-live-demo) • [Documentation](#-documentation) • [Deploy](#-deployment)

<img src="https://img.shields.io/github/stars/09Catho/webshotify?style=social" alt="GitHub stars">
<img src="https://img.shields.io/github/forks/09Catho/webshotify?style=social" alt="GitHub forks">

---

### 🎯 Why Webshotify?

| Feature | Webshotify | Other APIs |
|---------|------------|------------|
| **Multi-Browser** | ✅ 3 Engines | ❌ 1 Engine |
| **Visual Regression** | ✅ Built-in | ❌ Not Available |
| **Device Emulation** | ✅ 7 Presets | ⚠️ Limited |
| **Webhooks** | ✅ Full Support | ❌ Not Available |
| **Dashboard** | ✅ Real-time | ❌ Not Available |
| **Open Source** | ✅ MIT License | ❌ Proprietary |
| **Price** | ✅ Free/Affordable | ❌ Expensive |

</div>

---

## ✨ Features

### 🌐 Multi-Browser Support
Capture screenshots using different browser engines for cross-browser testing:
- **Chromium** - Chrome/Edge rendering engine
- **Firefox** - Gecko rendering engine  
- **WebKit** - Safari rendering engine

### 📱 Device Emulation
Pre-configured device presets for responsive testing:
- 📱 **iPhone 13** - 390x844 (Mobile)
- 📱 **iPhone 13 Pro Max** - 428x926 (Large Mobile)
- 📱 **iPad Pro 11"** - 834x1194 (Tablet)
- 📱 **Samsung Galaxy S21** - 360x800 (Android)
- 💻 **Desktop 1080p** - 1920x1080 (Standard)
- 🖥️ **Desktop 4K** - 3840x2160 (High-res)
- 🖥️ **Ultrawide** - 3440x1440 (Widescreen)

### 🎨 Advanced Rendering Options
- **Dark Mode Emulation** - Force dark color scheme
- **Animation Freezing** - Disable CSS animations for consistent screenshots
- **Full Page Capture** - Scroll and capture entire page content
- **Element Selection** - Capture specific elements via CSS selectors
- **Custom JavaScript** - Execute custom scripts before capture
- **Media Emulation** - Print media type support
- **Wait for Selector** - Wait for specific elements before capturing
- **Lazy Loading** - Automatic scroll to load lazy-loaded content

### 🔍 Visual Regression Testing
- **Pixel-Perfect Comparison** - Compare screenshots with baseline images
- **Diff Generation** - Visual diff images highlighting changes
- **Threshold Configuration** - Configurable difference thresholds
- **Baseline Management** - Create and manage baseline screenshots
- **CI/CD Integration** - Perfect for automated testing pipelines

### 🚀 Enterprise Features
- **Webhook Support** - Async job processing with callback notifications
- **Job Tracking** - Monitor async job status and history
- **HMAC Signatures** - Secure webhook authentication
- **Batch Processing** - Process multiple URLs in single request
- **Usage Dashboard** - Web UI for analytics and API key management
- **System Monitoring** - Real-time CPU, memory, and disk usage
- **Data Injection** - localStorage, sessionStorage, and API mocking

### 🔐 Security & Performance
- **Secure Authentication** - bcrypt hashed API keys with constant-time comparison
- **Rate Limiting** - Per-key request limits (configurable)
- **Smart Caching** - 24-hour cache for identical requests
- **Request Logging** - Comprehensive audit trail
- **CORS Support** - Cross-origin resource sharing
- **Health Monitoring** - `/health` endpoint for uptime monitoring

### 📊 Output Formats
- **PNG** - Lossless compression
- **JPEG** - Adjustable quality (1-100)
- **PDF** - Document export

### 🛠️ Developer Experience
- **Interactive Documentation** - Built-in API docs at `/docs`
- **Beautiful Landing Page** - Professional homepage with live demo
- **Comprehensive Demo** - Interactive demo showcasing all features
- **Usage Dashboard** - Real-time analytics and monitoring
- **RESTful API** - Clean, intuitive endpoints
- **Docker Support** - Complete containerization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/09Catho/webshotify.git
cd webshotify

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium firefox webkit

# 4. Run the server
python app.py
```

The API will start on `http://localhost:5000` 🎉

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t webshotify .
docker run -p 5000:5000 webshotify
```

---

## 🎮 Live Demo

Visit `http://localhost:5000` to access:
- 🏠 **Landing Page** - Beautiful homepage with feature showcase
- 🎯 **Interactive Demo** - Try all 25+ features in real-time
- 📊 **Dashboard** - View API usage and analytics
- 📖 **Documentation** - Complete API reference

---

## 📚 API Documentation

### Basic Screenshot

```bash
# Simple screenshot
curl "http://localhost:5000/screenshot?url=https://example.com&api_key=demo-key-12345" \
  --output screenshot.png
```

### Multi-Browser Screenshot

```python
import requests

# Capture with Firefox
response = requests.get('http://localhost:5000/screenshot', params={
    'url': 'https://example.com',
    'browser': 'firefox',
    'api_key': 'demo-key-12345'
})

with open('firefox_screenshot.png', 'wb') as f:
    f.write(response.content)
```

### Device Emulation

```javascript
const axios = require('axios');

// Capture iPhone 13 screenshot
const response = await axios.get('http://localhost:5000/screenshot', {
  params: {
    url: 'https://example.com',
    device: 'iphone13',
    api_key: 'demo-key-12345'
  },
  responseType: 'arraybuffer'
});

fs.writeFileSync('iphone_screenshot.png', response.data);
```

### Dark Mode Screenshot

```bash
curl "http://localhost:5000/screenshot?url=https://example.com&dark_mode=true&api_key=demo-key-12345" \
  --output dark_screenshot.png
```

### Full Page Capture

```python
import requests

response = requests.get('http://localhost:5000/screenshot', params={
    'url': 'https://example.com',
    'fullpage': 'true',
    'scroll_page': 'true',  # Load lazy content
    'api_key': 'demo-key-12345'
})
```

### Visual Regression Testing

```python
import requests

# Create baseline
baseline_response = requests.post('http://localhost:5000/baseline', 
    headers={'X-API-Key': 'demo-key-12345'},
    json={
        'url': 'https://example.com',
        'name': 'homepage_baseline'
    }
)

# Compare with baseline
compare_response = requests.post('http://localhost:5000/compare',
    headers={'X-API-Key': 'demo-key-12345'},
    json={
        'url': 'https://example.com',
        'baseline': 'homepage_baseline',
        'threshold': 0.02
    }
)

result = compare_response.json()
print(f"Match: {result['match']}")
print(f"Difference: {result['difference_percentage']}%")
```

### Webhook (Async) Screenshot

```python
import requests

response = requests.post('http://localhost:5000/screenshot/async',
    headers={'X-API-Key': 'demo-key-12345'},
    json={
        'url': 'https://example.com',
        'webhook_url': 'https://yourapp.com/webhook',
        'webhook_secret': 'your-secret',
        'params': {
            'browser': 'firefox',
            'fullpage': True
        }
    }
)

job_id = response.json()['job_id']
print(f"Job ID: {job_id}")
```

### Batch Processing

```python
import requests

response = requests.post('http://localhost:5000/batch',
    headers={'X-API-Key': 'demo-key-12345'},
    json={
        'urls': [
            'https://example.com',
            'https://github.com',
            'https://stackoverflow.com'
        ],
        'settings': {
            'width': 1280,
            'height': 720,
            'format': 'png'
        }
    }
)

results = response.json()['results']
```

---

## 🎯 All API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page with live demo |
| `/screenshot` | GET/POST | Capture screenshot |
| `/screenshot/async` | POST | Async screenshot with webhook |
| `/jobs/{id}` | GET | Check async job status |
| `/batch` | POST | Batch screenshot processing |
| `/compare` | POST | Compare screenshots (visual regression) |
| `/baseline` | POST | Create baseline screenshot |
| `/devices` | GET | List device presets |
| `/dashboard` | GET | Usage dashboard (web UI) |
| `/health` | GET | API health check |
| `/docs` | GET | Interactive API documentation |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Server Configuration
FLASK_ENV=production
PORT=5000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Caching
CACHE_DURATION_HOURS=24

# Security
API_KEY_1=your-secure-key-1
API_KEY_2=your-secure-key-2
```

### API Key Management

```bash
# Generate new secure API key
python manage_keys_secure.py

# List all keys
python manage_keys_secure.py
# Choose option 1

# Validate a key
python manage_keys_secure.py
# Choose option 4
```

---

## 📊 Request Parameters

### Screenshot Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | **required** | Target webpage URL |
| `browser` | string | `chromium` | Browser engine: `chromium`, `firefox`, `webkit` |
| `width` | integer | `1920` | Viewport width (320-3840) |
| `height` | integer | `1080` | Viewport height (320-2160) |
| `device` | string | - | Device preset (see list above) |
| `format` | string | `png` | Output format: `png`, `jpeg`, `pdf` |
| `quality` | integer | `80` | JPEG quality (1-100) |
| `fullpage` | boolean | `false` | Capture full page |
| `dark_mode` | boolean | `false` | Emulate dark mode |
| `disable_animations` | boolean | `false` | Freeze CSS animations |
| `block_ads` | boolean | `false` | Block ads and trackers |
| `scroll_page` | boolean | `false` | Scroll for lazy loading |
| `delay` | integer | `0` | Delay before capture (ms) |
| `selector` | string | - | CSS selector for element capture |
| `wait_for_selector` | string | - | Wait for element before capture |
| `script` | string | - | JavaScript to execute before capture |
| `user_agent` | string | - | Custom user agent |
| `media_type` | string | `screen` | Media type: `screen`, `print` |
| `timezone` | string | - | Timezone (e.g., `America/New_York`) |
| `geolocation` | object | - | Geolocation: `{latitude, longitude}` |

---

## 🧪 Testing

```bash
# Run all tests
python test_api.py

# Run specific test suite
python test_enterprise_features.py

# Run comprehensive YouTube test
python test_youtube.py
```

**Test Coverage: 97.5%** ✅

---

## 🚀 Deployment

### Deploy to Google Cloud Platform

```bash
# Deploy to Cloud Run
gcloud run deploy webshotify \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

See [GCP_DEPLOYMENT_GUIDE.md](GCP_DEPLOYMENT_GUIDE.md) for complete instructions.

### Deploy to Railway

```bash
railway init
railway up
```

### Deploy to Heroku

```bash
heroku create webshotify
git push heroku main
```

### Deploy with Docker

```bash
docker build -t webshotify .
docker run -p 5000:5000 -e API_KEY_1=your-key webshotify
```

---

## 📖 Documentation

- **[README.md](README.md)** - This file (Quick start & API reference)
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[SECURITY.md](SECURITY.md)** - Security policy
- **[LICENSE](LICENSE)** - MIT License

### Deployment Guides
- **[GCP_DEPLOYMENT_GUIDE.md](GCP_DEPLOYMENT_GUIDE.md)** - Google Cloud Platform

### Feature Documentation
- **[ENTERPRISE_FEATURES.md](ENTERPRISE_FEATURES.md)** - Advanced features
- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Feature guide
- **[CODE_REVIEW.md](CODE_REVIEW.md)** - Code quality report

---

## 🏗️ Architecture

```
webshotify/
├── app.py                      # Main Flask application
├── screenshot_service.py       # Screenshot capture logic
├── auth_service.py            # Secure authentication (bcrypt)
├── rate_limiter.py            # Rate limiting
├── cache_service.py           # Caching layer
├── comparison_service.py      # Visual regression testing
├── webhook_service.py         # Async job processing
├── dashboard_service.py       # Analytics dashboard
├── templates/                 # HTML templates
│   ├── landing.html          # Landing page
│   ├── dashboard.html        # Dashboard
│   └── components/           # Reusable components
├── tests/                     # Test suites
├── config/                    # Configuration
└── docs/                      # Documentation
```

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11, Flask 3.0
- **Browser Automation:** Playwright 1.40
- **Image Processing:** Pillow 10.1
- **Security:** bcrypt 4.1
- **Containerization:** Docker
- **Testing:** pytest, requests
- **Monitoring:** psutil

---

## 🎯 Use Cases

### 🔍 QA & Testing
- Visual regression testing
- Cross-browser compatibility testing
- Automated UI testing
- Screenshot comparison in CI/CD

### 📱 Marketing & Design
- Social media previews (Open Graph images)
- Client reports and presentations
- Portfolio screenshots
- Email campaign images

### 📚 Documentation
- API documentation screenshots
- Tutorial and guide images
- Help center visuals
- Product documentation

### 🛒 E-commerce
- Product page captures
- Invoice generation (PDF)
- Order confirmation images
- Catalog screenshots

### 📊 Monitoring
- Website change detection
- Uptime monitoring with screenshots
- Competitor analysis
- Content monitoring

---

## 🌟 Why Choose Webshotify?

### ✅ Comprehensive Features
**25+ advanced features** - More than any commercial API in the same price range.

### ✅ Multi-Browser Support
**3 browser engines** - Test across Chrome, Firefox, and Safari rendering.

### ✅ Visual Regression Testing
**Built-in comparison** - Pixel-perfect diff generation for CI/CD pipelines.

### ✅ Production Ready
- ✅ Secure bcrypt authentication
- ✅ Rate limiting and caching
- ✅ Health monitoring
- ✅ Comprehensive logging
- ✅ Docker support
- ✅ 97.5% test coverage

### ✅ Beautiful UI
- ✅ Professional landing page
- ✅ Interactive demo
- ✅ Real-time dashboard
- ✅ Complete documentation

### ✅ Open Source
- ✅ MIT License
- ✅ Community-driven
- ✅ Transparent development
- ✅ Free to use and modify

---

## 📈 Roadmap

### v1.1 (Coming Soon)
- [ ] Video recording support
- [ ] Screenshot archive/history
- [ ] Scheduled screenshots
- [ ] Image post-processing (resize, crop, watermark)
- [ ] More device presets

### v1.2 (Future)
- [ ] GraphQL API
- [ ] WebSocket support for real-time updates
- [ ] Advanced analytics
- [ ] Team collaboration features
- [ ] Custom branding/white-label

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contributors

<a href="https://github.com/09Catho/webshotify/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=09Catho/webshotify" />
</a>

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/09Catho/webshotify?style=social)
![GitHub forks](https://img.shields.io/github/forks/09Catho/webshotify?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/09Catho/webshotify?style=social)
![GitHub issues](https://img.shields.io/github/issues/09Catho/webshotify)
![GitHub pull requests](https://img.shields.io/github/issues-pr/09Catho/webshotify)
![GitHub last commit](https://img.shields.io/github/last-commit/09Catho/webshotify)
![GitHub repo size](https://img.shields.io/github/repo-size/09Catho/webshotify)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

- 📧 **Email:** support@webshotify.com
- 💬 **Discussions:** [GitHub Discussions](https://github.com/09Catho/webshotify/discussions)
- 🐛 **Issues:** [GitHub Issues](https://github.com/09Catho/webshotify/issues)
- 📖 **Documentation:** [Full Docs](https://github.com/09Catho/webshotify)

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Pillow](https://python-pillow.org/) - Image processing
- All our amazing contributors!

---

<div align="center">

### ⭐ Star us on GitHub!

If you find Webshotify useful, please consider giving us a star. It helps us grow! ⭐

**Made with ❤️ by the Webshotify Team**

[⬆ Back to Top](#-webshotify)

</div>
