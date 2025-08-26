from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api_clients import github_client
import logging

logger = logging.getLogger(__name__)


def homepage(request):
    """
    Homepage view with project information
    """
    return JsonResponse(
        {
            "project": "CS Student Hub",
            "description": "Real-time tech ecosystem dashboard for CS students",
            "version": "1.0.0",
            "endpoints": {
                "api_status": "/api/status/",
                "trending": "/api/trending/",
                "github_repos": "/api/github/repos/",
                "github_languages": "/api/github/languages/",
            },
            "frontend_url": "http://localhost:3000",
            "status": "running",
        }
    )


@api_view(["GET"])
def api_status(request):
    """
    API status endpoint with GitHub API status
    """
    github_status = github_client.get_api_status()

    return Response(
        {
            "status": "running",
            "message": "CS Student Hub API is operational",
            "version": "1.0.0",
            "features": [
                "Real-time GitHub trending repositories",
                "Programming language statistics",
                "WebSocket support for live updates",
                "Multi-platform data aggregation",
            ],
            "github_api": github_status,
        }
    )


@api_view(["GET"])
def trending_topics(request):
    """
    Get trending topics from GitHub repositories
    """
    try:
        # Get trending repositories (last 7 days)
        trending_repos = github_client.get_trending_repositories(days=7, limit=20)

        # Get language statistics
        language_stats = github_client.get_language_stats()

        # Transform trending repos into trending topics format
        trending_topics = []
        for repo in trending_repos[:10]:  # Top 10 for trending topics
            trending_topics.append(
                {
                    "id": repo["id"],
                    "keyword": repo["name"],
                    "platform": "GitHub",
                    "trend_score": min(repo["stars"] / 10, 100),  # Scale stars to 0-100
                    "posts_count": repo["forks"],
                    "description": (
                        repo["description"][:100] + "..."
                        if len(repo["description"]) > 100
                        else repo["description"]
                    ),
                    "language": repo["language"],
                    "url": repo["url"],
                    "stars": repo["stars"],
                }
            )

        # Platform status
        platforms = {
            "github": {
                "status": "connected",
                "last_fetch": "just now",
                "repos_count": len(trending_repos),
                "rate_limit_remaining": github_client.get_api_status()["rate_limit"][
                    "remaining"
                ],
            },
            "reddit": {
                "status": "pending",
                "last_fetch": "not implemented",
                "posts_count": 0,
            },
            "stackoverflow": {
                "status": "pending",
                "last_fetch": "not implemented",
                "questions_count": 0,
            },
            "hackernews": {
                "status": "pending",
                "last_fetch": "not implemented",
                "stories_count": 0,
            },
        }

        return Response(
            {
                "trending_topics": trending_topics,
                "platforms": platforms,
                "language_stats": language_stats,
                "total_repos_analyzed": len(trending_repos),
                "last_updated": "just now",
            }
        )

    except Exception as e:
        logger.error(f"Error fetching trending data: {str(e)}")

        # Fallback to indicate API is working but data fetch failed
        return Response(
            {
                "trending_topics": [],
                "platforms": {
                    "github": {
                        "status": "error",
                        "last_fetch": "failed",
                        "error": str(e),
                    }
                },
                "error": "Failed to fetch trending data",
                "message": "API is running but GitHub data fetch failed",
            }
        )


@api_view(["GET"])
def github_repositories(request):
    """
    Get detailed GitHub trending repositories
    """
    try:
        language = request.GET.get("language", "")
        days = int(request.GET.get("days", 7))
        limit = int(request.GET.get("limit", 30))

        repos = github_client.get_trending_repositories(
            language=language, days=days, limit=limit
        )

        return Response(
            {
                "repositories": repos,
                "count": len(repos),
                "filters": {
                    "language": language or "all",
                    "days": days,
                    "limit": limit,
                },
                "github_api_status": github_client.get_api_status(),
            }
        )

    except Exception as e:
        logger.error(f"Error fetching GitHub repositories: {str(e)}")
        return Response(
            {"error": "Failed to fetch repositories", "message": str(e)}, status=500
        )


@api_view(["GET"])
def github_languages(request):
    """
    Get programming language statistics from GitHub
    """
    try:
        language_stats = github_client.get_language_stats()

        return Response(
            {
                "language_stats": language_stats,
                "total_languages": len(language_stats),
                "github_api_status": github_client.get_api_status(),
            }
        )

    except Exception as e:
        logger.error(f"Error fetching language stats: {str(e)}")
        return Response(
            {"error": "Failed to fetch language statistics", "message": str(e)},
            status=500,
        )
