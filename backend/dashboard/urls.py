from django.urls import path
from . import views

urlpatterns = [
    path("status/", views.api_status, name="api_status"),
    path("trending/", views.trending_topics, name="trending_topics"),
    path("github/repos/", views.github_repositories, name="github_repositories"),
    path("github/languages/", views.github_languages, name="github_languages"),
]
