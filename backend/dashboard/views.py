from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api_clients import github_client, reddit_client, hackernews_client
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
                "reddit_posts": "/api/reddit/posts/",
                "reddit_subreddits": "/api/reddit/subreddits/",
                "hackernews_stories": "/api/hackernews/stories/",
            },
            "frontend_url": "http://localhost:3000",
            "status": "running",
        }
    )


@api_view(["GET"])
def api_status(request):
    """
    API status endpoint with GitHub, Reddit, and Hacker News API status
    """
    github_status = github_client.get_api_status()
    reddit_status = reddit_client.get_api_status()
    hackernews_status = hackernews_client.get_api_status()

    return Response(
        {
            "status": "running",
            "message": "CS Student Hub API is operational",
            "version": "1.0.0",
            "features": [
                "Real-time GitHub trending repositories",
                "Reddit programming community posts",
                "Hacker News top stories and tech trends",
                "Programming language statistics",
                "Multi-platform data aggregation",
            ],
            "apis": {
                "github": github_status,
                "reddit": reddit_status,
                "hackernews": hackernews_status,
            },
        }
    )


@api_view(["GET"])
def trending_topics(request):
    """
    Get trending topics from GitHub repositories, Reddit posts, and Hacker News stories
    """
    try:
        # Get trending repositories (last 7 days)
        trending_repos = github_client.get_trending_repositories(days=7, limit=20)

        # Try to get Reddit posts, but don't fail if Reddit is down
        reddit_posts = []
        reddit_error = None
        try:
            reddit_posts = reddit_client.get_programming_trending()
            logger.info(f"Successfully fetched {len(reddit_posts)} Reddit posts")
        except Exception as e:
            reddit_error = str(e)
            logger.error(
                f"Reddit API failed, continuing without Reddit data: {reddit_error}"
            )

        # Try to get Hacker News stories
        hackernews_stories = []
        hackernews_error = None
        try:
            hackernews_stories = hackernews_client.get_top_stories(limit=15)
            logger.info(
                f"Successfully fetched {len(hackernews_stories)} Hacker News stories"
            )
        except Exception as e:
            hackernews_error = str(e)
            logger.error(
                f"Hacker News API failed, continuing without HN data: {hackernews_error}"
            )

        # Get language statistics
        language_stats = github_client.get_language_stats()

        # Transform trending repos into trending topics format
        trending_topics = []

        # Add GitHub repos (adjust limit based on what other APIs returned)
        github_limit = (
            6
            if (reddit_posts and hackernews_stories)
            else 8 if (reddit_posts or hackernews_stories) else 15
        )
        for repo in trending_repos[:github_limit]:
            trending_topics.append(
                {
                    "id": f"github_{repo['id']}",
                    "keyword": repo["name"],
                    "platform": "GitHub",
                    "trend_score": min(repo["stars"] / 10, 100),
                    "posts_count": repo["forks"],
                    "description": (
                        repo["description"][:100] + "..."
                        if len(repo["description"]) > 100
                        else repo["description"]
                    ),
                    "language": repo["language"],
                    "url": repo["url"],
                    "stars": repo["stars"],
                    "type": "repository",
                }
            )

        # Add Reddit posts if available
        reddit_limit = 5 if hackernews_stories else 7
        for post in reddit_posts[:reddit_limit]:
            trending_topics.append(
                {
                    "id": f"reddit_{post['id']}",
                    "keyword": (
                        post["title"][:50] + "..."
                        if len(post["title"]) > 50
                        else post["title"]
                    ),
                    "platform": "Reddit",
                    "trend_score": min(post["score"] / 5, 100),
                    "posts_count": post["num_comments"],
                    "description": post.get(
                        "selftext", f"Discussion in r/{post['subreddit']}"
                    ),
                    "language": post.get("flair_text", "Discussion"),
                    "url": post["url"],
                    "score": post["score"],
                    "subreddit": post["subreddit"],
                    "type": "discussion",
                }
            )

        # Add Hacker News stories if available
        for story in hackernews_stories[:4]:
            trending_topics.append(
                {
                    "id": f"hackernews_{story['id']}",
                    "keyword": (
                        story["title"][:50] + "..."
                        if len(story["title"]) > 50
                        else story["title"]
                    ),
                    "platform": "Hacker News",
                    "trend_score": min(
                        story["score"] / 3, 100
                    ),  # HN scores are generally lower
                    "posts_count": story["descendants"],
                    "description": f"Tech news story by {story['by']}",
                    "language": "Tech News",
                    "url": (
                        story["url"]
                        if story["url"]
                        else f"https://news.ycombinator.com/item?id={story['id']}"
                    ),
                    "score": story["score"],
                    "author": story["by"],
                    "type": "news",
                }
            )

        # Platform status with detailed status for all platforms
        reddit_status = {
            "status": "connected" if reddit_posts and not reddit_error else "error",
            "last_fetch": "just now" if reddit_posts else "failed",
            "posts_count": len(reddit_posts),
            "subreddits_monitored": 7 if reddit_posts else 0,
        }
        if reddit_error:
            reddit_status["error"] = reddit_error[:100]

        hackernews_status = {
            "status": (
                "connected" if hackernews_stories and not hackernews_error else "error"
            ),
            "last_fetch": "just now" if hackernews_stories else "failed",
            "stories_count": len(hackernews_stories),
        }
        if hackernews_error:
            hackernews_status["error"] = hackernews_error[:100]

        platforms = {
            "github": {
                "status": "connected",
                "last_fetch": "just now",
                "repos_count": len(trending_repos),
                "rate_limit_remaining": github_client.get_api_status()["rate_limit"][
                    "remaining"
                ],
            },
            "reddit": reddit_status,
            "hackernews": hackernews_status,
        }

        return Response(
            {
                "trending_topics": trending_topics,
                "platforms": platforms,
                "language_stats": language_stats,
                "total_repos_analyzed": len(trending_repos),
                "total_posts_analyzed": len(reddit_posts),
                "total_stories_analyzed": len(hackernews_stories),
                "last_updated": "just now",
                "api_notes": {
                    "reddit": (
                        "Reddit API can be inconsistent" if reddit_error else None
                    ),
                    "hackernews": (
                        "Hacker News API is generally reliable"
                        if hackernews_error
                        else None
                    ),
                },
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
                    },
                    "reddit": {
                        "status": "error",
                        "last_fetch": "failed",
                        "error": "Failed due to GitHub error",
                    },
                    "hackernews": {
                        "status": "error",
                        "last_fetch": "failed",
                        "error": "Failed due to GitHub error",
                    },
                },
                "error": "Failed to fetch trending data",
                "message": "API is running but data fetch failed",
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


