import os
from celery import Celery

# Ensure Django settings are loaded for Celery workers
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("integratex")

# Read Celery settings from Django settings, using the "CELERY_" namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py in installed apps
app.autodiscover_tasks()
