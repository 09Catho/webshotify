# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## 🐛 Reporting a Vulnerability

We take the security of Screenshot API seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do NOT:

- ❌ Open a public GitHub issue
- ❌ Disclose the vulnerability publicly before it's fixed
- ❌ Exploit the vulnerability beyond what's necessary to demonstrate it

### Please DO:

- ✅ Email us at: **security@yourapi.com** (replace with your email)
- ✅ Provide detailed information about the vulnerability
- ✅ Give us reasonable time to fix the issue before public disclosure
- ✅ Act in good faith towards our users' privacy and data

## 📧 What to Include in Your Report

Please include the following information:

1. **Type of vulnerability** (e.g., XSS, SQL injection, authentication bypass)
2. **Full paths** of source file(s) related to the vulnerability
3. **Location** of the affected source code (tag/branch/commit or direct URL)
4. **Step-by-step instructions** to reproduce the issue
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact** of the vulnerability
7. **Your contact information** for follow-up

### Example Report

```
Subject: [SECURITY] Authentication Bypass in API Key Validation

Description:
I discovered an authentication bypass vulnerability in the API key validation logic.

Affected Component:
- File: auth_service.py
- Function: validate_key()
- Lines: 45-60

Steps to Reproduce:
1. Send a request to /screenshot endpoint
2. Use API key: "admin' OR '1'='1"
3. Request is accepted without valid authentication

Impact:
Allows unauthorized access to all API endpoints without valid credentials.

Proof of Concept:
curl -X GET "http://api/screenshot?url=https://example.com" \
  -H "X-API-Key: admin' OR '1'='1"

Suggested Fix:
Implement proper input sanitization and use parameterized queries.

Contact: security-researcher@email.com
```

## ⏱️ Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity
  - Critical: 1-7 days
  - High: 7-30 days
  - Medium: 30-90 days
  - Low: 90+ days

## 🏆 Recognition

We appreciate security researchers who help keep Screenshot API safe!

### Hall of Fame

Security researchers who responsibly disclose vulnerabilities will be:
- ✅ Listed in our Security Hall of Fame (with permission)
- ✅ Credited in release notes
- ✅ Mentioned in CHANGELOG.md

## 🛡️ Security Best Practices

### For Users

When deploying Screenshot API:

1. **API Keys**
   - Use strong, randomly generated API keys
   - Rotate keys regularly (every 90 days recommended)
   - Never commit API keys to version control
   - Use environment variables for sensitive data

2. **Network Security**
   - Deploy behind HTTPS (always)
   - Use firewall rules to restrict access
   - Implement IP whitelisting if possible
   - Use VPC/private networks in cloud deployments

3. **Rate Limiting**
   - Configure appropriate rate limits
   - Monitor for unusual traffic patterns
   - Set up alerts for rate limit violations

4. **Monitoring**
   - Enable comprehensive logging
   - Monitor logs for suspicious activity
   - Set up alerts for authentication failures
   - Track API usage patterns

5. **Updates**
   - Keep dependencies up to date
   - Subscribe to security advisories
   - Apply security patches promptly
   - Test updates in staging first

### For Developers

When contributing to Screenshot API:

1. **Input Validation**
   - Validate all user inputs
   - Sanitize URLs and parameters
   - Use type hints and validation libraries
   - Never trust user input

2. **Authentication**
   - Use secure comparison for API keys
   - Implement proper session management
   - Hash sensitive data (use bcrypt)
   - Follow principle of least privilege

3. **Dependencies**
   - Keep dependencies updated
   - Review security advisories
   - Use `pip-audit` or similar tools
   - Pin dependency versions

4. **Code Review**
   - Review all code for security issues
   - Use static analysis tools
   - Follow secure coding guidelines
   - Test security controls

## 🔐 Known Security Considerations

### Current Implementation

1. **API Key Storage**
   - Currently stored in JSON file
   - **Recommendation:** Use hashed keys with bcrypt for production
   - **Mitigation:** Ensure `config/api_keys.json` is in `.gitignore`

2. **Rate Limiting**
   - In-memory rate limiting (resets on restart)
   - **Recommendation:** Use Redis for distributed rate limiting
   - **Mitigation:** Configure appropriate limits per tier

3. **Screenshot Content**
   - API can capture any publicly accessible URL
   - **Consideration:** May capture sensitive information
   - **Mitigation:** Implement URL blacklists if needed

4. **Resource Limits**
   - Browser processes consume significant resources
   - **Consideration:** Potential for resource exhaustion
   - **Mitigation:** Configure max instances and timeouts

### Recommended Production Hardening

```python
# 1. Hash API keys
import bcrypt

def hash_api_key(key: str) -> str:
    return bcrypt.hashpw(key.encode(), bcrypt.gensalt()).decode()

# 2. Use secrets for comparison
import secrets

def compare_keys(provided: str, stored: str) -> bool:
    return secrets.compare_digest(provided, stored)

# 3. Add request signing
import hmac
import hashlib

def verify_signature(payload: str, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return secrets.compare_digest(signature, expected)
```

## 📚 Security Resources

### External Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Flask Security](https://flask.palletsprojects.com/en/latest/security/)

### Tools

- **Static Analysis:** `bandit`, `pylint`
- **Dependency Scanning:** `pip-audit`, `safety`
- **Secret Scanning:** `gitleaks`, `trufflehog`
- **Container Scanning:** `trivy`, `grype`

## 📞 Contact

- **Security Issues:** security@yourapi.com
- **General Support:** support@yourapi.com
- **GitHub Issues:** [Report non-security bugs](../../issues)

## 📜 Disclosure Policy

We follow **Coordinated Vulnerability Disclosure**:

1. Researcher reports vulnerability privately
2. We acknowledge receipt within 48 hours
3. We investigate and develop a fix
4. We notify the researcher when fix is ready
5. We deploy the fix to production
6. We publicly disclose after 90 days (or sooner with agreement)
7. We credit the researcher (with permission)

## 🙏 Thank You

Thank you for helping keep Screenshot API and our users safe!

---

**Last Updated:** 2025-01-08
