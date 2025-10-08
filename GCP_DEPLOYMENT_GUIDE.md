# 🚀 Google Cloud Platform (GCP) Deployment Guide

## 📋 Overview

Deploy your Screenshot API to **Google Cloud Platform** for production-ready hosting before listing on RapidAPI.

**Why GCP?**
- ✅ **Reliable** - 99.95% uptime SLA
- ✅ **Scalable** - Auto-scaling built-in
- ✅ **Fast** - Global CDN & edge locations
- ✅ **Secure** - Enterprise-grade security
- ✅ **Cost-effective** - Pay only for what you use
- ✅ **RapidAPI Compatible** - Perfect integration

**Estimated Monthly Cost:**
- **Low traffic** (< 10K requests): **$20-50/month**
- **Medium traffic** (10K-100K): **$50-200/month**
- **High traffic** (100K+): **$200-500/month**

---

## 🎯 Deployment Options (Choose One)

### **Option 1: Cloud Run (RECOMMENDED)** ⭐
**Best for:** Serverless, auto-scaling, pay-per-use

**Pros:**
- ✅ Easiest to deploy
- ✅ Auto-scales to zero (save money)
- ✅ Built-in HTTPS
- ✅ No server management
- ✅ Perfect for APIs

**Cons:**
- ⚠️ Cold starts (1-2s delay after idle)
- ⚠️ 60-second timeout (OK for screenshots)

**Cost:** ~$0.40 per million requests + compute time

---

### **Option 2: App Engine**
**Best for:** Traditional PaaS, managed infrastructure

**Pros:**
- ✅ Easy deployment
- ✅ Auto-scaling
- ✅ Built-in monitoring
- ✅ No cold starts

**Cons:**
- ⚠️ More expensive than Cloud Run
- ⚠️ Less flexible

**Cost:** ~$50-200/month minimum

---

### **Option 3: Compute Engine (VM)**
**Best for:** Full control, custom configuration

**Pros:**
- ✅ Complete control
- ✅ Can optimize costs
- ✅ Persistent storage

**Cons:**
- ⚠️ Requires server management
- ⚠️ Manual scaling
- ⚠️ More complex

**Cost:** ~$30-100/month for small VM

---

## 🚀 RECOMMENDED: Cloud Run Deployment

### **Prerequisites**

1. **Google Cloud Account**
   - Go to: https://console.cloud.google.com
   - Sign up (free $300 credit for 90 days!)
   - Enable billing

2. **Install Google Cloud SDK**

**Windows:**
```powershell
# Download installer
https://cloud.google.com/sdk/docs/install

# Or use PowerShell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

**Mac/Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

3. **Initialize gcloud**
```bash
gcloud init
gcloud auth login
```

---

## 📦 Step 1: Prepare Your Application

### **1.1: Update requirements.txt**

Add production dependencies:

```txt
Flask==3.0.0
playwright==1.40.0
Werkzeug==3.0.1
python-dotenv==1.0.0
Pillow==10.1.0
requests==2.31.0
psutil==5.9.6
gunicorn==21.2.0
```

### **1.2: Create Production WSGI Server**

Create `wsgi.py`:

```python
"""
WSGI entry point for production
"""
from app import app

if __name__ == "__main__":
    app.run()
```

### **1.3: Create Dockerfile for Cloud Run**

Create `Dockerfile.cloudrun`:

```dockerfile
# Use official Python runtime
FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium firefox webkit
RUN playwright install-deps

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs screenshots cache baselines webhooks

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run with Gunicorn
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 120 wsgi:app
```

### **1.4: Create .dockerignore**

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.git/
.gitignore
*.md
tests/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.DS_Store
*.log
screenshots/*
cache/*
logs/*
baselines/*
webhooks/*
```

### **1.5: Create app.yaml (for App Engine alternative)**

```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT wsgi:app

instance_class: F2

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.65

env_variables:
  PYTHONUNBUFFERED: "1"
```

---

## 🚀 Step 2: Deploy to Cloud Run

