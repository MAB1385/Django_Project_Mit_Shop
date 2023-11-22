import os

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Article


@receiver(post_delete, sender=Article)
def delete_article_image(sender, **kwargs):
    path = settings.MEDIA_ROOT + str(kwargs["instance"].main_image)
    if os.path.isfile(path):
        os.remove(path)
