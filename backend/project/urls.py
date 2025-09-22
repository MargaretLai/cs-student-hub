"""
URL configuration for project project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


def api_status(request):
    """API status endpoint"""
    return JsonResponse(
        {
            "project": "CS Student Hub - Real-Time Tech Ecosystem Dashboard",
            "status": "Running Successfully! 🚀",
            "description": "A real-time web application aggregating content from GitHub, Reddit, and Hacker News",
            "api_endpoints": {
                "status": "/api/status/",
                "trending": "/api/trending/",
                "admin": "/admin/",
            },
            "websocket": f"ws://{request.get_host()}/ws/dashboard/",
            "tech_stack": [
                "Django + Django Channels",
                "WebSocket for real-time updates",
                "PostgreSQL + Redis",
                "React frontend",
                "Multiple API integrations",
            ],
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("dashboard.urls")),
    path("api/status/", api_status, name="api_status"),
    # Serve React static files in production
    re_path(
        r"^.*$", TemplateView.as_view(template_name="index.html"), name="react_app"
    ),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
