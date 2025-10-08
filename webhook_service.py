"""
Webhook Service
Handles async job notifications and callbacks
"""

import requests
import hashlib
import hmac
import json
from datetime import datetime
from pathlib import Path
import threading
import time


class WebhookService:
    """Service for managing webhooks and async job notifications"""
    
    def __init__(self):
        self.webhooks_dir = Path('webhooks')
        self.webhooks_dir.mkdir(exist_ok=True)
        self.jobs = {}  # In-memory job tracking
        self.job_file = self.webhooks_dir / 'jobs.json'
        self.load_jobs()
    
    def load_jobs(self):
        """Load jobs from persistent storage"""
        if self.job_file.exists():
            try:
                with open(self.job_file, 'r') as f:
                    self.jobs = json.load(f)
            except Exception as e:
                print(f"Error loading jobs: {e}")
                self.jobs = {}
    
    def save_jobs(self):
        """Save jobs to persistent storage"""
        try:
            with open(self.job_file, 'w') as f:
                json.dump(self.jobs, f, indent=2)
        except Exception as e:
            print(f"Error saving jobs: {e}")
    
    def create_job(self, job_type, params, webhook_url=None, webhook_secret=None):
        """
        Create a new async job
        
        Args:
            job_type (str): Type of job (screenshot, batch, pdf, etc.)
            params (dict): Job parameters
            webhook_url (str): URL to call when job completes
            webhook_secret (str): Secret for webhook signature
        
        Returns:
            str: Job ID
        """
        import uuid
        
        job_id = str(uuid.uuid4())
        
        job = {
            'job_id': job_id,
            'job_type': job_type,
            'status': 'pending',
            'params': params,
            'webhook_url': webhook_url,
            'webhook_secret': webhook_secret,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'result': None,
            'error': None,
            'attempts': 0
        }
        
        self.jobs[job_id] = job
        self.save_jobs()
        
        return job_id
    
    def update_job_status(self, job_id, status, result=None, error=None):
        """
        Update job status
        
        Args:
            job_id (str): Job ID
            status (str): New status (pending, processing, completed, failed)
            result (dict): Job result data
            error (str): Error message if failed
        """
        if job_id not in self.jobs:
            return False
        
        self.jobs[job_id]['status'] = status
        self.jobs[job_id]['updated_at'] = datetime.now().isoformat()
        
        if result:
            self.jobs[job_id]['result'] = result
        
        if error:
            self.jobs[job_id]['error'] = error
        
        self.save_jobs()
        
        # Trigger webhook if job completed or failed
        if status in ['completed', 'failed']:
            self.trigger_webhook(job_id)
        
        return True
    
    def get_job(self, job_id):
        """Get job details"""
        return self.jobs.get(job_id)
    
    def trigger_webhook(self, job_id):
        """
        Trigger webhook notification for completed job
        
        Args:
            job_id (str): Job ID
        """
        job = self.jobs.get(job_id)
        if not job or not job.get('webhook_url'):
            return
        
        webhook_url = job['webhook_url']
        webhook_secret = job.get('webhook_secret')
        
        # Prepare payload
        payload = {
            'job_id': job_id,
            'job_type': job['job_type'],
            'status': job['status'],
            'created_at': job['created_at'],
            'completed_at': job['updated_at'],
            'result': job.get('result'),
            'error': job.get('error')
        }
        
        # Send webhook in background thread
        thread = threading.Thread(
            target=self._send_webhook,
            args=(webhook_url, payload, webhook_secret, job_id)
        )
        thread.daemon = True
        thread.start()
    
    def _send_webhook(self, url, payload, secret, job_id, max_retries=3):
        """
        Send webhook with retries
        
        Args:
            url (str): Webhook URL
            payload (dict): Payload data
            secret (str): Webhook secret
            job_id (str): Job ID
            max_retries (int): Maximum retry attempts
        """
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Job-ID': job_id,
            'X-Webhook-Timestamp': str(int(time.time()))
        }
        
        # Add signature if secret provided
        if secret:
            signature = self._generate_signature(payload, secret)
            headers['X-Webhook-Signature'] = signature
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    # Webhook delivered successfully
                    self.jobs[job_id]['webhook_delivered'] = True
                    self.jobs[job_id]['webhook_delivered_at'] = datetime.now().isoformat()
                    self.save_jobs()
                    return
                
            except Exception as e:
                print(f"Webhook delivery failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        # All attempts failed
        self.jobs[job_id]['webhook_failed'] = True
        self.jobs[job_id]['attempts'] = max_retries
        self.save_jobs()
    
    def _generate_signature(self, payload, secret):
        """
        Generate HMAC signature for webhook payload
        
        Args:
            payload (dict): Payload data
            secret (str): Webhook secret
        
        Returns:
            str: HMAC signature
        """
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify_webhook_signature(self, payload, signature, secret):
        """
        Verify webhook signature
        
        Args:
            payload (dict): Payload data
            signature (str): Provided signature
            secret (str): Webhook secret
        
        Returns:
            bool: True if signature is valid
        """
        expected_signature = self._generate_signature(payload, secret)
        return hmac.compare_digest(signature, expected_signature)
    
    def process_job_async(self, job_id, job_function, *args, **kwargs):
        """
        Process job asynchronously in background thread
        
        Args:
            job_id (str): Job ID
            job_function (callable): Function to execute
            *args, **kwargs: Arguments for job function
        """
        def worker():
            try:
                # Update status to processing
                self.update_job_status(job_id, 'processing')
                
                # Execute job
                result = job_function(*args, **kwargs)
                
                # Update status to completed
                self.update_job_status(job_id, 'completed', result=result)
                
            except Exception as e:
                # Update status to failed
                self.update_job_status(job_id, 'failed', error=str(e))
        
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
    
    def get_job_status(self, job_id):
        """
        Get job status for API response
        
        Args:
            job_id (str): Job ID
        
        Returns:
            dict: Job status information
        """
        job = self.get_job(job_id)
        if not job:
            return None
        
        return {
            'job_id': job_id,
            'status': job['status'],
            'job_type': job['job_type'],
            'created_at': job['created_at'],
            'updated_at': job['updated_at'],
            'result': job.get('result'),
            'error': job.get('error'),
            'webhook_delivered': job.get('webhook_delivered', False)
        }
    
    def cleanup_old_jobs(self, max_age_hours=48):
        """
        Remove old completed/failed jobs
        
        Args:
            max_age_hours (int): Maximum age in hours
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        jobs_to_remove = []
        for job_id, job in self.jobs.items():
            if job['status'] in ['completed', 'failed']:
                updated_at = datetime.fromisoformat(job['updated_at'])
                if updated_at < cutoff_time:
                    jobs_to_remove.append(job_id)
        
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
        
        if jobs_to_remove:
            self.save_jobs()
        
        return len(jobs_to_remove)