### **2.1: Create GCP Project**

```bash
# Set project ID (choose unique name)
export PROJECT_ID="screenshot-api-prod"

# Create project
gcloud projects create $PROJECT_ID --name="Screenshot API"

# Set as active project
gcloud config set project $PROJECT_ID

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
```

### **2.2: Enable Required APIs**

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build
gcloud services enable cloudbuild.googleapis.com
```

### **2.3: Build and Deploy**

**Option A: Automatic Build & Deploy (Easiest)**

```bash
# Deploy directly from source
gcloud run deploy screenshot-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 120s \
  --max-instances 10 \
  --min-instances 1

# This will:
# 1. Build Docker image
# 2. Push to Container Registry
# 3. Deploy to Cloud Run
# 4. Give you a public URL
```

**Option B: Manual Build & Deploy (More Control)**

```bash
# 1. Build Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/screenshot-api

# 2. Deploy to Cloud Run
gcloud run deploy screenshot-api \
  --image gcr.io/$PROJECT_ID/screenshot-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 120s \
  --max-instances 10 \
  --min-instances 1
```

### **2.4: Get Your Public URL**

```bash
# Get service URL
gcloud run services describe screenshot-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'

# Output: https://screenshot-api-xxxxx-uc.a.run.app
```

**🎉 Your API is now live!**

---

## 🔒 Step 3: Configure Security & Environment

### **3.1: Set Environment Variables**

```bash
# Set environment variables
gcloud run services update screenshot-api \
  --update-env-vars \
    FLASK_ENV=production,\
    API_KEY_1=your-secure-key-1,\
    API_KEY_2=your-secure-key-2,\
    RATE_LIMIT_PER_MINUTE=60,\
    CACHE_DURATION_HOURS=24

# Or use secrets (more secure)
# Create secret
echo -n "your-api-key" | gcloud secrets create api-key --data-file=-

# Use secret in Cloud Run
gcloud run services update screenshot-api \
  --update-secrets API_KEY=api-key:latest
```

### **3.2: Configure Custom Domain (Optional)**

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service screenshot-api \
  --domain api.yourdomain.com \
  --region us-central1

# Follow instructions to update DNS records
```

### **3.3: Enable HTTPS (Automatic)**

Cloud Run automatically provides HTTPS with managed SSL certificates. No configuration needed! ✅

---

## 📊 Step 4: Monitoring & Logging

### **4.1: View Logs**

```bash
# Stream logs
gcloud run services logs tail screenshot-api \
  --region us-central1

# View in Cloud Console
# https://console.cloud.google.com/run
```

### **4.2: Set Up Monitoring**

**Cloud Console:**
1. Go to: https://console.cloud.google.com/monitoring
2. Create dashboard
3. Add metrics:
   - Request count
   - Response time
   - Error rate
   - CPU usage
   - Memory usage

### **4.3: Set Up Alerts**

```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=5 \
  --condition-threshold-duration=300s
```

---

## 💰 Step 5: Cost Optimization

### **5.1: Configure Auto-Scaling**

```bash
# Update scaling settings
gcloud run services update screenshot-api \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80
```

**Scaling Strategy:**
- **min-instances: 0** - Scale to zero when idle (save money)
- **min-instances: 1** - Always ready (no cold starts, costs more)
- **max-instances: 10** - Prevent runaway costs

### **5.2: Set Budget Alerts**

```bash
# Create budget
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Screenshot API Budget" \
  --budget-amount=100USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90
```

### **5.3: Estimated Costs**

**Cloud Run Pricing:**
```
CPU: $0.00002400 per vCPU-second
Memory: $0.00000250 per GiB-second
Requests: $0.40 per million requests

Example (10K requests/month, 10s avg):
- CPU: 10,000 × 10s × 2 vCPU × $0.000024 = $4.80
- Memory: 10,000 × 10s × 2GB × $0.0000025 = $0.50
- Requests: 10,000 × $0.0000004 = $0.004
Total: ~$5.30/month
```

