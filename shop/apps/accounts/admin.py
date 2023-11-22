from admin_decorators import order_field, short_description
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core import serializers
from django.http import HttpResponse
from django.utils.html import format_html

from .forms import UserChangeForm, UserCreationForm
from .models import Customer, CustomUser


def export_json(modeladmin, request, queryset):
    #! To create json
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm  # * form show
    add_form = UserCreationForm  # * form creating

    list_display = (
        "mobail_number",
        "email",
        "name",
        "family",
        "gender",
        "is_active",
        "is_admin",
    )
    list_filter = ("is_admin", "is_active", "gender")
    search_fields = ("mobail_number", "name", "family", "email")
    ordering = ("name", "family")
    list_editable = (
        "is_active",
        "is_admin",
    )

    actions = [export_json]
    # ? To divide the information page
    fieldsets = (
        (None, {"fields": ("mobail_number", "password", "active_code")}),
        ("اطلاعات شخصی", {"fields": ("name", "family", "email", "gender")}),
        (
            "دسترسی ها",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    # ? To divide the add page
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "mobail_number",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "اطلاعات شخصی",
            {
                "fields": (
                    "email",
                    "name",
                    "family",
                    "gender",
                ),
            },
        ),
        (
            None,
            {
                "fields": ("captcha",),
            },
        ),
    )

    export_json.short_description = "خروجی json گرفتن از کاربرهای انتخاب شده"

    filter_horizontal = ("groups", "user_permissions")  # * To display two columns


# todo --------------------------------------------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        # "show_image",
        "user",
        "address",
    )
    search_fields = (
        "address",
        "user",
    )
    ordering = ("user",)

    # @short_description("تصویر")
    # def show_image(self, obj):
    #     return format_html(
    #         f"<img src='{obj.image.url}' style='height:100px;' alt='بدون عکس' />"
    #     )

    actions = [export_json]

    export_json.short_description = "خروجی json گرفتن از مشتری های انتخاب شده"
