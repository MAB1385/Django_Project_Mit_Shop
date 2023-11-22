from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
    RelatedOnlyDropdownFilter,
    SimpleDropdownFilter,
)

from .models import Warehouse, WarehouseType


@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = (
        "title",
        "id",
    )
    ordering = ("id",)


# todo --------------------------------------------------------------------
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "warehouse_type",
        "user_registered",
        "qty",
        "price",
        "register_date",
    )
    list_filter = (
        ("product", RelatedDropdownFilter),
        ("user_registered", RelatedOnlyDropdownFilter),
        ("warehouse_type", RelatedDropdownFilter),
    )
    ordering = (
        "-register_date",
        "warehouse_type",
    )

    fieldsets = (
        (None, {"fields": ("warehouse_type",)}),
        (
            "اطلاعات تراکنش",
            {
                "fields": (
                    "user_registered",
                    ("product", "qty", "price"),
                )
            },
        ),
    )