---

## 🔗 Step 6: Integrate with RapidAPI

### **6.1: Update API for RapidAPI**

Add RapidAPI middleware to `app.py`:

```python
from functools import wraps
from flask import request, jsonify

def rapidapi_auth(f):
    """RapidAPI authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for RapidAPI proxy secret
        rapidapi_secret = request.headers.get('X-RapidAPI-Proxy-Secret')
        
        if rapidapi_secret:
            # Validate against your RapidAPI secret
            if rapidapi_secret == os.getenv('RAPIDAPI_SECRET'):
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Invalid RapidAPI credentials'}), 401
        
        # Fallback to regular API key auth
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key or not auth_service.validate_key(api_key):
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# Apply to endpoints
@app.route('/screenshot')
@rapidapi_auth
def screenshot():
    # Your existing code
    pass
```

### **6.2: Add CORS for RapidAPI**

```python
from flask_cors import CORS

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://rapidapi.com",
            "https://*.rapidapi.com",
            "https://rapidapi.com/*"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": [
            "Content-Type",
            "X-RapidAPI-Key",
            "X-RapidAPI-Host",
            "X-RapidAPI-Proxy-Secret"
        ]
    }
})
```

### **6.3: Add Rate Limit Headers**

```python
@app.after_request
def add_headers(response):
    """Add RapidAPI-compatible headers"""
    response.headers['X-RateLimit-Limit'] = '1000'
    response.headers['X-RateLimit-Remaining'] = '999'
    response.headers['X-RateLimit-Reset'] = str(int(time.time()) + 3600)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
```

### **6.4: Redeploy with Changes**

```bash
# Redeploy
gcloud run deploy screenshot-api \
  --source . \
  --platform managed \
  --region us-central1
```

---

## 🎯 Step 7: Test Your Deployment

### **7.1: Basic Health Check**

```bash
# Get your URL
URL=$(gcloud run services describe screenshot-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

# Test health endpoint
curl $URL/health

# Test screenshot endpoint
curl "$URL/screenshot?url=https://example.com&api_key=demo-key-12345" \
  --output test.png
```

### **7.2: Load Testing**

```bash
# Install Apache Bench
# Windows: Download from Apache website
# Mac: brew install httpd
# Linux: sudo apt install apache2-utils

# Run load test (100 requests, 10 concurrent)
ab -n 100 -c 10 "$URL/health"
```

### **7.3: Monitor Performance**

```bash
# Check metrics
gcloud run services describe screenshot-api \
  --platform managed \
  --region us-central1 \
  --format yaml
```

---

## 📋 Step 8: RapidAPI Integration

### **8.1: Add API to RapidAPI**

1. **Go to RapidAPI Provider Dashboard**
   - https://rapidapi.com/provider/dashboard

2. **Add New API**
   - Name: "Professional Screenshot API"
   - Base URL: `https://screenshot-api-xxxxx-uc.a.run.app`
   - Category: Tools / Data

3. **Configure Authentication**
   - Type: Header
   - Header Name: `X-API-Key`
   - Test with your demo key

4. **Upload OpenAPI Spec**
   - Use the spec from RAPIDAPI_GUIDE.md
   - Update base URL to your Cloud Run URL

5. **Test All Endpoints**
   - Use RapidAPI testing interface
   - Verify all features work

6. **Submit for Review**
   - RapidAPI reviews in 24-48 hours
   - Fix any issues they find

---

## 🚀 Step 9: Go Live!

### **9.1: Pre-Launch Checklist**

- [ ] API deployed to Cloud Run
- [ ] HTTPS working (automatic)
- [ ] All endpoints tested
- [ ] Monitoring configured
- [ ] Budget alerts set
- [ ] RapidAPI integration tested
- [ ] Documentation complete
- [ ] Pricing tiers configured

### **9.2: Launch!**

