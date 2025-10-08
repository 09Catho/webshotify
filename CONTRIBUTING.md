# Contributing to Screenshot API

First off, thank you for considering contributing to Screenshot API! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all.

### Our Standards

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers and help them learn
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other community members

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

**Bug Report Template:**
```markdown
**Description:**
A clear description of the bug.

**To Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior:**
What you expected to happen.

**Screenshots:**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.11]
- Browser: [e.g., Chrome 120]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - Why is this enhancement useful?
- **Proposed solution**
- **Alternative solutions** you've considered
- **Additional context**

### Pull Requests

We actively welcome your pull requests!

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Add tests if applicable
4. Ensure tests pass
5. Update documentation
6. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Git

### Setup Steps

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/screenshot-api.git
cd screenshot-api
```

2. **Create a virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium firefox webkit
```

4. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application:**
```bash
python app.py
```

6. **Run tests:**
```bash
python test_api.py
```

## 📝 Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] Self-review of your code completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings introduced

### PR Title Format

Use clear, descriptive titles:

```
✅ Good: "Add support for WebP format"
✅ Good: "Fix: Resolve timeout issue in Firefox"
✅ Good: "Docs: Update API documentation for webhooks"

❌ Bad: "Update"
❌ Bad: "Fix bug"
❌ Bad: "Changes"
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] All tests pass
```

## 💻 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Good: Clear function names, docstrings, type hints
def capture_screenshot(url: str, width: int = 1920, height: int = 1080) -> bytes:
    """
    Capture a screenshot of the specified URL.
    
    Args:
        url (str): Target webpage URL
        width (int): Viewport width in pixels
        height (int): Viewport height in pixels
    
    Returns:
        bytes: Screenshot image data
    
    Raises:
        ValueError: If URL is invalid
        TimeoutError: If page load times out
    """
    # Implementation
    pass
```

### Code Organization

```python
# 1. Standard library imports
import os
import sys
from datetime import datetime

# 2. Third-party imports
from flask import Flask, request
from playwright.sync_api import sync_playwright

# 3. Local imports
from auth_service import AuthService
from rate_limiter import RateLimiter
```

### Naming Conventions

- **Functions/Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private methods:** `_leading_underscore`

```python
# Good
class ScreenshotService:
    MAX_TIMEOUT = 30000
    
    def capture_screenshot(self, url: str):
        pass
    
    def _validate_url(self, url: str):
        pass
```

## 🧪 Testing Guidelines

### Writing Tests

```python
def test_screenshot_capture():
    """Test basic screenshot capture"""
    # Arrange
    url = "https://example.com"
    
    # Act
    result = capture_screenshot(url)
    
    # Assert
    assert result is not None
    assert len(result) > 0
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python test_api.py

# Run with coverage
python -m pytest --cov=.
```

### Test Coverage

Aim for:
- **80%+ overall coverage**
- **100% for critical paths** (auth, rate limiting)
- **90%+ for core features** (screenshot capture)

## 📚 Documentation

### Code Comments

```python
# Good: Explain WHY, not WHAT
# Use exponential backoff to handle rate limiting gracefully
time.sleep(2 ** attempt)

# Bad: Obvious comment
# Sleep for 2 seconds
time.sleep(2)
```

### Docstrings

Use Google-style docstrings:

```python
def process_image(image_data: bytes, format: str = "png") -> bytes:
    """
    Process and convert image data to specified format.
    
    Args:
        image_data (bytes): Raw image data
        format (str): Output format (png, jpeg, webp)
    
    Returns:
        bytes: Processed image data
    
    Raises:
        ValueError: If format is not supported
        
    Example:
        >>> data = capture_screenshot("https://example.com")
        >>> processed = process_image(data, format="jpeg")
    """
    pass
```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- 🐛 **Bug fixes** - Always appreciated!
- 📝 **Documentation improvements** - Help others understand
- 🧪 **Test coverage** - More tests = more confidence
- ⚡ **Performance optimizations** - Make it faster

### Feature Requests
- 🎨 **New image formats** (WebP, AVIF, etc.)
- 🌍 **Internationalization** (i18n support)
- 📊 **Analytics improvements** (better dashboard)
- 🔌 **Integration examples** (CI/CD, frameworks)

### Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

## 🏆 Recognition

Contributors will be:
- ✅ Listed in CONTRIBUTORS.md
- ✅ Mentioned in release notes
- ✅ Credited in documentation

## 💬 Getting Help

- 📖 Check the [documentation](README.md)
- 💬 Ask in [GitHub Discussions](../../discussions)
- 🐛 Report bugs in [Issues](../../issues)
- 📧 Email: support@yourapi.com (if applicable)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🎉 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🙏

**Happy Coding!** 🚀
