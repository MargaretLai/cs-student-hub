"""
URL configuration for dashboard app
"""

from django.urls import path
from . import views

urlpatterns = [
    path("status/", views.api_status, name="api_status"),
    path("trending/", views.trending_topics, name="trending_topics"),
]
