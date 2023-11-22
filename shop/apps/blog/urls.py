from django.urls import path

from .views import (
    ArticleDetailView,
    LastArticles,
    MostVisitedArticles,
    SearchArticleView,
    ShowArticlesView,
)

app_name = "blog"
urlpatterns = [
    path("articles/", ShowArticlesView.as_view(), name="show_articles"),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("last_articles/", LastArticles.as_view(), name="last_articles"),
    path(
        "most_visited_articles/",
        MostVisitedArticles.as_view(),
        name="most_visited_articles",
    ),
    path(
        "search/",
        SearchArticleView.as_view(),
        name="search",
    ),
]
