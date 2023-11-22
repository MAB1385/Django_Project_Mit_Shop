from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from utils import FileUpload


class Slider(models.Model):
    text = RichTextUploadingField(
        config_name="default", null=True, blank=True, verbose_name="متن اسلایدر"
    )
    file_upload = FileUpload("images", "slides")
    image = models.ImageField(
        upload_to=file_upload.upload_to, verbose_name="تصویر اسلایدر"
    )
    slider_link = models.URLField(
        max_length=300, null=True, blank=True, verbose_name="لینک"
    )
    is_active = models.BooleanField(
        default=True, blank=True, verbose_name="فعال / غیر فعال"
    )
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درج")
    published_date = models.DateTimeField(
        default=timezone.now, verbose_name="تاریخ انتشار"
    )
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def __str__(self) -> str:
        return f"{self.text[:10]}"

    class Meta:
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلایدها"

    def img_slide(self):
        return format_html(f"<img src='/media/{self.image}' style='height:80px;'>")

    img_slide.short_description = "تصویر اسلاید"

    def link(self):
        return format_html(f"<a href='{self.slider_link}' target='_blank'>link</a>")

    link.short_description = "پیوند اسلاید"
