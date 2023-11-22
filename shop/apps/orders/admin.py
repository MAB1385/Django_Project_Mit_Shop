from admin_decorators import order_field, short_description
from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse

from .models import Order, OrderState, PaymentType, ShopCart


def export_json(modeladmin, request, queryset):
    #! To create json
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


# todo --------------------------------------------------------------------
class ShopCartInstanceInLineAdmin(admin.TabularInline):
    model = ShopCart
    extra = 0


# todo --------------------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "order_state",
        "register_date",
        "is_finaly",
        "discount",
        "order_code",
    )
    list_filter = ("is_finaly", "order_state")
    search_fields = ("order_code",)
    ordering = ("-update_date",)
    list_editable = ("is_finaly",)

    fieldsets = (
        (None, {"fields": ("customer", "is_finaly", "discount", "order_state")}),
        (
            "تاریخ و زمان",
            {
                "fields": ("register_date",),
            },
        ),
    )
    inlines = [ShopCartInstanceInLineAdmin]

    actions = [export_json]

    @short_description("تعداد کالاهای گروه")
    @order_field("product_of_group")  #! To add sorting by this field
    def product_of_group(self, obj):
        return obj.product_of_group

    export_json.short_description = "خروجی json گرفتن از سفارشات انتخاب شده"


# todo --------------------------------------------------------------------
@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ("payment_title",)
    search_fields = ("payment_title",)
    ordering = ("payment_title",)


# todo --------------------------------------------------------------------
@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)
    ordering = ("id",)
