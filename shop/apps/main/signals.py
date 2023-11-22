import os

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Slider


@receiver(post_delete, sender=Slider)
def delete_slider_image(sender, **kwargs):
    path = settings.MEDIA_ROOT + str(kwargs["instance"].image)
    if os.path.isfile(path):
        os.remove(path)
