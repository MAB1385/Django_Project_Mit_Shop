import os

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Brand, Product, ProductGallery, ProductGroup


@receiver(post_delete, sender=Product)
def delete_product_image(sender, **kwargs):
    path = settings.MEDIA_ROOT + str(kwargs["instance"].image)
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=Brand)
def delete_brand_image(sender, **kwargs):
    path = settings.MEDIA_ROOT + str(kwargs["instance"].image)
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=ProductGallery)
def delete_product_gallery_image(sender, **kwargs):
    path = settings.MEDIA_ROOT + str(kwargs["instance"].image)
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=ProductGroup)
def delete_product_group_image(sender, **kwargs):
    path = settings.MEDIA_ROOT + str(kwargs["instance"].image)
    if os.path.isfile(path):
        os.remove(path)
