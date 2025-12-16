import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def _set_test_env():
    """
    Ensure tests don't accidentally run with production settings and
    keep Celery from talking to a real broker unless explicitly desired.
    """
    os.environ.setdefault("DJANGO_ENV", "dev")
    os.environ.setdefault("DJANGO_DEBUG", "0")
    os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "1")
    os.environ.setdefault("CORS_ALLOW_ALL_ORIGINS", "1")
    yield


@pytest.fixture
def api_client():
    """
    DRF APIClient fixture. Imported lazily so Django is initialized first.
    """
    from rest_framework.test import APIClient

    return APIClient()
