from django.conf import settings
from django.shortcuts import render
from django.views import View

from .models import Slider


class Index(View):  # ? Maine page view
    def get(self, *args, **kwargs):
        return render(self.request, "main/index.html")


# todo ------------------------------------------------------------
class SliderView(View):
    def get(self, *args, **kwargs):
        sliders = Slider.objects.filter(is_active=True)
        return render(self.request, "main/sliders.html", {"sliders": sliders})


# todo ------------------------------------------------------------
def media_admin(request):
    return {
        "media_url": settings.MEDIA_URL,
    }


# todo ------------------------------------------------------------
def handler404(request, exception=None):
    return render(request, "main/404.html")
