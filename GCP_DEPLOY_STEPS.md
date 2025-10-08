# 🚀 GCP Cloud Run Deployment - Step by Step

## 📋 Prerequisites

✅ Google Cloud SDK installed  
✅ GCP account with billing enabled  
✅ Project created in GCP Console

---

## 🎯 Quick Deploy (Automated)

**Option 1: Use the deployment script**

```bash
# Just double-click or run:
DEPLOY_TO_GCP.bat
```

The script will:
1. Check authentication
2. Enable required APIs
3. Build Docker image
4. Deploy to Cloud Run
5. Give you the live URL

**Done in 5-10 minutes!** ✅

---

## 📝 Manual Deployment (Step-by-Step)

### Step 1: Open Google Cloud SDK Shell

Find and open **"Google Cloud SDK Shell"** from your Start Menu

Or add gcloud to PATH:
```
C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin
```

### Step 2: Authenticate

```bash
gcloud auth login
```

This will open your browser to log in to Google Cloud.

### Step 3: Set Your Project

```bash
# List your projects
gcloud projects list

# Set your project (replace with your project ID)
gcloud config set project YOUR_PROJECT_ID
```

**Example:**
```bash
gcloud config set project webshotify-prod
```

### Step 4: Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 5: Navigate to Your Project

```bash
cd "I:/API PNG"
```

### Step 6: Deploy to Cloud Run

```bash
gcloud run deploy webshotify \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 120s \
  --max-instances 10 \
  --min-instances 0 \
  --port 8080
```

**What this does:**
- Builds your Docker image automatically
- Pushes to Google Container Registry
- Deploys to Cloud Run
- Gives you a public HTTPS URL

**This will take 5-10 minutes** ⏱️

### Step 7: Get Your Service URL

```bash
gcloud run services describe webshotify \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

**Output example:**
```
https://webshotify-xxxxx-uc.a.run.app
```

### Step 8: Test Your Deployment

```bash
# Test health endpoint
curl https://webshotify-xxxxx-uc.a.run.app/health

# Or open in browser
start https://webshotify-xxxxx-uc.a.run.app
```

---

## 🔧 Configuration

### Set Environment Variables

```bash
gcloud run services update webshotify \
  --platform managed \
  --region us-central1 \
  --update-env-vars \
    FLASK_ENV=production,\
    RATE_LIMIT_PER_MINUTE=60,\
    CACHE_DURATION_HOURS=24
```

### Set Secrets (for API keys)

```bash
# Create secret
echo -n "your-secure-api-key" | gcloud secrets create api-key-1 --data-file=-

# Use in Cloud Run
gcloud run services update webshotify \
  --update-secrets API_KEY_1=api-key-1:latest
```

### Configure Custom Domain

```bash
gcloud run domain-mappings create \
  --service webshotify \
  --domain api.yourdomain.com \
  --region us-central1
```

Then update your DNS records as instructed.

---

## 📊 Monitoring

### View Logs

```bash
# Stream logs in real-time
gcloud run services logs tail webshotify --region us-central1

# View recent logs
gcloud run services logs read webshotify --region us-central1 --limit 50
```

### View Metrics

Go to: https://console.cloud.google.com/run

Click on your service → **Metrics** tab

You'll see:
- Request count
- Request latency
- Container CPU utilization
- Container memory utilization
- Container instance count

---

## 💰 Cost Optimization

### Current Configuration

```
Memory: 2 GiB
CPU: 2
Min instances: 0 (scales to zero)
Max instances: 10
Timeout: 120s
```

### Estimated Costs

**Low traffic (1,000 requests/month):**
- ~$5-10/month

**Medium traffic (10,000 requests/month):**
- ~$20-50/month

**High traffic (100,000 requests/month):**
- ~$100-200/month

### Reduce Costs

```bash
# Scale to zero when idle (already configured)
gcloud run services update webshotify \
  --min-instances 0

# Reduce memory if not needed
gcloud run services update webshotify \
  --memory 1Gi

# Reduce CPU
gcloud run services update webshotify \
  --cpu 1
```

---

## 🔄 Update Deployment

### Deploy New Version

```bash
# Make your code changes, then:
gcloud run deploy webshotify \
  --source . \
  --region us-central1
```

### Rollback to Previous Version

```bash
# List revisions
gcloud run revisions list --service webshotify --region us-central1

# Rollback
gcloud run services update-traffic webshotify \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

---

## 🔒 Security

### Enable Authentication (Optional)

```bash
# Require authentication
gcloud run services update webshotify \
  --no-allow-unauthenticated \
  --region us-central1
```

### Set Up VPC Connector (Optional)

For private database access:

```bash
gcloud compute networks vpc-access connectors create webshotify-connector \
  --region us-central1 \
  --range 10.8.0.0/28

gcloud run services update webshotify \
  --vpc-connector webshotify-connector \
  --region us-central1
```

---

## 🎯 Production Checklist

Before going live:

- [ ] Test all endpoints
- [ ] Configure environment variables
- [ ] Set up monitoring and alerts
- [ ] Configure custom domain (optional)
- [ ] Set up budget alerts
- [ ] Enable Cloud Armor (DDoS protection)
- [ ] Configure Cloud CDN (optional)
- [ ] Set up backup strategy
- [ ] Document your deployment
- [ ] Test with production API keys

---

## 🆘 Troubleshooting

### Issue: Build Fails

```bash
# Check build logs
gcloud builds log --region us-central1

# Common fix: Increase build timeout
gcloud run deploy webshotify \
  --source . \
  --timeout 600s
```

### Issue: Service Crashes

```bash
# Check logs
gcloud run services logs read webshotify --region us-central1 --limit 100

# Common fixes:
# 1. Increase memory
gcloud run services update webshotify --memory 4Gi

# 2. Increase timeout
gcloud run services update webshotify --timeout 300s
```

### Issue: Slow Performance

```bash
# Increase CPU and memory
gcloud run services update webshotify \
  --cpu 4 \
  --memory 4Gi

# Keep instances warm
gcloud run services update webshotify \
  --min-instances 1
```

### Issue: Out of Memory

```bash
# Check memory usage in logs
gcloud run services logs read webshotify --region us-central1 | grep -i memory

# Increase memory
gcloud run services update webshotify --memory 4Gi
```

---

## 📞 Support

**GCP Documentation:**
- Cloud Run: https://cloud.google.com/run/docs
- Troubleshooting: https://cloud.google.com/run/docs/troubleshooting

**Webshotify:**
- GitHub Issues: https://github.com/09Catho/webshotify/issues
- Documentation: https://github.com/09Catho/webshotify

---

## 🎉 Success!

Your Webshotify API is now:
- ✅ Live on GCP Cloud Run
- ✅ Auto-scaling (0 to 10 instances)
- ✅ HTTPS enabled (automatic)
- ✅ Production-ready
- ✅ Globally available

**Service URL:** `https://webshotify-xxxxx-uc.a.run.app`

**Next Steps:**
1. Test your API
2. Configure monitoring
3. Set up custom domain
4. List on RapidAPI
5. Start making money! 💰

---

**Congratulations! You're in production!** 🚀🎉
