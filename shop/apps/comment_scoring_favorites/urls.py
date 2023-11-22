from django.urls import path

from .views import (
    AddScore,
    AddToFavorite,
    CommentView,
    DeleteFromFavorite,
    ShowFavorite,
    status_of_favorite,
)

app_name = "csf"
urlpatterns = [
    path("create_comment/<slug:slug>/", CommentView.as_view(), name="create_comment"),
    path("add_score/", AddScore.as_view(), name="add_score"),
    path("add_to_favorite/", AddToFavorite.as_view(), name="add_to_favorite"),
    path(
        "delete_from_favorite/",
        DeleteFromFavorite.as_view(),
        name="delete_from_favorite",
    ),
    path(
        "show_favorite/",
        ShowFavorite.as_view(),
        name="show_favorite",
    ),
    path(
        "status_of_favorite/",
        status_of_favorite,
        name="status_of_favorite",
    ),
]
