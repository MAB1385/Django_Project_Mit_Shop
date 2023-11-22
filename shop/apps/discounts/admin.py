from admin_decorators import order_field, short_description
from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse

from .models import Coupon, DiscountBasket, DiscountBasketDetails


def export_json(modeladmin, request, queryset):
    #! To create json
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


# todo --------------------------------------------------------------------
class DiscountBasketDetailsInstanceInLineAdmin(admin.TabularInline):
    model = DiscountBasketDetails
    extra = 1


# todo --------------------------------------------------------------------
@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = (
        "discount_title",
        "discount",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("discount_title",)
    ordering = ("-start_date", "-end_date")
    list_editable = ("is_active",)

    fieldsets = (
        (None, {"fields": ("discount_title", "discount", "is_active")}),
        (
            "تاریخ و زمان",
            {
                "fields": ("start_date", "end_date"),
            },
        ),
    )
    inlines = [DiscountBasketDetailsInstanceInLineAdmin]

    actions = [export_json]

    export_json.short_description = "خروجی json گرفتن از سبدهای تخفیف انتخاب شده"


# todo --------------------------------------------------------------------
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "coupon_code",
        "discount",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("coupon_code",)
    ordering = ("-start_date", "-end_date")
    list_editable = ("is_active",)

    fieldsets = (
        (None, {"fields": ("coupon_code", "discount", "is_active")}),
        (
            "تاریخ و زمان",
            {
                "fields": ("start_date", "end_date"),
            },
        ),
    )
