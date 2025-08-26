from django.urls import path
from . import views

urlpatterns = [
    # Status and main endpoints
    path("status/", views.api_status, name="api_status"),
    path("trending/", views.trending_topics, name="trending_topics"),
    # GitHub endpoints
    path("github/repos/", views.github_repositories, name="github_repositories"),
    path("github/languages/", views.github_languages, name="github_languages"),
    # Reddit endpoints
    path("reddit/posts/", views.reddit_posts, name="reddit_posts"),
    path("reddit/subreddits/", views.reddit_subreddits, name="reddit_subreddits"),
    # Hacker News endpoints
    path("hackernews/stories/", views.hackernews_stories, name="hackernews_stories"),
]
