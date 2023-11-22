from django.contrib import admin

from .models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "img_slide",
        "link",
        "is_active",
        "register_date",
        "published_date",
    )
    list_filter = ("is_active",)
    search_fields = (
        "text",
        "slider_link",
    )
    ordering = ("-register_date",)
    list_editable = ("is_active",)
    readonly_fields = ("img_slide",)

    fieldsets = (
        (
            "تنظیمات نمایش اسلایدر",
            {
                "fields": (
                    "text",
                    ("image", "slider_link"),
                    "is_active",
                )
            },
        ),
        (
            "تاریخ و زمان",
            {"fields": ("published_date",)},
        ),
    )