```bash
# Final deployment
gcloud run deploy screenshot-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --min-instances 1

# Get final URL
echo "Your API is live at:"
gcloud run services describe screenshot-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

---

## 🔧 Maintenance & Updates

### **Update Deployment**

```bash
# Deploy new version
gcloud run deploy screenshot-api --source .

# Rollback if needed
gcloud run services update-traffic screenshot-api \
  --to-revisions=PREVIOUS_REVISION=100
```

### **View All Revisions**

```bash
gcloud run revisions list \
  --service screenshot-api \
  --region us-central1
```

### **Scale Manually**

```bash
# Scale up
gcloud run services update screenshot-api \
  --min-instances 3 \
  --max-instances 20

# Scale down
gcloud run services update screenshot-api \
  --min-instances 0 \
  --max-instances 5
```

---

## 💡 Pro Tips

### **1. Use Cloud CDN**
```bash
# Enable Cloud CDN for static assets
gcloud compute backend-services update screenshot-api \
  --enable-cdn
```

### **2. Use Cloud Storage for Screenshots**
```python
from google.cloud import storage

def save_to_gcs(screenshot_data, filename):
    client = storage.Client()
    bucket = client.bucket('screenshot-api-storage')
    blob = bucket.blob(filename)
    blob.upload_from_string(screenshot_data)
    return blob.public_url
```

### **3. Use Cloud SQL for Database**
```bash
# Create PostgreSQL instance
gcloud sql instances create screenshot-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1
```

### **4. Use Cloud Scheduler for Cleanup**
```bash
# Schedule daily cleanup
gcloud scheduler jobs create http cleanup-old-screenshots \
  --schedule="0 2 * * *" \
  --uri="https://your-api.run.app/cleanup" \
  --http-method=POST
```

---

## 📊 Monitoring Dashboard

**Key Metrics to Track:**

1. **Request Rate** - Requests per second
2. **Response Time** - P50, P95, P99 latency
3. **Error Rate** - 4xx and 5xx errors
4. **CPU Usage** - Average and peak
5. **Memory Usage** - Average and peak
6. **Cost** - Daily spend

**Set Up Alerts For:**
- Error rate > 5%
- Response time > 30s
- CPU > 80%
- Memory > 90%
- Daily cost > $10

---

## 🎉 Success Checklist

- [ ] GCP account created with billing enabled
- [ ] Cloud SDK installed and configured
- [ ] Application containerized with Dockerfile
- [ ] Deployed to Cloud Run successfully
- [ ] HTTPS working (automatic)
- [ ] Custom domain configured (optional)
- [ ] Environment variables set
- [ ] Monitoring and logging enabled
- [ ] Budget alerts configured
- [ ] RapidAPI integration tested
- [ ] API listed on RapidAPI
- [ ] First test customer! 🎉

---

## 🆘 Troubleshooting

### **Issue: Build Fails**
```bash
# Check build logs
gcloud builds log --region=us-central1

# Common fix: Update Dockerfile
```

### **Issue: Timeout Errors**
```bash
# Increase timeout
gcloud run services update screenshot-api --timeout 300s
```

### **Issue: Out of Memory**
```bash
# Increase memory
gcloud run services update screenshot-api --memory 4Gi
```

### **Issue: Cold Starts**
```bash
# Keep 1 instance warm
gcloud run services update screenshot-api --min-instances 1
```

---

## 📞 Support Resources

**Google Cloud:**
- Documentation: https://cloud.google.com/run/docs
- Support: https://cloud.google.com/support
- Community: https://stackoverflow.com/questions/tagged/google-cloud-run

**Your API:**
- Landing Page: https://your-api.run.app
- Documentation: https://your-api.run.app/docs
- Dashboard: https://your-api.run.app/dashboard

---

## 🎯 Next Steps

1. ✅ Deploy to GCP Cloud Run
2. ✅ Test all endpoints
3. ✅ List on RapidAPI
4. ✅ Start marketing
5. ✅ Get first customers!
6. 💰 Make money!

---

**You're ready to deploy! Let's make this happen! 🚀**

**Questions? Need help with deployment? Just ask!**
