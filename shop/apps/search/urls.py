from django.urls import path

from .views import BrandsFilter, FeaturesFilter, SearchResultsView

app_name = "search"
urlpatterns = [
    path("", SearchResultsView.as_view(), name="search_view"),
    path(
        "product_features_filter/<str:q>/",
        FeaturesFilter.as_view(),
        name="product_features_filter",
    ),
    path(
        "product_brands_filter/<str:q>/",
        BrandsFilter.as_view(),
        name="product_brands_filter",
    ),
]
