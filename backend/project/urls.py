"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def homepage(request):
    """Simple homepage showing the project is running"""
    return JsonResponse(
        {
            "project": "CS Student Hub - Real-Time Tech Ecosystem Dashboard",
            "status": "Running Successfully! 🚀",
            "description": "A real-time web application aggregating content from GitHub, Reddit, Stack Overflow, and Hacker News",
            "api_endpoints": {
                "status": "/api/status/",
                "trending": "/api/trending/",
                "admin": "/admin/",
            },
            "websocket": "ws://localhost:8000/ws/dashboard/",
            "tech_stack": [
                "Django + Django Channels",
                "WebSocket for real-time updates",
                "PostgreSQL + Redis",
                "React frontend (coming next)",
                "Multiple API integrations",
            ],
            "next_steps": [
                "Create React frontend",
                "Integrate real APIs",
                "Add WebSocket live updates",
                "Deploy to AWS",
            ],
        }
    )


urlpatterns = [
    path("", homepage, name="homepage"),
    path("admin/", admin.site.urls),
    path("api/", include("dashboard.urls")),
]
