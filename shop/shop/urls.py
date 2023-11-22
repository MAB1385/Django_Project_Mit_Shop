"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.accounts.views import LoginUserView, LogoutUserView

# from captcha_admin import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/login/", LoginUserView.as_view(), name="login"),  #!new
    path("admin/logout/", LogoutUserView.as_view(), name="logout"),  #!new
    path("admin/", admin.site.urls),
    path(
        "",
        include("apps.main.urls", namespace="main"),
        name="main",
    ),  # ! main app
    path(
        "accounts/",
        include("apps.accounts.urls", namespace="accounts"),
        name="accounts",
    ),  # ! accounts app
    path(
        "csf/",
        include("apps.comment_scoring_favorites.urls", namespace="csf"),
        name="csf",
    ),  # ! comment_scoring_favorites app
    path(
        "payments/",
        include("apps.payments.urls", namespace="payments"),
        name="payments",
    ),  # ! payments app
    path(
        "warehouses/",
        include("apps.warehouses.urls", namespace="warehouses"),
        name="warehouses",
    ),  # ! warehouses app
    path(
        "products/",
        include("apps.products.urls", namespace="products"),
        name="products",
    ),  # ! products app
    path(
        "discounts/",
        include("apps.discounts.urls", namespace="discounts"),
        name="discounts",
    ),  # ! discounts app
    path(
        "orders/",
        include("apps.orders.urls", namespace="orders"),
        name="orders",
    ),  # ! orders app
    path(
        "search/",
        include("apps.search.urls", namespace="search"),
        name="search",
    ),  # ! search app
    path(
        "blog/",
        include("apps.blog.urls", namespace="blog"),
        name="blog",
    ),  # ! blog app
    path(
        "ckeditor",
        include("ckeditor_uploader.urls"),
    ),  # ! ckeditor
    # // path("jet_api/", include("jet_django.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # ? Permission to access media files

# ? To admin panel:
admin.site.site_header = "میت شاپ"
admin.site.site_title = "میت شاپ"
admin.site.index_title = "پنل مدیریت"

# ? For 404 error:
handler404 = "apps.main.views.handler404"