@api_view(["GET"])
def reddit_posts(request):
    """
    Get trending posts from Reddit programming communities
    """
    try:
        subreddit = request.GET.get("subreddit", "programming")
        sort = request.GET.get("sort", "hot")
        limit = int(request.GET.get("limit", 25))

        posts = reddit_client.get_subreddit_posts(
            subreddit=subreddit, sort=sort, limit=limit
        )

        return Response(
            {
                "posts": posts,
                "count": len(posts),
                "filters": {
                    "subreddit": subreddit,
                    "sort": sort,
                    "limit": limit,
                },
                "reddit_api_status": reddit_client.get_api_status(),
            }
        )

    except Exception as e:
        logger.error(f"Error fetching Reddit posts: {str(e)}")
        return Response(
            {"error": "Failed to fetch Reddit posts", "message": str(e)}, status=500
        )


@api_view(["GET"])
def reddit_subreddits(request):
    """
    Get statistics for popular programming subreddits
    """
    try:
        subreddit_stats = reddit_client.get_subreddit_stats()

        return Response(
            {
                "subreddit_stats": subreddit_stats,
                "total_subreddits": len(subreddit_stats),
                "reddit_api_status": reddit_client.get_api_status(),
            }
        )

    except Exception as e:
        logger.error(f"Error fetching subreddit stats: {str(e)}")
        return Response(
            {"error": "Failed to fetch subreddit statistics", "message": str(e)},
            status=500,
        )


@api_view(["GET"])
def hackernews_stories(request):
    """
    Get top stories from Hacker News
    """
    try:
        limit = int(request.GET.get("limit", 30))

        stories = hackernews_client.get_top_stories(limit=limit)

        return Response(
            {
                "stories": stories,
                "count": len(stories),
                "filters": {
                    "limit": limit,
                },
                "hackernews_api_status": hackernews_client.get_api_status(),
            }
        )

    except Exception as e:
        logger.error(f"Error fetching Hacker News stories: {str(e)}")
        return Response(
            {"error": "Failed to fetch Hacker News stories", "message": str(e)},
            status=500,
        )
