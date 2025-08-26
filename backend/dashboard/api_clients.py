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


class RedditAPIClient:
    """
    Reddit API client for fetching trending posts from programming subreddits
    No authentication required for public data
    """

    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {
            "User-Agent": "python:cs-student-hub:v1.0.0 (by /u/csstudent)",
            "Accept": "application/json",
        }

    def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Make request to Reddit API with error handling
        """
        try:
            # Ensure endpoint ends with .json
            if not endpoint.endswith(".json"):
                endpoint += ".json"

            url = f"{self.base_url}/{endpoint.lstrip('/')}"

            response = requests.get(
                url, headers=self.headers, params=params, timeout=15
            )

            logger.info(f"Reddit API request: {url} - Status: {response.status_code}")

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"Reddit API error {response.status_code}: {response.text[:200]}"
                )
                return None

        except requests.RequestException as e:
            logger.error(f"Reddit API request failed: {str(e)}")
            return None

    def get_subreddit_posts(
        self, subreddit: str = "programming", sort: str = "hot", limit: int = 25
    ) -> List[Dict]:
        """
        Get posts from a specific subreddit
        sort options: hot, new, top, rising
        """
        # Fix: construct the endpoint correctly with r/ prefix
        endpoint = f"r/{subreddit}/{sort}"
        params = {"limit": min(limit, 100)}  # Reddit max is 100

        data = self._make_request(endpoint, params)
        if not data or "data" not in data:
            logger.error(f"No data received from Reddit for r/{subreddit}")
            return []

        if "children" not in data["data"]:
            logger.error(f"No children in Reddit data for r/{subreddit}")
            return []

        posts = []
        for item in data["data"]["children"]:
            try:
                post_data = item["data"]

                # Skip pinned/stickied posts and ads
                if post_data.get("stickied", False) or post_data.get(
                    "is_sponsored", False
                ):
                    continue

                # Skip deleted/removed posts
                if post_data.get("removed_by_category"):
                    continue

                posts.append(
                    {
                        "id": post_data.get("id", ""),
                        "title": post_data.get("title", "No title"),
                        "author": post_data.get("author", "unknown"),
                        "subreddit": post_data.get("subreddit", subreddit),
                        "score": post_data.get("score", 0),
                        "upvote_ratio": post_data.get("upvote_ratio", 0),
                        "num_comments": post_data.get("num_comments", 0),
                        "url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "external_url": post_data.get("url", ""),
                        "selftext": (
                            (post_data.get("selftext", "")[:200] + "...")
                            if post_data.get("selftext", "")
                            else ""
                        ),
                        "created_utc": post_data.get("created_utc", 0),
                        "flair_text": post_data.get("link_flair_text", ""),
                        "domain": post_data.get("domain", ""),
                        "is_self": post_data.get("is_self", False),
                    }
                )

            except Exception as e:
                logger.warning(f"Error processing Reddit post: {str(e)}")
                continue

        logger.info(f"Successfully parsed {len(posts)} posts from r/{subreddit}")
        return posts

    def get_programming_trending(self) -> List[Dict]:
        """
        Get trending posts from multiple programming subreddits with better error handling
        """
        subreddits = [
            "programming",
            "webdev",
            "Python",
            "javascript",
            "MachineLearning",
            "cscareerquestions",
            "learnprogramming",
        ]

        all_posts = []
        successful_subreddits = []
        failed_subreddits = []

        for subreddit in subreddits:
            try:
                posts = self.get_subreddit_posts(subreddit, "hot", 8)

                if posts:  # If we got posts successfully
                    successful_subreddits.append(subreddit)
                    # Add subreddit info and filter for quality posts
                    for post in posts:
                        if post["score"] >= 5:  # Lower threshold for more posts
                            post["source_subreddit"] = subreddit
                            all_posts.append(post)
                else:
                    failed_subreddits.append(f"{subreddit} (no posts)")

            except Exception as e:
                logger.error(f"Failed to get posts from r/{subreddit}: {str(e)}")
                failed_subreddits.append(f"{subreddit} (error: {str(e)[:50]})")

        logger.info(
            f"Reddit trending: {len(successful_subreddits)} successful, {len(failed_subreddits)} failed"
        )
        logger.info(f"Successful subreddits: {successful_subreddits}")
        if failed_subreddits:
            logger.warning(f"Failed subreddits: {failed_subreddits}")

        # Sort by score and return top posts
        all_posts.sort(key=lambda x: x["score"], reverse=True)
        result = all_posts[:25]

        logger.info(f"Returning {len(result)} total Reddit posts")
        return result

    def get_subreddit_stats(self) -> Dict:
        """
        Get statistics for popular programming subreddits
        """
        subreddits = [
            "programming",
            "webdev",
            "Python",
            "javascript",
            "MachineLearning",
        ]
        stats = {}

        for subreddit in subreddits:
            posts = self.get_subreddit_posts(subreddit, "hot", 20)
            if posts:
                total_score = sum(post["score"] for post in posts)
                total_comments = sum(post["num_comments"] for post in posts)

                stats[subreddit] = {
                    "posts_count": len(posts),
                    "total_score": total_score,
                    "total_comments": total_comments,
                    "avg_score": total_score // len(posts) if posts else 0,
                    "top_post": posts[0] if posts else None,
                }

        return stats

    def get_api_status(self) -> Dict:
        """
        Check Reddit API status with a simple test request
        """
        try:
            # Test with a simple request to r/programming - pass the endpoint correctly
            data = self._make_request("r/programming/hot", {"limit": 1})
            if data and "data" in data:
                return {
                    "status": "connected",
                    "message": "Successfully connected to Reddit API",
                    "note": "Using public Reddit JSON feeds",
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to fetch data from Reddit API",
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Reddit API connection failed: {str(e)}",
            }


class HackerNewsAPIClient:
    """
    Hacker News API client for fetching top stories and trending tech news
    """

    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        self.headers = {
            "User-Agent": "python:cs-student-hub:v1.0.0 (by /u/csstudent)",
            "Accept": "application/json",
        }

    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """
        Make request to Hacker News API with error handling
        """
        try:
            url = f"{self.base_url}/{endpoint}"

            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"Hacker News API error {response.status_code}: {response.text[:100]}"
                )
                return None

        except requests.RequestException as e:
            logger.error(f"Hacker News API request failed: {str(e)}")
            return None

    def get_story_details(self, story_id: int) -> Optional[Dict]:
        """
        Get details for a specific story
        """
        data = self._make_request(f"item/{story_id}.json")
        if not data:
            return None

        return {
            "id": data.get("id"),
            "title": data.get("title", "No title"),
            "url": data.get("url", ""),
            "score": data.get("score", 0),
            "by": data.get("by", "unknown"),
            "time": data.get("time", 0),
            "descendants": data.get("descendants", 0),  # comment count
            "type": data.get("type", "story"),
        }

    def get_top_stories(self, limit: int = 30) -> List[Dict]:
        """
        Get top stories from Hacker News
        """
        # Get list of top story IDs
        story_ids = self._make_request("topstories.json")
        if not story_ids:
            return []

        stories = []
        # Get details for first N stories
        for story_id in story_ids[:limit]:
            story = self.get_story_details(story_id)
            if (
                story and story["title"] and story["score"] >= 10
            ):  # Filter quality stories
                stories.append(story)

        logger.info(f"Successfully fetched {len(stories)} Hacker News stories")
        return stories

    def get_api_status(self) -> Dict:
        """
        Check Hacker News API status
        """
        try:
            data = self._make_request("topstories.json")
            if data and len(data) > 0:
                return {
                    "status": "connected",
                    "message": "Connected to Hacker News API",
                }
            else:
                return {"status": "error", "message": "No data from Hacker News API"}
        except Exception as e:
            return {"status": "error", "message": f"Hacker News API failed: {str(e)}"}


# Initialize all API clients
github_client = GitHubAPIClient()
reddit_client = RedditAPIClient()
hackernews_client = HackerNewsAPIClient()
