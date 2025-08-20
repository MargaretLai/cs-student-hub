"""
Views for dashboard app
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


@api_view(["GET"])
def api_status(request):
    """
    Check if the API is working
    """
    return Response(
        {
            "status": "success",
            "message": "CS Student Hub API is running!",
            "version": "1.0",
            "features": [
                "Real-time WebSocket updates",
                "GitHub API integration",
                "Reddit API integration",
                "Stack Overflow API integration",
                "Hacker News API integration",
            ],
        }
    )


@api_view(["GET"])
def trending_topics(request):
    """
    Get trending topics (mock data for now)
    """
    # Mock data - we'll replace this with real API data later
    mock_data = {
        "status": "success",
        "last_updated": "2025-08-20T20:25:00Z",
        "trending_topics": [
            {
                "id": 1,
                "keyword": "React",
                "platform": "github",
                "trend_score": 95,
                "posts_count": 156,
                "description": "JavaScript library for building user interfaces",
            },
            {
                "id": 2,
                "keyword": "Python Django",
                "platform": "stackoverflow",
                "trend_score": 87,
                "posts_count": 89,
                "description": "Web framework questions trending",
            },
            {
                "id": 3,
                "keyword": "AI/ML Jobs",
                "platform": "reddit",
                "trend_score": 92,
                "posts_count": 234,
                "description": "Machine learning career discussions",
            },
            {
                "id": 4,
                "keyword": "TypeScript",
                "platform": "hackernews",
                "trend_score": 78,
                "posts_count": 67,
                "description": "Strongly typed JavaScript discussions",
            },
        ],
        "platforms": {
            "github": {"status": "active", "last_fetch": "2025-08-20T20:24:30Z"},
            "reddit": {"status": "active", "last_fetch": "2025-08-20T20:24:45Z"},
            "stackoverflow": {"status": "active", "last_fetch": "2025-08-20T20:24:15Z"},
            "hackernews": {"status": "active", "last_fetch": "2025-08-20T20:24:50Z"},
        },
    }

    return Response(mock_data)
