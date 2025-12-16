from django.urls import path

from .test_views import OrgContextView

urlpatterns = [
    path("test-org-context/", OrgContextView.as_view()),
]
