import requests
from django.conf import settings
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class GitHubAPIClient:
    """
    GitHub API client for fetching trending repositories, languages, and developer data
    """

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = settings.GITHUB_TOKEN
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CS-Student-Hub/1.0",
        }

        if not self.token:
            logger.warning("GITHUB_TOKEN not configured in settings")

    def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Make authenticated request to GitHub API with error handling
        """
        if not self.token:
            logger.error("No GitHub token available")
            return None

        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.get(
                url, headers=self.headers, params=params, timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                logger.error(
                    f"GitHub API rate limit exceeded. Reset time: {response.headers.get('x-ratelimit-reset')}"
                )
                return None
            else:
                logger.error(
                    f"GitHub API error {response.status_code}: {response.text}"
                )
                return None

        except requests.RequestException as e:
            logger.error(f"GitHub API request failed: {str(e)}")
            return None

    def get_trending_repositories(
        self, language: str = "", days: int = 7, limit: int = 30
    ) -> List[Dict]:
        """
        Get trending repositories from the last N days
        """
        # Calculate date for search (e.g., created:>2024-01-01)
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Build search query
        query_parts = [f"created:>{since_date}"]
        if language:
            query_parts.append(f"language:{language}")

        query = " ".join(query_parts)

        params = {"q": query, "sort": "stars", "order": "desc", "per_page": limit}

        data = self._make_request("search/repositories", params)
        if not data or "items" not in data:
            return []

        trending_repos = []
        for repo in data["items"]:
            trending_repos.append(
                {
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo["description"] or "No description available",
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo["language"] or "Unknown",
                    "url": repo["html_url"],
                    "created_at": repo["created_at"],
                    "updated_at": repo["updated_at"],
                    "topics": repo.get("topics", []),
                }
            )

        return trending_repos

    def get_language_stats(self) -> Dict:
        """
        Get popular programming language statistics
        """
        # Get trending repos for different languages
        languages = [
            "Python",
            "JavaScript",
            "TypeScript",
            "Java",
            "Go",
            "Rust",
            "C++",
            "C#",
        ]
        language_stats = {}

        for lang in languages:
            repos = self.get_trending_repositories(language=lang, days=30, limit=10)
            if repos:
                total_stars = sum(repo["stars"] for repo in repos)
                language_stats[lang] = {
                    "repos_count": len(repos),
                    "total_stars": total_stars,
                    "avg_stars": total_stars // len(repos) if repos else 0,
                    "top_repo": repos[0] if repos else None,
                }

        return language_stats

    def get_api_status(self) -> Dict:
        """
        Check GitHub API status and rate limits
        """
        data = self._make_request("rate_limit")
        if not data:
            return {"status": "error", "message": "Failed to connect to GitHub API"}

        core = data.get("rate", {})
        return {
            "status": "connected",
            "rate_limit": {
                "limit": core.get("limit", 0),
                "remaining": core.get("remaining", 0),
                "reset_time": core.get("reset", 0),
            },
            "message": f"Connected to GitHub API. {core.get('remaining', 0)}/{core.get('limit', 0)} requests remaining",
        }


# Initialize GitHub client
github_client = GitHubAPIClient()
