from django.urls import path

from .views import Index, SliderView

app_name = "main"
urlpatterns = [
    path("", Index.as_view(), name="home"),  # ! Main page --> home
    path("sliders/", SliderView.as_view(), name="sliders"),  # ! sliders
]
